import random
from game.enums import *


class AI:
    def __init__(self, board):
        self.board = board

    def make_random_move(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class EasyAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self, color_of_current_move: Colors):
        return super().make_random_move()


class NormalAI(AI):
    def __init__(self, board):
        super().__init__(board)
        self.attack_positions = []
        self.defend_positions = []

    def get_random_cell_in_list(self, coords):
        if not coords:
            return self.make_random_move()
        random_group = random.choice(coords)
        if not random_group:
            return self.make_random_move()
        random_cell = random.choice(random_group)
        return random_cell.x - 1, random_cell.y - 1

    def get_weakest_coords(self, coords):
        min_amount_of_liberties = 4
        weakest_coords = []
        for coord in coords:
            if len(coord) < min_amount_of_liberties:
                weakest_coords.clear()
                weakest_coords.append(coord)
                min_amount_of_liberties = len(coord)
            elif len(coord) == min_amount_of_liberties:
                weakest_coords.append(coord)
        return min_amount_of_liberties, weakest_coords

    def get_move(self, color_of_current_move: Colors):
        self.defend_positions = self.board.get_liberties(color_of_current_move)
        self.attack_positions = self.board.get_liberties(color_of_current_move.get_opposite())
        if not self.defend_positions and not self.attack_positions:
            return self.make_random_move()
        min_self_liberties, weakest_self_coords = self.get_weakest_coords(self.defend_positions)
        min_opponent_liberties, weakest_opponent_coords = self.get_weakest_coords(self.attack_positions)
        if min_opponent_liberties == 1:
            return self.get_random_cell_in_list(weakest_opponent_coords)
        elif min_self_liberties <= min_opponent_liberties:
            return self.get_random_cell_in_list(weakest_self_coords)
        return self.get_random_cell_in_list(weakest_opponent_coords)


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
