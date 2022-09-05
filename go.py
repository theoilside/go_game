import math
import random

import Game
from enums import *


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class Board:
    # В этот список вносятся дамэ / дыхания (liberties)
    list_of_liberties = []
    list_of_block = []

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

    def generate_starting_board(self):
        board = [[TypesOfCells.border] * self.size_with_borders]
        for i in range(self.size):
            data_of_row = ([TypesOfCells.border] + [TypesOfCells.empty] * self.size + [TypesOfCells.border])
            board.append(data_of_row)
        board.append([TypesOfCells.border] * self.size_with_borders)
        return board

    def calculate_id(self, x, y):
        return y * self.size_with_borders + x

    def place_piece(self, color: Colors, x, y):
        if not (self.size >= x >= 1 and self.size >= y >= 1):
            raise ('id слишком большой/маленький! Введенное значение id: {0}. Доступный диапазон: от 0 до {1}'
                   .format(id, self.size))
        if self.board[y][x] == TypesOfCells.empty:
            if color == Colors.black:
                self.board[y][x] = Cell(TypesOfCells.black)
            else:
                self.board[y][x] = Cell(TypesOfCells.white)
            return True
        return False

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


class Cell:
    def __init__(self, type: TypesOfCells):
        self.type = type

    def __str__(self):
        return str(self.type)


if __name__ == '__main__':
    game = Game.SingleplayerGame()
    print('Напиши, каким цветом хочешь играть — «b» или «w». Первыми ходят черные')
    inputted_color = input()
    if inputted_color == 'w':
        color_of_human = Colors.white
    elif inputted_color == 'b':
        color_of_human = Colors.black
    else:
        raise 'Неправильный цвет!'
    print('Напиши размер поля')
    inputted_size = input()
    if int(inputted_size) < 2:
        raise 'Неправильный размер!'
    game.start_new_game(int(inputted_size), color_of_human)
    while True:
        print(game.board)
        while True:
            print('Напиши свой ход в формате «x,y», где «x» и «y» — координаты')
            inputted_coords = input().split(',')
            if game.place_piece(int(inputted_coords[0]), int(inputted_coords[1])):
                break
            print('Туда ходить нельзя, выбери другое место')
        game.make_ai_move()
