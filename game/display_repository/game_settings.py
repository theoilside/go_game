from typing import Optional, List
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
        self.field_cell: List[List[tk.Label]] = []

        self._image_storage = ImageStorage()
        self._cell_height: int = 0

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

    def init_game_state(self, game_frame, on_cell_pressed):
        for x in range(self.size):
            game_row_ceil = []
            for y in range(self.size):
                btn = tk.Label(game_frame,
                               text=' ',
                               image=self._image_storage.empty_cell,
                               borderwidth=0,
                               highlightthickness=0,
                               # width=50,
                               # height=50,
                               )
                btn.bind("<Button-1>", lambda e, a=x, b=y: on_cell_pressed(a, b))

                btn.grid(row=x + 1, column=y + 6)
                game_row_ceil.append(btn)
            self.field_cell.append(game_row_ceil)

        self._cell_height = self.field_cell[0][0].winfo_height()
        self.create_white_state(game_frame)
        self.create_black_state(game_frame)

        pass_button = tk.Button(game_frame, text='ПАСС', font='Calibri 34 bold', bg=BUTTON_COLOR,
                                activebackground=BUTTON_PRESSED_COLOR, )
        # pass_button.grid(row=field_size + 3, columnspan=field_size, pady=(20, 0))

        self.info_label = tk.Label(game_frame, font='Calibri 20')
        if self.game_type == TypesOfGames.multiplayer:
            self._configure_label_multiplayer()
        else:
            self._configure_label_singleplayer(self.current_color)

        self.info_label.grid(row=0, column=6, columnspan=self.size)

    def create_white_state(self, game_frame):
        name = tk.Label(game_frame,
                        text='Белый',
                        background='white',
                        font='Calibri 34',
                        fg='black',
                        borderwidth=0,
                        highlightthickness=0,
                        )
        name.grid(row=0, column=0, padx=20)

        score = tk.Label(game_frame,
                         text='Количество\nзахватов: 0',
                         background='white',
                         font='Calibri 28',
                         fg='black',
                         borderwidth=0,
                         highlightthickness=0,
                         )
        score.grid(row=1, column=0, padx=20, rowspan=2)

        pass_button = tk.Button(game_frame, text='ПАСС', font='Calibri 34 bold', bg='white',
                                activebackground=BUTTON_PRESSED_COLOR, fg='black')
        pass_button.grid(row=3, column=0, padx=20, rowspan=3)

    def create_black_state(self, game_frame):
        name = tk.Label(game_frame,
                        text='Чёрный',
                        background='black',
                        font='Calibri 34',
                        fg='white',
                        borderwidth=0,
                        highlightthickness=0,
                        )
        name.grid(row=0, column=self.size + 6, padx=20)

        score = tk.Label(game_frame,
                         text='Количество\nзахватов: 0',
                         background='black',
                         font='Calibri 28',
                         fg='white',
                         borderwidth=0,
                         highlightthickness=0,
                         )
        score.grid(row=1, column=self.size + 6, padx=20, rowspan=2)

        pass_button = tk.Button(game_frame, text='ПАСС', font='Calibri 34 bold', bg='black',
                                activebackground=BUTTON_PRESSED_COLOR, fg='white')
        pass_button.grid(row=3, column=self.size + 6, padx=20, rowspan=3)
