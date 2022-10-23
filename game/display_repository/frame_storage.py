import tkinter as tk
from typing import List, Tuple
from PIL import ImageTk, Image

from .consts import *
from .element_creator import ElementCreator
from ..enums import TypesOfGames, AILevel


class FrameStorage:
    def __init__(self, window):
        self._window = window
        main_menu_bg_image = Image.open('./img/main_menu_bg.jpg')
        self._main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)

        self.menu_frame = self._create_menu_frame()
        self.leaderboard_frame = self._create_menu_frame()
        self.players_count_frame = self._create_menu_frame()
        self.game_size_frame = self._create_menu_frame()
        self.rule_frame = self._create_menu_frame()
        self.ai_frame = self._create_menu_frame()

        self.game_frame = tk.Frame(window)
        self.escape_frame = self._create_menu_frame()

        self.is_game_active = False
        self.leaderboard: List[Tuple[str, int]] = []

    def _create_menu_frame(self):
        menu_frame = tk.Frame(self._window, width=WIDTH, height=HEIGHT)
        main_menu_bg_label = tk.Label(menu_frame, image=self._main_menu_bg)
        main_menu_bg_label.place(x=0, y=0)

        menu_frame.pack_propagate(False)
        return menu_frame

    def configure_frames(self, element_creator: ElementCreator,
                         on_leaderboard_open, on_chosen_player_count, on_chosen_field_size, exit_game_by_user,
                         on_chosen_ai):

        create_label = element_creator.create_label
        create_button = element_creator.create_button

        # Main frame config
        create_label('Игра Го', self.menu_frame)
        create_button('Начать игру', self.menu_frame,
                      callback=lambda: self.change_frame(self.menu_frame, self.players_count_frame))
        create_button('Лидерборд', self.menu_frame,
                      callback=on_leaderboard_open)
        create_button('Правила игры', self.menu_frame,
                      callback=lambda: self.change_frame(self.menu_frame, self.rule_frame))
        create_button('Выход', self.menu_frame, callback=lambda: self._window.quit())

        # Frame with game type config
        create_label('Выберете режим игры', self.players_count_frame, width=20)
        create_button('С компьютером', self.players_count_frame,
                      callback=lambda: on_chosen_player_count(TypesOfGames.singleplayer))
        create_button('Два игрока', self.players_count_frame,
                      callback=lambda: on_chosen_player_count(TypesOfGames.multiplayer))
        create_button('Назад', self.players_count_frame,
                      callback=lambda: self.change_frame(self.players_count_frame, self.menu_frame))

        # Frame with field size config
        create_label('Выберете размер игрового поля', self.game_size_frame, width=20)
        create_button('9x9', self.game_size_frame, width=10, callback=lambda: on_chosen_field_size(9))
        create_button('13x13', self.game_size_frame, width=10, callback=lambda: on_chosen_field_size(13))
        create_button('19x19', self.game_size_frame, width=10, callback=lambda: on_chosen_field_size(19))
        create_button('Назад', self.game_size_frame, width=10,
                      callback=lambda: self.change_frame(self.game_size_frame, self.players_count_frame))

        # Frame with AI level config
        create_label('Выберете уровень сложности', self.ai_frame, width=20)
        create_button('Тупой', self.ai_frame, width=10, callback=lambda: on_chosen_ai(AILevel.random))
        create_button('Умный', self.ai_frame, width=10, callback=lambda: on_chosen_ai(AILevel.smart))
        create_button('Назад', self.ai_frame, width=10,
                      callback=lambda: self.change_frame(self.ai_frame, self.players_count_frame))

        # Frame with rules config
        create_label('Правила игры', self.rule_frame, width=20)

        text = ' ' * 4 + f'\n\n{" " * 4}'.join(RULES)  # O_o

        create_label(text, self.rule_frame, width=60, font=CALIBRI_SMALL_FONT, justify='left')
        create_button('Назад', self.rule_frame, width=10,
                      callback=lambda: self.change_frame(self.rule_frame, self.menu_frame))

        # Frame with leaderboard config
        if len(self.leaderboard) == 0:
            create_label('Таблица лидеров пуста', self.leaderboard_frame, width=20)
        else:
            create_label('Таблица лидеров', self.leaderboard_frame, width=20)
            for (name, score) in self.leaderboard:
                create_label(f'{name} : {score}', self.leaderboard_frame, width=30)

        create_button('Назад', self.leaderboard_frame, width=10,
                      callback=lambda: self.change_frame(self.leaderboard_frame, self.menu_frame))

        # Frame with escape items config
        self._window.bind('<Escape>', lambda e: self.change_frame(self.game_frame,
                                                                  self.escape_frame) if self.is_game_active else None)

        create_button('Продолжить игру', self.escape_frame, width=20,
                      callback=lambda: self.change_frame(self.escape_frame, self.game_frame))

        create_button('Выйти в главное меню', self.escape_frame, width=20,
                      callback=lambda: exit_game_by_user())

    @staticmethod
    def change_frame(old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack()
