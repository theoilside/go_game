from typing import Optional, List
import tkinter as tk

from game.enums import TypesOfGames, Colors, AILevel, CellTypes
from game.game import SingleplayerGame, MultiplayerGame
from .consts import *
from .image_storage import ImageStorage
from ..api import MakeMoveByAIResponse
from ..go import Cell


class GameSettings:
    def __init__(self):
        self.size: int = 9
        self._game_type: TypesOfGames = TypesOfGames.singleplayer
        self.ai_level: AILevel = AILevel.hard
        self.singleplayer_color: Colors = Colors.black

        self.current_color: Colors = Colors.black
        self.game_api: Optional[SingleplayerGame | MultiplayerGame] = None
        self.info_label: Optional[tk.Label] = None
        self.error_label: Optional[tk.Label] = None
        self.field_cell: List[List[tk.Label]] = []

        self.white_score: Optional[tk.Label] = None
        self.black_score: Optional[tk.Label] = None

        self.white_name: Optional[tk.Label] = None
        self.black_name: Optional[tk.Label] = None

        self.white_pass: Optional[tk.Button] = None
        self.black_pass: Optional[tk.Button] = None

        self.confirm_button: Optional[tk.Button] = None

        self._image_storage = ImageStorage()

    @property
    def game_type(self):
        return self._game_type

    @game_type.setter
    def game_type(self, game_type: TypesOfGames):
        self._game_type = game_type
        self.game_api = SingleplayerGame() if game_type == TypesOfGames.singleplayer else MultiplayerGame()

    def _configure_label_multiplayer(self):
        self.info_label.configure(
            text=f'Сейчас ходит {"белый" if self.current_color == Colors.white else "черный"} игрок')

    def _configure_label_singleplayer(self, color_of_player: Colors):
        self.info_label.configure(text=f'Вы играете за {"белыx" if color_of_player == Colors.white else "черныx"}')

    def update_info_label(self):
        if self._game_type == TypesOfGames.multiplayer:
            self._configure_label_multiplayer()

    def update_error_label(self, is_error: bool):
        self.error_label.configure(text='Такой ход сделать нельзя!' if is_error else '')

    def init_game_state(self, game_frame, on_cell_pressed, on_pass_button_pressed, on_confirm_button):
        for x in range(self.size):
            game_row_ceil = []
            for y in range(self.size):
                btn = tk.Label(game_frame,
                               text=' ',
                               image=self._image_storage.empty_cell,
                               borderwidth=0,
                               highlightthickness=0,
                               )
                btn.bind("<Button-1>", lambda e, a=x, b=y: on_cell_pressed(a, b))

                btn.grid(row=x + 1, column=y + 6)
                game_row_ceil.append(btn)
            self.field_cell.append(game_row_ceil)

        self._create_black_state(game_frame, on_pass_button_pressed)
        self._create_white_state(game_frame, on_pass_button_pressed)
        self.update_score(0, 0)

        self.info_label = tk.Label(game_frame, font='Calibri 20')
        if self.game_type == TypesOfGames.multiplayer:
            self._configure_label_multiplayer()
        else:
            self._configure_label_singleplayer(self.singleplayer_color)

        self.info_label.grid(row=0, column=6, columnspan=self.size)

        self.error_label = tk.Label(game_frame, font='Calibri 20')
        self.error_label.grid(row=self.size + 1, column=6, columnspan=self.size)

        self.confirm_button = tk.Button(game_frame, font='Calibri 20', text='Подтвердить выбор', bg=BUTTON_COLOR,
                                        activebackground=BUTTON_PRESSED_COLOR,
                                        highlightbackground=BUTTON_COLOR,  # For Mac OS
                                        command=on_confirm_button
                                        )

    def _create_white_state(self, game_frame, on_pass_button_pressed):
        name = tk.Label(game_frame,
                        text='Белые',
                        background='white',
                        font='Calibri 34',
                        fg='black',
                        borderwidth=0,
                        highlightthickness=0,
                        )
        name.grid(row=0, column=0, padx=20)
        self.white_name = name

        score = tk.Label(game_frame,
                         background='white',
                         font='Calibri 28',
                         fg='black',
                         borderwidth=0,
                         highlightthickness=0,
                         )
        score.grid(row=1, column=0, padx=20, rowspan=2)
        self.white_score = score

        pass_button = tk.Button(game_frame, text='ПАС', font='Calibri 34 bold', bg='white',
                                activebackground=BUTTON_PRESSED_COLOR, fg='black',
                                highlightbackground='white',  # For Mac OS
                                command=on_pass_button_pressed)
        self.white_pass = pass_button

        pass_button.grid(row=3, column=0, padx=20, rowspan=3)

    def _create_black_state(self, game_frame, on_pass_button_pressed):
        name = tk.Label(game_frame,
                        text='Черные',
                        background='black',
                        font='Calibri 34',
                        fg='white',
                        borderwidth=0,
                        highlightthickness=0,
                        )
        name.grid(row=0, column=self.size + 6, padx=20)

        self.black_name = name
        score = tk.Label(game_frame,
                         background='black',
                         font='Calibri 28',
                         fg='white',
                         borderwidth=0,
                         highlightthickness=0,
                         )
        score.grid(row=1, column=self.size + 6, padx=20, rowspan=2)
        self.black_score = score

        pass_button = tk.Button(game_frame, text='ПАС', font='Calibri 34 bold', bg='black',
                                activebackground=BUTTON_PRESSED_COLOR, fg='white',
                                highlightbackground='black',  # For Mac OS
                                command=on_pass_button_pressed)
        self.black_pass = pass_button

        pass_button.grid(row=3, column=self.size + 6, padx=20, rowspan=3)

    def update_score(self, for_white: int, for_black: int):
        self.white_score.configure(text=f'Захвачено:\n{for_black}')
        self.black_score.configure(text=f'Захвачено:\n{for_white}')

    def configure_names(self, white: str, black: str):
        self.white_name.configure(text=white)
        self.black_name.configure(text=black)

    def change_pass_buttons(self):
        if self.current_color == Colors.black:
            self.white_pass.configure(state=tk.DISABLED)
            self.black_pass.configure(state=tk.NORMAL)
        else:
            self.white_pass.configure(state=tk.NORMAL)
            self.black_pass.configure(state=tk.DISABLED)

    def disable_pass_button(self):
        self.white_pass.configure(state=tk.DISABLED)
        self.black_pass.configure(state=tk.DISABLED)

    def grid_confirm_button(self):
        self.confirm_button.grid(row=self.size + 2, column=6, columnspan=self.size)

    def do_ai_move(self):
        make_move_by_ai_response: MakeMoveByAIResponse = self.game_api.make_ai_move()
        self.clear_captured_pieces(make_move_by_ai_response.captured_pieces)
        self._image_storage.change_cell_image(self.current_color.get_type_of_cells(),
                                              self.field_cell[make_move_by_ai_response.y][
                                                  make_move_by_ai_response.x])

        self.current_color = make_move_by_ai_response.current_turn

    def clear_captured_pieces(self, captured_pieces: List[Cell]):
        for captured_cell in captured_pieces:
            self._image_storage.change_cell_image(CellTypes.empty,
                                                  self.field_cell[captured_cell.y - 1][
                                                      captured_cell.x - 1])
