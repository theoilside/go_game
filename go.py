import math
from enum import Enum
import random


def generate_starting_board_2d(size):
    board = ['x' * (size + 2)]
    for i in range(size):
        board.append('x' + ('.' * size) + 'x')
    board.append('x' * (size + 2))
    return board


class Colors(Enum):
    white = 'white'
    black = 'black'

    def get_opposite(self):
        if self.value == 'white':
            return 'black'
        return 'white'


class TypesOfGames(Enum):
    singleplayer = 'singleplayer'
    multiplayer = 'multiplayer'


class Game:
    def __init__(self):
        self.board = None
        self.color_of_current_move = Colors.black

    def start_new_game(self, size):
        self.board = Board(size)

    def place_piece(self, color: Colors, x, y):
        self.board.place_piece(color, x, y)
        self.color_of_current_move = self.color_of_current_move.get_opposite()


class SingleplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.color_of_human = None
        self.color_of_AI = None
        self.AI = None

    def start_new_game(self, size, color_of_human: Colors = 'black'):
        super().start_new_game(size)
        self.color_of_human = color_of_human
        self.color_of_AI = color_of_human.get_opposite()
        self.AI = AI(self.board)

    def make_ai_move(self):
        x, y = self.AI.get_move()
        self.place_piece(self.color_of_AI, x, y)
        return x, y


class MultiplayerGame(Game):
    def __init__(self):
        super().__init__()

    def start_new_game(self, size):
        super().start_new_game(size)


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self, current_color: Colors = 'white'):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class Board:
    # В этот список вносятся дамэ / дыхания (liberties)
    list_of_liberties = []
    list_of_block = []

    def __init__(self, size):
        self.size = size
        self.board = generate_starting_board_2d(size)
        self.size_with_borders = size + 2

    def print(self):
        for row in self.board:
            print(row)

    def calculate_id(self, x, y):
        return y * self.size_with_borders + x

    def place_piece(self, color: Colors, x, y):
        if not (self.size > x >= 0 and self.size > y >= 0):
            raise ('id слишком большой/маленький! Введенное значение id: {0}. Доступный диапазон: от 0 до {1}'
                   .format(id, self.size))
        if color == Colors.black:
            self.board[y + 1][x + 1] = Cell(TypesOfCells.black)
        else:
            self.board[y + 1][x + 1] = Cell(TypesOfCells.white)

    def get_piece_by_id(self, id):
        if id < 0 or id >= (self.size + 2) * (self.size + 2):
            raise ('id слишком большой/маленький! Введенное значение id: {0}'.format(id))
        return self.board[math.floor(id / (self.size + 2))][id % (self.size + 2)]

    def calculate_liberties(self, location_id, color):
        if color not in ('w', 'b'):
            raise ('Цветом может быть только “w” или “b”! Введенное значение color: {0}'.format(color))
        piece = self.get_piece_by_id(location_id)
        if piece == 'x':
            return
        if piece and piece == color:
            ...
        #     # save stone's coordinate
        #     block.append(square)
        #
        #     # mark the stone
        #     board[square] |= MARKER
        #
        #     # look for neighbours recursively
        #     count(square - BOARD_RANGE, color)  # walk north
        #     count(square - 1, color)  # walk east
        #     count(square + BOARD_RANGE, color)  # walk south
        #     count(square + 1, color)  # walk west
        #
        # # if the square is empty
        # elif piece == EMPTY:
        #     # mark liberty
        #     board[square] |= LIBERTY
        #
        #     # save liberty
        #     liberties.append(square)


class TypesOfCells(Enum):
    black = 'b'
    white = 'w'
    empty = '.'
    border = 'x'


class Cell:
    def __init__(self, type: TypesOfCells):
        self.type = type


game = SingleplayerGame()
print('Напиши, каким цветом хочешь играть — «b» или «w». Первыми ходят черные')
color_of_human = input()
game.start_new_game(9)
while True:
    game.board.print()
    print('Напиши свой ход в формате «x,y», где «x» и «y» — координаты')
