from enums import TypesOfGames, Colors
from Game import SingleplayerGame, MultiplayerGame


class GameSettings:
    def __init__(self):
        self.size: int = 9
        self._game_type: TypesOfGames = TypesOfGames.singleplayer
        self.current_turn_color: Colors = Colors.black
        self.game_state = SingleplayerGame()

    @property
    def game_type(self):
        return self._game_type

    @game_type.setter
    def game_type(self, value: TypesOfGames):
        self._game_type = value
        self.game_state = SingleplayerGame() if value == TypesOfGames.singleplayer else MultiplayerGame()
