from .game import SingleplayerGame, MultiplayerGame
from .enums import Colors
import re


def start_cli():
    print('Выберите режим игры. Одиночная игра — игра с компьютером, '
          'мультиплеерная — hotseat-режим для двух людей за одним компьютером.')
    print('[одиночная — 0 (default); мультиплеерная — 1]')
    print('Ввод:', end=' ')
    interface = input()
    if interface == '0' or interface == '':
        singleplayer_cli()
    elif interface == '1':
        multiplayer_cli()
    else:
        raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')


def singleplayer_cli():
    game = SingleplayerGame()
    print('Выберите цвет своих камней. Первыми ходят черные камни.')
    print('[черные — 0 (default); белые — 1]')
    print('Ввод:', end=' ')
    interface = input()
    if interface == '0' or interface == '':
        color_of_human = Colors.black
    elif interface == '1':
        color_of_human = Colors.white
    else:
        raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')
    print('Выберите размер игрового поля. Минимальный размер: 5х5; максимальный: 19х19.')
    print('[например, поле 9х9 — 9 (default)]')
    print('Ввод:', end=' ')
    interface = input()
    board_size = 9
    if interface:
        try:
            board_size = int(interface)
        except TypeError:
            raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо любое число из диапазона [5, 19]')
    if not 4 < board_size < 20:
        raise NameError(f'Неподходящие размеры. Получено: {board_size}. Допустим любой размер из диапазона [5, 19]')
    game.start_new_game(int(board_size), color_of_human)
    while True:
        print(f'Белых захвачено: {game.captured_white}, черных захвачено: {game.captured_black}.')
        print(game.board)
        while True:
            print('Напишите свой ход в формате «x,y», где «x» и «y» — координаты')
            print('Ввод:', end=' ')
            interface = input()
            if not re.fullmatch(r'\d+,\d+', interface):
                print('Некорректный ввод координат! Требуемый формат: x,y (например: 1,2).')
                continue
            inputted_coords = interface.split(',')
            try:
                if game.make_player_move(int(inputted_coords[0]), int(inputted_coords[1])).is_success:
                    break
            except IndexError as e:
                print(e)
                continue
            print('Туда ходить нельзя, выберите другое место!')
        print('Ходит компьютер...')
        game.make_ai_move()


def multiplayer_cli():
    game = MultiplayerGame()
    print('Выберите размер игрового поля. Минимальный размер: 5х5; максимальный: 19х19.')
    print('[например, поле 9х9 — 9 (default)]')
    print('Ввод:', end=' ')
    interface = input()
    board_size = 9
    if interface:
        try:
            board_size = int(interface)
        except TypeError:
            raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо любое число из диапазона [5, 19]')
    if not 4 < board_size < 20:
        raise NameError(f'Неподходящие размеры. Получено: {board_size}. Допустим любой размер из диапазона [5, 19]')
    game.start_new_game(int(board_size))
    while True:
        print(game.board)
        print(f'→ Сейчас ходят {game.color_of_current_move}')
        print(f'Белых захвачено: {game.captured_white}, черных захвачено: {game.captured_black}.')
        while True:
            print('Напишите свой ход в формате x,y, где x и y — координаты')
            print('Ввод:', end=' ')
            interface = input()
            if not re.fullmatch(r'\d+,\d+', interface):
                print('Некорректный ввод координат! Требуемый формат: x,y (например: 1,2).')
                continue
            inputted_coords = interface.split(',')
            try:
                result = game.make_player_move(int(inputted_coords[0]), int(inputted_coords[1]))
                if result.is_success:
                    break
            except IndexError as e:
                print(e)
                continue
            print('Туда ходить нельзя, выберите другое место!')
