import random
from game.enums import *


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self, color_of_current_move: Colors):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class EasyAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self, color_of_current_move: Colors):
        return super().get_move(color_of_current_move)


class NormalAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self, color_of_current_move: Colors):
        weak_coords = self.board.get_liberties(color_of_current_move.get_opposite())
        if weak_coords:
            random_group_of_liberties = random.choice(weak_coords)
            random_liberty_cell = random.choice(random_group_of_liberties)
            x = random_liberty_cell.x - 1
            y = random_liberty_cell.y - 1
            return x, y
        return super().get_move(color_of_current_move)


class HardAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self, color_of_current_move: Colors):
        weak_coords = self.board.get_liberties(color_of_current_move.get_opposite())
        if weak_coords:
            min_amount_of_liberties = 4
            weakest_coords = []
            for weak_coord in weak_coords:
                if len(weak_coord) < min_amount_of_liberties:
                    weakest_coords.clear()
                    weakest_coords.append(weak_coord)
                    min_amount_of_liberties = len(weak_coord)
                elif len(weak_coord) == min_amount_of_liberties:
                    weakest_coords.append(weak_coord)
            random_group_of_liberties = random.choice(weakest_coords)
            random_liberty_cell = random.choice(random_group_of_liberties)
            x = random_liberty_cell.x - 1
            y = random_liberty_cell.y - 1
            return x, y
        return super().get_move(color_of_current_move)
