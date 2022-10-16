from __future__ import annotations
import copy
from collections import namedtuple
from game.enums import *


class Cell:
    def __init__(self, type: CellTypes, state: CellStates, x: int, y: int):
        self.type = type
        self.state = state
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.type)


def generate_empty_board(size):
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
        self.current_borders = []

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
            response = self.if_permitted_move(initial_cell, piece_type)
            if response.is_permitted_move:
                return Response(True, response.captured)
        return Response(False, None)

    def if_permitted_move(self, initial_cell: Cell, new_type: CellTypes):
        Response = namedtuple('Response', ('is_permitted_move', 'captured'), defaults=(False, None))
        # save current board
        initial_board = copy.deepcopy(self)
        # create next board
        self.update_cell(initial_cell, new_type)
        suicide_captured = [item for items in self.get_captured_groups(new_type.get_color()) for item in items]
        opponent_captured = [item for items in self.get_captured_groups(new_type.get_opposite_color().get_color()) for item in items]
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
                        captured.append(self.capture_current_group())
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

    def capture_current_group(self):
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
    def __init__(self, board: Board, size: int):
        super().__init__(size)
        self.board: Board = board
        self.size_with_borders: int = board.size_with_borders
        self.players_territory: list[list[Cell]] = []

    def remove_cell_at(self, x, y):
        adjusted_x = x + 1
        adjusted_y = y + 1
        self.board[adjusted_y][adjusted_x] = Cell(CellTypes.empty, CellStates.unmarked, adjusted_x, adjusted_y)

    def count_territory(self, color: Colors):
        # Using Flood fill algorithm
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                self.players_territory.append([cell])
                self.flood_fill(color, x, y)

    def flood_fill(self, color: Colors, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell.state == CellStates.marked or cell.type == Colors.get_type_of_cells(color):
            return
        if cell.type == CellTypes.get_opposite_color(color.get_type_of_cells()):
            self.players_territory.pop()
            return
        if cell.type == CellTypes.empty:
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




