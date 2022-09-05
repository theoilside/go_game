from typing import Optional

from enums import TypesOfGames, Colors
from Game import SingleplayerGame, MultiplayerGame

import tkinter as tk


class GameSettings:
    def __init__(self):
        self.size: int = 9
        self._game_type: TypesOfGames = TypesOfGames.singleplayer
        self.current_turn_color: Colors = Colors.black
        self.game_state = SingleplayerGame()
        self.info_label: Optional[tk.Label] = None

    @property
    def game_type(self):
        return self._game_type

    @game_type.setter
    def game_type(self, value: TypesOfGames):
        self._game_type = value
        self.game_state = SingleplayerGame() if value == TypesOfGames.singleplayer else MultiplayerGame()

    def configure_label_multiplayer(self):
        self.info_label.configure(
            text=f'Сейчас ходит {"белый" if self.current_turn_color == Colors.white else "чёрный"} игрок')

    def configure_label_singleplayer(self, color_of_player: Colors):
        self.info_label.configure(text=f'Вы играете за {"белыx" if color_of_player == Colors.white else "чёрныx"}')

    def configure_label(self):
        if self.game_state == TypesOfGames.multiplayer:
            self.configure_label_multiplayer()
