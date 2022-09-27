import random
from game.enums import *


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


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
    def __init__(self, size):
        self.size = size
        self.size_with_borders = size + 2
        self.board = generate_empty_board(self.size_with_borders)
        self.current_liberties = []
        self.current_groups = []

    def __str__(self):
        array = []
        for row in self.board:
            for element in row:
                array.append(str(element))
            array.append('\n')
        return ''.join(array)

    def get_cell(self, x, y):
        if not (self.size_with_borders > x >= 0 and self.size_with_borders > y >= 0):
            raise IndexError(f'x или y слишком большой/маленький! Полученные значения: {x} и {y}. Доступный диапазон: '
                             f'[0, {self.size_with_borders}).')
        return self.board[y][x]

    def update_cell(self, cell: Cell, new_type: CellTypes = None, new_state: CellStates = None):
        if not new_type:
            new_type = cell.type
        if not new_state:
            new_state = cell.state
        self.board[cell.y][cell.x] = Cell(new_type, new_state, cell.x, cell.y)
        return True

    def place_piece(self, color: Colors, x, y):
        # Берем ячейку с координатами на 1 больше, так как в эту функцию отправляются запросы без учета границ board.
        adjusted_x = x + 1
        adjusted_y = y + 1
        initial_cell = self.get_cell(adjusted_x, adjusted_y)
        if initial_cell.type == CellTypes.empty and initial_cell.type != CellTypes.border:
            if color == Colors.black:
                self.update_cell(initial_cell, CellTypes.black)
                self.get_captured_groups(Colors.white)
            else:
                self.update_cell(initial_cell, CellTypes.white)
                self.get_captured_groups(Colors.black)
            # self.compute_board_updates(color, adjusted_x, adjusted_y)
            return True
        return False

    def get_captured_groups(self, color: Colors):
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                color_of_cell = Colors.get_type_of_cells(color)
                if cell.type == CellTypes.border:
                    continue
                if color_of_cell == cell.type:
                    self.compute_board_updates(color, x, y)
                    if len(self.current_liberties) == 0:
                        self.capture_current_group()
                    self.restore_states()

    def compute_board_updates(self, color: Colors, x, y):
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
        for i in range(len(self.current_groups)):
            self.update_cell(self.current_groups[i], CellTypes.empty, CellStates.unmarked)

    def restore_states(self):
        self.current_groups.clear()
        self.current_liberties.clear()
        for x in range(self.size_with_borders):
            for y in range(self.size_with_borders):
                cell = self.get_cell(x, y)
                if cell.state == CellStates.marked:
                    self.update_cell(cell, None, CellStates.unmarked)