import random
from game.enums import *


class AI:
    def __init__(self, board):
        self.board = board


class EasyAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self, color_of_current_move: Colors):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class NormalAI(AI):
    def __init__(self, board):
        super().__init__(board)
        self.attack_positions = []
        self.defend_positions = []

    def make_random_move(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y

    def get_random_cell(self, coords):
        if not coords:
            return self.make_random_move()
        random_group = random.choice(coords)
        if not random_group:
            return self.make_random_move()
        random_cell = random.choice(random_group)
        return random_cell.x, random_cell.y

    def get_move(self, color_of_current_move: Colors):
        self.defend_positions = self.board.get_liberties(color_of_current_move)
        self.attack_positions = self.board.get_liberties(color_of_current_move.get_opposite())
        if not self.defend_positions and not self.attack_positions:
            return self.make_random_move()
        min_amount_of_self_liberties = 4
        min_amount_of_opponent_liberties = 4
        weakest_self_coords = []
        weakest_opponent_coords = []
        for defend_coord in self.defend_positions:
            if len(defend_coord) < min_amount_of_self_liberties:
                weakest_self_coords.clear()
                weakest_self_coords.append(defend_coord)
                min_amount_of_self_liberties = len(defend_coord)
            elif len(defend_coord) == min_amount_of_self_liberties:
                weakest_self_coords.append(defend_coord)
        for attack_coord in self.attack_positions:
            if len(attack_coord) < min_amount_of_opponent_liberties:
                weakest_opponent_coords.clear()
                weakest_opponent_coords.append(attack_coord)
                min_amount_of_opponent_liberties = len(attack_coord)
            elif len(attack_coord) == min_amount_of_opponent_liberties:
                weakest_opponent_coords.append(attack_coord)
        if min_amount_of_self_liberties <= min_amount_of_opponent_liberties:
            return self.get_random_cell(weakest_self_coords)
        return self.get_random_cell(weakest_opponent_coords)


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
        else:
            x = random.randint(0, self.board.size - 1)
            y = random.randint(0, self.board.size - 1)
        return x, y
