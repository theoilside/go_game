import tkinter as tk
from typing import List, Tuple, Optional
from PIL import ImageTk, Image

from .consts import *
from .element_creator import ElementCreator
from ..enums import TypesOfGames, AILevel, Colors


class FrameStorage:
    def __init__(self, window):
        self._window = window
        main_menu_bg_image = Image.open('./img/main_menu_bg.jpg')
        self._main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)
        self.element_creator = ElementCreator()

        self.menu_frame = self._create_menu_frame()
        self.leaderboard_frame = self._create_menu_frame()
        self.players_count_frame = self._create_menu_frame()
        self.game_size_frame = self._create_menu_frame()
        self.rule_frame = self._create_menu_frame()
        self.ai_frame = self._create_menu_frame()
        self.color_frame = self._create_menu_frame()

        self.game_frame = tk.Frame(window)
        self.escape_frame = self._create_menu_frame()

        self.is_game_active = False
        self.leaderboard: List[Tuple[str, int]] = []

        self.leaderboard_title: Optional[tk.Label] = None

    def _create_menu_frame(self):
        menu_frame = tk.Frame(self._window, width=WIDTH, height=HEIGHT)
        main_menu_bg_label = tk.Label(menu_frame, image=self._main_menu_bg)
        main_menu_bg_label.place(x=0, y=0)

        menu_frame.pack_propagate(False)
        return menu_frame

    def configure_frames(self, on_leaderboard_open, on_chosen_player_count, on_chosen_field_size, exit_game_by_user,
                         on_chosen_ai, on_chosen_color):

        create_label = self.element_creator.create_label
        create_button = self.element_creator.create_button

        # Main frame config
        create_label('Го (囲碁)', self.menu_frame)
        create_button('Начать игру', self.menu_frame,
                      callback=lambda: self.change_frame(self.menu_frame, self.players_count_frame))
        create_button('Лидерборд', self.menu_frame,
                      callback=on_leaderboard_open)
        create_button('Правила игры', self.menu_frame,
                      callback=lambda: self.change_frame(self.menu_frame, self.rule_frame))
        create_button('Выход', self.menu_frame, callback=lambda: self._window.quit())

        # Frame with game type config
        create_label('Выберите режим игры', self.players_count_frame, width=20)
        create_button('С компьютером', self.players_count_frame,
                      callback=lambda: on_chosen_player_count(TypesOfGames.singleplayer))
        create_button('Два игрока', self.players_count_frame,
                      callback=lambda: on_chosen_player_count(TypesOfGames.multiplayer))
        create_button('← Назад', self.players_count_frame,
                      callback=lambda: self.change_frame(self.players_count_frame, self.menu_frame))

        # Frame with field size config
        create_label('Выберите размер игрового поля', self.game_size_frame, width=20)
        create_button('9x9', self.game_size_frame, width=10, callback=lambda: on_chosen_field_size(9))
        create_button('13x13', self.game_size_frame, width=10, callback=lambda: on_chosen_field_size(13))
        create_button('19x19', self.game_size_frame, width=10, callback=lambda: on_chosen_field_size(19))
        create_button('← Назад', self.game_size_frame, width=10,
                      callback=lambda: self.change_frame(self.game_size_frame, self.players_count_frame))

        # Frame with AI level config
        create_label('Выберите уровень сложности', self.ai_frame, width=20)
        create_button('Простой', self.ai_frame, width=15, callback=lambda: on_chosen_ai(AILevel.easy))
        create_button('Нормальный', self.ai_frame, width=15, callback=lambda: on_chosen_ai(AILevel.normal))
        create_button('Сложный', self.ai_frame, width=15, callback=lambda: on_chosen_ai(AILevel.hard))
        create_button('← Назад', self.ai_frame, width=10,
                      callback=lambda: self.change_frame(self.ai_frame, self.players_count_frame))

        # Frame with colors config
        create_label('Выберите ваш цвет', self.color_frame, width=20)
        create_button('Черный', self.color_frame, width=10, callback=lambda: on_chosen_color(Colors.black))
        create_button('Белый', self.color_frame, width=10, callback=lambda: on_chosen_color(Colors.white))
        create_button('← Назад', self.color_frame, width=10,
                      callback=lambda: self.change_frame(self.color_frame, self.ai_frame))

        # Frame with rules config
        create_label('Правила игры', self.rule_frame, width=20)

        text = ' ' * 4 + f'\n\n{" " * 4}'.join(RULES)  # O_o Если писать \t, получается что-то некрасивое

        create_label(text, self.rule_frame, width=60, font=CALIBRI_SMALL_FONT, justify='left')
        create_button('← Назад', self.rule_frame, width=10,
                      callback=lambda: self.change_frame(self.rule_frame, self.menu_frame))

        # Frame with leaderboard config
        create_label('Таблица лидеров', self.leaderboard_frame, width=20)
        self.leaderboard_title = create_label('Здесь ничего нет :(', self.leaderboard_frame, width=30)
        create_button('← Назад', self.leaderboard_frame, width=10,
                      callback=lambda: self.change_frame(self.leaderboard_frame, self.menu_frame))

        # Frame with escape items config
        self._window.bind('<Escape>', lambda e: self.change_frame(self.game_frame,
                                                                  self.escape_frame) if self.is_game_active else None)

        create_button('Продолжить игру', self.escape_frame, width=20,
                      callback=lambda: self.change_frame(self.escape_frame, self.game_frame))

        create_button('← Выйти в главное меню', self.escape_frame, width=20,
                      callback=lambda: exit_game_by_user(self.escape_frame))

    @staticmethod
    def change_frame(old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack()

    def configure_leaderboard(self):
        if len(self.leaderboard) == 0:
            self.leaderboard_title.configure(text='Здесь ничего нет')
            return

        score_message = ''
        for (name, score) in self.leaderboard:
            score_message += f'{name} : {score}\n'

        self.leaderboard_title.configure(text=score_message)
