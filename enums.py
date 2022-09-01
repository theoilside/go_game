from enum import Enum


class Colors(Enum):
    white = 'white'
    black = 'black'

    def get_opposite(self):
        if self.value == 'white':
            return 'black'
        return 'white'


class TypesOfGames(Enum):
    singleplayer = 'singleplayer'
    multiplayer = 'multiplayer'


class TypesOfCells(Enum):
    black = 'b'
    white = 'w'
    empty = '.'
    border = 'x'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

