from typing import Optional
import tkinter as tk

from game.enums import TypesOfGames, Colors
from game.game import SingleplayerGame, MultiplayerGame
from .consts import *
from .image_storage import ImageStorage


class GameSettings:
    def __init__(self):
        self.size: int = 9
        self._game_type: TypesOfGames = TypesOfGames.singleplayer
        self.current_color: Colors = Colors.black
        self.game_state = SingleplayerGame()
        self.info_label: Optional[tk.Label] = None
        self.field_cell = []
        self.image_storage = ImageStorage()

    @property
    def game_type(self):
        return self._game_type

    @game_type.setter
    def game_type(self, value: TypesOfGames):
        self._game_type = value
        self.game_state = SingleplayerGame() if value == TypesOfGames.singleplayer else MultiplayerGame()

    def _configure_label_multiplayer(self):
        self.info_label.configure(
            text=f'Сейчас ходит {"белый" if self.current_color == Colors.white else "чёрный"} игрок')

    def _configure_label_singleplayer(self, color_of_player: Colors):
        self.info_label.configure(text=f'Вы играете за {"белыx" if color_of_player == Colors.white else "чёрныx"}')

    def update_label(self):
        if self.game_state == TypesOfGames.multiplayer:
            self._configure_label_multiplayer()

    def init_game_state(self, game_frame, field_size, on_cell_pressed):
        white_name = tk.Label(game_frame,
                              text='Белый',
                              background='white',
                              font='Calibri 34',
                              fg='black',
                              width=10,
                              )
        white_name.grid(row=0, column=0, padx=20)

        black_name = tk.Label(game_frame,
                              text='Чёрный',
                              background='black',
                              font='Calibri 34',
                              fg='white',
                              width=10,
                              )
        black_name.grid(row=0, column=field_size + 1, padx=20)

        for x in range(1, field_size + 1):
            game_row_ceil = []
            for y in range(field_size):
                btn = tk.Label(game_frame,
                               text=' ',
                               image=self.image_storage.empty_cell,
                               borderwidth=0,
                               highlightthickness=0,
                               )
                btn.bind("<Button-1>", lambda e, a=x - 1, b=y: on_cell_pressed(a, b))

                btn.grid(row=x, column=y + 1)
                game_row_ceil.append(btn)
            self.field_cell.append(game_row_ceil)

        pass_button = tk.Button(game_frame, text='ПАСС', font='Calibri 34 bold', bg=BUTTON_COLOR,
                                activebackground=BUTTON_PRESSED_COLOR, )
        pass_button.grid(row=field_size + 3, columnspan=field_size, pady=(20, 0))

        self.info_label = tk.Label(game_frame, font='Calibri 20')
        if self.game_type == TypesOfGames.multiplayer:
            self._configure_label_multiplayer()
        else:
            self._configure_label_singleplayer(self.current_color)
