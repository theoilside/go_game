import random


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y