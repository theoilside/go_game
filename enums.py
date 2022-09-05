from enum import Enum


class Colors(Enum):
    white = 'white'
    black = 'black'

    def get_opposite(self):
        if self.value == 'white':
            return Colors.black
        return Colors.white

    def get_type_of_cells(self):
        match self:
            case Colors.black:
                return TypesOfCells.black
            case Colors.white:
                return TypesOfCells.white


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
