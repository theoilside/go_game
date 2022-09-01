import math

def generate_starting_board_2d(size):
    board = ['x' * (size + 2)]
    for i in range(size):
        board.append('x' + ('.' * size) + 'x')
    board.append('x' * (size + 2))
    return board


class Board:
    # В этот список вносятся дамэ / дыхания (liberties)
    list_of_liberties = []
    list_of_block = []

    def __init__(self, size):
        self.size = size
        self.board = generate_starting_board_2d(size)

    def print(self):
        for row in self.board:
            print(row)

    def get_piece_by_id(self, id):
        if id < 0 or id >= (self.size + 2) * (self.size + 2):
            raise('id слишком большой/маленький! Введенное значение id: {0}'.format(id))
        else:
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


class Object:
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
