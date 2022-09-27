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
                return CellTypes.black
            case Colors.white:
                return CellTypes.white


class TypesOfGames(Enum):
    singleplayer = 'singleplayer'
    multiplayer = 'multiplayer'


class CellTypes(Enum):
    black = Colors.black
    white = Colors.white
    empty = '·'
    border = 'x'

    def __str__(self):
        if self.value == Colors.black:
            return '■'
        if self.value == Colors.white:
            return '○'
        return self.value


class CellStates(Enum):
    unmarked = '-'
    marked = '+'

    def get_opposite(self):
        if self.value == 'unmarked':
            return CellStates.marked
        return CellStates.unmarked
