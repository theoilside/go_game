import random


class AI:
    def __init__(self, board):
        self.board = board

    def get_move(self):
        pass


class RandomAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self):
        super().get_move()
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y


class SmartAI(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_move(self):
        super().get_move()
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return x, y
