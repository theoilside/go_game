import math
import random
from game.game import SingleplayerGame
from game.enums import *


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class Board:
    def __init__(self, size):
        self.size = size
        self.size_with_borders = size + 2
        board = [[TypesOfCells.border] * self.size_with_borders]
        for i in range(self.size):
            data_of_row = ([TypesOfCells.border] + [TypesOfCells.empty] * self.size + [TypesOfCells.border])
            board.append(data_of_row)
        board.append([TypesOfCells.border] * self.size_with_borders)
        self.board = board

    def __str__(self):
        array = []
        for row in self.board:
            for element in row:
                array.append(str(element))
            array.append('\n')
        return ''.join(array)

    def calculate_id(self, x, y):
        return y * self.size_with_borders + x

    def place_piece(self, color: Colors, x: int, y: int):
        if not (self.size - 1 >= x >= 0 and self.size >= y >= 0):
            raise IndexError(f'x или y слишком большой/маленький! Полученные значения: {x} и {y}. Доступный диапазон: '
                             f'[0, {self.size - 1}].')
        if self.board[y+1][x+1] == TypesOfCells.empty:
            if color == Colors.black:
                self.board[y+1][x+1] = Cell(TypesOfCells.black)
            else:
                self.board[y+1][x+1] = Cell(TypesOfCells.white)
            return True
        return False

    def get_piece_by_id(self, id):
        if id < 0 or id >= (self.size + 2) * (self.size + 2):
            raise IndexError(f'id слишком большой/маленький! Полученное значение id: {id}.')
        return self.board[math.floor(id / (self.size + 2))][id % (self.size + 2)]

    # В этот список вносятся дамэ / дыхания (liberties)
    list_of_liberties = []
    list_of_block = []

    def calculate_liberties(self, location_id, color):
        if color not in ('w', 'b'):
            raise IndexError(f'Цветом может быть только “w” или “b”! Полученное значение: {color}.')
        piece = self.get_piece_by_id(location_id)
        if piece == 'x':
            return
        if piece and piece == color:
            ...
        #    list_of_block.append(square)
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
    def __init__(self, type: TypesOfCells):
        self.type = type

    def __str__(self):
        return str(self.type)


def start_cli():
    game = SingleplayerGame()
    print('Напиши, каким цветом хочешь играть — «b» или «w». Первыми ходят черные')
    inputted_color = input()
    if inputted_color == 'w':
        color_of_human = Colors.white
    elif inputted_color == 'b':
        color_of_human = Colors.black
    else:
        raise IndexError('Неправильный цвет!')
    print('Напиши размер поля')
    inputted_size = input()
    if int(inputted_size) < 2:
        raise IndexError('Неправильный размер!')
    game.start_new_game(int(inputted_size), color_of_human)
    while True:
        print(game.board)
        while True:
            print('Напиши свой ход в формате «x,y», где «x» и «y» — координаты')
            inputted_coords = input().split(',')
            if game.place_piece(int(inputted_coords[0]), int(inputted_coords[1])):
                break
            print('Туда ходить нельзя, выбери другое место')
        print('Ходит компьютер...')
        game.make_ai_move()
