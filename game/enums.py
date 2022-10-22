from enum import Enum


class Colors(Enum):
    white = 'white'
    black = 'black'

    def __str__(self):
        if self.value == 'black':
            return '■'
        return '○'

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

    def get_color(self):
        if self.value == Colors.black or self.value == Colors.white:
            return self.value
        raise ValueError('Невозможно получить цвет пустой клетки или границы поля!')

    def get_opposite_color(self):
        match self:
            case CellTypes.white:
                return CellTypes.black
            case CellTypes.black:
                return CellTypes.white
            case _:
                raise ValueError('Невозможно получить противоположный цвет пустой клетки или границы поля!')


class CellStates(Enum):
    unmarked = '-'
    marked = '+'

    def get_opposite(self):
        if self.value == 'unmarked':
            return CellStates.marked
        return CellStates.unmarked


class AILevel(Enum):
    random = 'random'
    smart = 'smart'
