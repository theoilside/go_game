from __future__ import annotations
import copy
from collections import namedtuple
from game.enums import *


class Cell:
    def __init__(self, cell_type: CellTypes, state: CellStates, x: int, y: int):
        self.type = cell_type
        self.state = state
        self.x = x
        self.y = y

        self.dead: bool = False

    def __str__(self):
        return str(self.type)

    def __eq__(self, other: Cell):
        return self.type == other.type and self.state == other.state and self.x == other.x and self.y == other.y

    def check_dead(self):
        self.dead = not self.dead


def generate_empty_board(size):
    if size < 0:
        raise ValueError(f'Size must be non-negative. Got {size}')
    if size > 21:
        raise ValueError(f'Size is too large, 21 is maximum. Got {size}')
    board = []
    row = []
    for x in range(size):
        row.append(Cell(CellTypes.border, CellStates.unmarked, x, 0))
    board.append(row)
    for y in range(1, size - 1):
        row = [Cell(CellTypes.border, CellStates.unmarked, 0, y)]
        for x in range(1, size - 1):
            row.append(Cell(CellTypes.empty, CellStates.unmarked, x, y))
        row.append(Cell(CellTypes.border, CellStates.unmarked, size - 1, y))
        board.append(row)
    row = []
    for x in range(size):
        row.append(Cell(CellTypes.border, CellStates.unmarked, x, size - 1))
    board.append(row)
    return board


class Board:
    def __init__(self, size: int):
        self.size: int = size
        self.size_with_borders = size + 2
        self.board = generate_empty_board(self.size_with_borders)
        self.current_liberties = []
        self.current_groups = []
        self.last_captured = []
        self.previous_board: None | Board = None

    def __eq__(self, other):
        self_size = self.size_with_borders
        other_size = other.size_with_borders
        if self_size == other_size:
            for i in range(self_size):
                for j in range(self_size):
                    if self.board[i][j].type != other.board[i][j].type:
                        return False
            return True
        return False

    def __str__(self):
        array = ['   ']
        row_index = 0
        for column_index in range(self.size):
            array.append(str(column_index) + ' ')
        array.append('\n')
        for row in self.board[1:-1]:
            array.append(str(row_index) + '  ')
            for element in row[1:-1]:
                array.append(str(element) + ' ')
            array.append('\n')
            row_index += 1
        return ''.join(array)

    def get_cell(self, x, y):
        if not (self.size_with_borders > x >= 0 and self.size_with_borders > y >= 0):
            raise IndexError(f'Координаты слишком большие/маленькие! Полученные значения: {x - 1} и {y - 1}. '
                             f'Доступный диапазон: [0, {self.size}).')
        return self.board[y][x]

    def update_cell(self, cell: Cell, new_type: CellTypes = None, new_state: CellStates = None):
        if not new_type:
            new_type = cell.type
        if not new_state:
            new_state = cell.state
        self.board[cell.y][cell.x] = Cell(new_type, new_state, cell.x, cell.y)

    def replace_board(self, new_board: Board):
        self.size = new_board.size
        self.size_with_borders = new_board.size_with_borders
        self.board = new_board.board
        self.current_liberties = new_board.current_liberties
        self.current_groups = new_board.current_groups
        self.last_captured = new_board.last_captured
        self.previous_board = new_board.previous_board

    def place_piece(self, color: Colors, x, y):
        Response = namedtuple('Response', ('is_permitted_move', 'captured'), defaults=(False, None))
        # Берем ячейку с координатами на 1 больше, так как в эту функцию отправляются запросы без учета границ board.
        adjusted_x = x + 1
        adjusted_y = y + 1
        piece_type = CellTypes.black
        if color == Colors.white:
            piece_type = CellTypes.white
        initial_cell = self.get_cell(adjusted_x, adjusted_y)
        if initial_cell.type == CellTypes.empty and initial_cell.type != CellTypes.border:
            response = self.is_permitted_move(initial_cell, piece_type)
            if response.is_permitted_move:
                return Response(True, response.captured)
        return Response(False, None)

    def is_permitted_move(self, initial_cell: Cell, new_type: CellTypes):
        Response = namedtuple('Response', ('is_permitted_move', 'captured'), defaults=(False, None))
        # save current board
        initial_board = copy.deepcopy(self)
        # create next board
        self.update_cell(initial_cell, new_type)
        suicide_captured = [item for items in self.get_captured_groups(new_type.get_color()) for item in items]
        opponent_captured = [item for items in self.get_captured_groups(new_type.get_opposite_color().get_color()) for
                             item in items]
        # check for suicide
        if suicide_captured and not opponent_captured:
            self.replace_board(initial_board)
            return Response(False, None)
        self.remove_pieces(opponent_captured)
        # check for ko
        if self.previous_board and self.previous_board == self:
            self.replace_board(initial_board)
            return Response(False, None)
        self.previous_board = initial_board
        return Response(True, opponent_captured)

    def get_captured_groups(self, color: Colors):
        captured = []
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                if cell.type == CellTypes.border:
                    continue
                if cell.type == Colors.get_type_of_cells(color):
                    self.compute_board_updates(color, x, y)
                    if len(self.current_liberties) == 0:
                        captured.append(self.get_current_captured_group())
                    self.restore_states()
        return captured

    def compute_board_updates(self, color: Colors, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell.type == CellTypes.border:
            return
        if cell.type == CellTypes.empty:
            self.current_liberties.append(cell)
        elif cell.type.value == color and cell.state == CellStates.unmarked:
            self.update_cell(cell, None, CellStates.marked)
            self.current_groups.append(cell)
            # Walk ↑
            self.compute_board_updates(color, x, y - 1)
            # Walk →
            self.compute_board_updates(color, x + 1, y)
            # Walk ↓
            self.compute_board_updates(color, x, y + 1)
            # Walk ←
            self.compute_board_updates(color, x - 1, y)

    def get_current_captured_group(self):
        captured = []
        for i in range(len(self.current_groups)):
            captured.append(self.current_groups[i])
        return captured

    def remove_pieces(self, captured: list):
        if captured:
            for i in range(len(captured)):
                self.update_cell(captured[i], CellTypes.empty, CellStates.unmarked)

    def restore_states(self):
        self.current_groups.clear()
        self.current_liberties.clear()
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                if cell.state == CellStates.marked:
                    self.update_cell(cell, None, CellStates.unmarked)


class FinalizedBoard(Board):
    def __init__(self, board: Board):
        super().__init__(board.size)
        self.board: list[list[Cell]] = board.board
        self.size_with_borders: int = board.size_with_borders
        self.players_territory: list[list[Cell]] = [[]]
        self.met_opponent = False

    def get_cell(self, x, y):
        if not (self.size_with_borders > x >= 0 and self.size_with_borders > y >= 0):
            raise IndexError(f'Координаты слишком большие/маленькие! Полученные значения: {x - 1} и {y - 1}. '
                             f'Доступный диапазон: [0, {self.size}).')
        return self.board[y][x]

    def count_territory(self, color: Colors):
        # Using Flood fill algorithm
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                if cell.state.unmarked:
                    self.met_opponent = False
                    self.players_territory.append([])
                    self.flood_fill(color, x, y)
                    self.players_territory = [x for x in self.players_territory if x]
        territory_array = copy.deepcopy(sum(self.players_territory, []))
        self.restore_board()
        return len(self.get_unique_cells(territory_array))

    def flood_fill(self, color: Colors, x: int, y: int):
        if not self.met_opponent:
            cell = self.get_cell(x, y)
            if cell.state == CellStates.marked or cell.type == Colors.get_type_of_cells(color):
                return
            if cell.type == CellTypes.get_opposite_color(color.get_type_of_cells()):
                if self.players_territory and self.players_territory[-1]:
                    self.players_territory.pop()
                self.mark_only_territory()
                self.met_opponent = True
                return
            if cell.type == CellTypes.empty:
                if cell.x == 1 and cell.y == 6:
                    hello = 'world'
                self.update_cell(cell, None, CellStates.marked)
                self.players_territory[-1].append(cell)
                # Walk ↑
                self.flood_fill(color, x, y - 1)
                # Walk →
                self.flood_fill(color, x + 1, y)
                # Walk ↓
                self.flood_fill(color, x, y + 1)
                # Walk ←
                self.flood_fill(color, x - 1, y)

    def mark_only_territory(self):
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                if cell.state == CellStates.marked and cell not in sum([x for x in self.players_territory if x], []):
                    self.update_cell(cell, None, CellStates.unmarked)

    def restore_board(self):
        self.met_opponent = False
        self.players_territory.clear()
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                if cell.state == CellStates.marked:
                    self.update_cell(cell, None, CellStates.unmarked)

    def get_unique_cells(self, list_of_cells: list[Cell]):
        unique_coordinates = []
        unique_cells = []
        for cell in list_of_cells:
            coordinates = cell.x, cell.y
            if coordinates in unique_coordinates:
                continue
            unique_coordinates.append(coordinates)
        for coordinate in unique_coordinates:
            unique_cells.append(self.get_cell(coordinate[0], coordinate[1]))
        return unique_cells
