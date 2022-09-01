import math
from enum import Enum


def generate_starting_board_2d(size):
    board = ['x' * (size + 2)]
    for i in range(size):
        board.append('x' + ('.' * size) + 'x')
    board.append('x' * (size + 2))
    return board

class Colors(Enum):
    white = 'white'
    black = 'black'


class TypesOfGames(Enum):
    singleplayer = 'singleplayer'
    multiplayer = 'multiplayer'


class Game:
    def __init__(self):
        self.board = None
        self.type_of_game = None
        self.color_of_player = None

    def start_new_game(self, size, type_of_game: TypesOfGames, color_of_player: Colors = 'black'):
        self.board = Board(size)
        self.type_of_game = type_of_game
        self.color_of_player = color_of_player

    def place_piece(self, color: Colors, x, y):
        self.board.place_piece(color, x, y)

    def request_ai_move(self):
        ...




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

    def place_piece(self, color, x, y):
        if color not in ('black', 'white'):
            raise ('Цветом может быть только “black” или “white”! Введенное значение color: {0}'.format(color))
        if not (self.size > x >= 0 and self.size > y >= 0):
            raise ('id слишком большой/маленький! Введенное значение id: {0}'.format(id))
        self.board[y+1][x+1] = Cell(color)

    def get_piece_by_id(self, id):
        if id < 0 or id >= (self.size + 2) * (self.size + 2):
            raise('id слишком большой/маленький! Введенное значение id: {0}'.format(id))
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


class Cell:
    types = {
        'black': 'b',
        'white': 'w',
        'empty': '.',
        'void': 'x'
    }

    def __init__(self, type):
        if type not in self.types:
            raise ('Неверно указан тип объекта! Возможные значения: {0}'.format(self.types.keys))
        self.type = type



new_game = Board(9)
new_game.print()
