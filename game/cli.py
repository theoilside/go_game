from .game import SingleplayerGame, MultiplayerGame
from .enums import Colors, AILevel
import re


class CLI:
    def __init__(self):
        self.game = None
        self.board_size: int = 9
        self.completed_game: bool = False

    def ask_for_size(self):
        print('? Выберите размер игрового поля. Минимальный размер: 5х5; максимальный: 19х19.')
        print('[например, поле 9х9 — 9 (default)]')
        print('Ввод:', end=' ')
        interface = input()
        if interface:
            try:
                self.board_size = int(interface)
            except TypeError:
                raise NameError(f'! Неверный ввод. Получено: {interface}. Допустимо число из диапазона [5, 19]')
        if not 4 < self.board_size < 20:
            raise NameError(f'! Неподходящие размеры. Получено: {self.board_size}. '
                            f'Допустимо число из диапазона [5, 19]')

    def end_game(self):
        self.game.finalize_board()
        self.ask_for_count()
        self.count_points()

    def ask_for_count(self):
        print('? Выберите полуавтоматический или самостоятельный подсчет территорий.')
        print('[полуавтоматический — 0 (default); самостоятельный — 1]')
        print('Ввод:', end=' ')
        interface = input()
        if interface == '0' or interface == '':
            dead_stones = self.ask_for_dead_stones()
            if dead_stones:
                self.game.remove_pieces_at_coords(dead_stones)
            print('i Текущая игровая доска:')
            print(self.game.board)
        elif interface == '1':
            territory = self.ask_for_territory()
            self.game.count_points(int(territory[0]), int(territory[1]))
        else:
            raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')

    def ask_for_dead_stones(self):
        print('i Текущая игровая доска:')
        print(self.game.board)
        print('? Введите координаты всех мертвых (dead) камней.')
        print('[удалить камни по координатам (x,y) и (a,b) — x,y;a,b; не удалять камни — пустое поле (default)]')
        print('Ввод:', end=' ')
        interface = input()
        list_of_coords = []
        if interface:
            coords = interface.split(';')
            for coord in coords:
                xy = coord.split(',')
                list_of_coords.append((int(xy[0]), int(xy[1])))
        return list_of_coords

    def ask_for_territory(self):
        print('i Текущая игровая доска:')
        print(self.game.board)
        print('? Введите площади захваченных территорий черными и белыми.')
        print('[площадь у черных X и площадь у белых Y — X,Y; нет захваченных площадей — пустое поле (default)]')
        print('Ввод:', end=' ')
        territory_interface = input()
        territory = territory_interface.split(',')
        return territory

    def count_points(self):
        self.game.count_points()
        print()
        print('i Итоговый игровой счет:')
        print(f'Черные: {self.game.black_points}. Белые: {self.game.white_points}')
        if self.game.black_points > self.game.white_points:
            print('i Черные победили!')
        else:
            print('i Белые победили!')


class SingleplayerCLI(CLI):
    def __init__(self):
        super().__init__()
        self.human_name: str | None = None
        self.human_color: Colors = Colors.black
        self.AI_level: AILevel = AILevel.normal
        self.player_can_move: bool = True

    def start_singleplayer(self):
        self.game = SingleplayerGame()
        self.ask_for_size()
        self._ask_for_human_color()
        self._ask_for_human_name()
        self._ask_for_AI_level()
        self.game.start_singleplayer_game(self.board_size, self.human_name, self.human_color, self.AI_level)
        while not self.completed_game:
            self._ask_for_human_turn()
            if not self.completed_game:
                self._ask_for_ai_turn()
        self.end_game()

    def _ask_for_human_color(self):
        print('? Выберите цвет своих камней. Первыми ходят черные камни, за это у белых компенсация в +6,5 очков.')
        print('[черные — 0 (default); белые — 1]')
        print('Ввод:', end=' ')
        interface = input()
        if interface == '0' or interface == '':
            self.human_color = Colors.black
        elif interface == '1':
            self.human_color = Colors.white
            self.player_can_move = False
        else:
            raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')

    def _ask_for_AI_level(self):
        print('? Выберите сложность игры.')
        print('[простая — 0; нормальная — 1 (default); сложная — 2]')
        print('Ввод:', end=' ')
        interface = input()
        if interface == '1' or interface == '':
            self.AI_level = AILevel.normal
        elif interface == '0':
            self.AI_level = AILevel.easy
        elif interface == '2':
            self.AI_level = AILevel.hard
        else:
            raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')

    def _ask_for_human_name(self):
        print('? Введите ваше имя.')
        print('[играть анонимно — пустое поле (default)]')
        print('Ввод:', end=' ')
        interface = input()
        if interface:
            try:
                self.human_name = str(interface)
            except TypeError:
                raise NameError(f'Неверный ввод. Получено: {interface}. Допустима строка из стандартных символов.')

    def _ask_for_human_turn(self):
        captured_count = self.game.get_captured_pieces_count()
        print(f'i Счет захватов камней: белых — {captured_count.white_count}, черных — {captured_count.black_count}.')
        print('i Текущая игровая доска:')
        print(self.game.board)
        while True and self.player_can_move:
            print(f'? Вы играете за {self.human_color}. Сделайте свой ход.')
            print('[ход по координатам (x, y) — x,y; завершить игру — пустое поле (default)]')
            print('Ввод:', end=' ')
            interface = input()
            if interface:
                if not re.fullmatch(r'\d+,\d+', interface):
                    print('! Некорректный ввод координат. Требуемый формат: x,y (например: 1,2).')
                    continue
                inputted_coords = interface.split(',')
                try:
                    if self.game.request_move(int(inputted_coords[0]), int(inputted_coords[1])).is_success:
                        break
                except IndexError as e:
                    print(e)
                    continue
            else:
                response = self.game.pass_button_pressed(pass_by_only_human=True)
                if response.end_game:
                    print(f'i Игра завершается из-за паса игрока.')
                    self.completed_game = True
                    break
                break
            print('! Туда ходить нельзя, выберите другое место.')

    def _ask_for_ai_turn(self):
        current_move = self.game.color_of_current_move
        ai_move = self.game.make_ai_move()
        print(f'i ИИ {current_move} сходил в {ai_move.x}, {ai_move.y}.')
        self.player_can_move = True


class MultiplayerCLI(CLI):
    def __init__(self):
        super().__init__()
        self.black_name: str | None = None
        self.white_name: str | None = None

    def start_multiplayer(self):
        self.game = MultiplayerGame()
        self._ask_for_black_name()
        self._ask_for_white_name()
        self.game.start_multiplayer_game(self.board_size, self.black_name, self.white_name)
        while not self.completed_game:
            self._ask_for_turn()
            if not self.completed_game:
                self._ask_for_turn()
        self.end_game()

    def _ask_for_turn(self):
        captured_count = self.game.get_captured_pieces_count()
        print(f'i Счет захватов камней: белых — {captured_count.white_count}, черных — {captured_count.black_count}.')
        print('i Текущая игровая доска:')
        print(self.game.board)
        while True:
            print(f'i Сейчас ходят {self.game.color_of_current_move}')
            print('Напишите свой ход в формате «x,y», где x и y — координаты. Для пропуска хода нажмите Enter.')
            print('Ввод:', end=' ')
            interface = input()
            if interface:
                if not re.fullmatch(r'\d+,\d+', interface):
                    print('Некорректный ввод координат! Требуемый формат: x,y (например: 1,2).')
                    continue
                inputted_coords = interface.split(',')
                try:
                    if self.game.request_move(int(inputted_coords[0]), int(inputted_coords[1])).is_success:
                        break
                except IndexError as e:
                    print(e)
                    continue
                print('Туда ходить нельзя, выберите другое место!')
            else:
                print(f'Игрок {self.game.color_of_current_move} пасанул.')
                response = self.game.pass_button_pressed()
                if response.end_game:
                    print(f'i Игра завершается из-за двух пасов подряд.')
                    self.completed_game = True
                    break
                break

    def _ask_for_black_name(self):
        print('? Введите имя игрока, который будет играть черными камнями.')
        print('[играть анонимно — пустое поле (default)]')
        print('Ввод:', end=' ')
        interface = input()
        if interface:
            try:
                self.black_name = str(interface)
            except TypeError:
                raise NameError(f'Неверный ввод. Получено: {interface}. Допустима строка из стандартных символов.')

    def _ask_for_white_name(self):
        print('? Введите имя игрока, который будет играть белыми камнями.')
        print('[играть анонимно — пустое поле (default)]')
        print('Ввод:', end=' ')
        interface = input()
        if interface:
            try:
                self.white_name = str(interface)
            except TypeError:
                raise NameError(f'Неверный ввод. Получено: {interface}. Допустима строка из стандартных символов.')


def start_cli():
    print('? Выберите режим игры.')
    print('[одиночная  — 0 (default); мультиплеерная — 1]')
    print('Ввод:', end=' ')
    interface = input()
    if interface == '0' or not interface:
        cli = SingleplayerCLI()
        cli.start_singleplayer()
    elif interface == '1':
        cli = MultiplayerCLI()
        cli.start_multiplayer()
    else:
        raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')
