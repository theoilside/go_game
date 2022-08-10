class Board:
    def __init__(self, size):
        self.size = size


class Object:
    types = {
        'black': '#',
        'white': 'o',
        'empty': '.',
        'void': 'x'
    }

    def __init__(self, type):
        if type not in self.types:
            raise ('Неверно указан тип объекта! Возможные значения: {0}'.format(self.types.keys))
        self.type = type