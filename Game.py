import ReqestResponse
from enums import Colors
from go import Board, AI


class Game:
    def __init__(self):
        self.board = None
        self.color_of_current_move = Colors.black

    def start_new_game(self, size):
        self.board = Board(size)
        return ReqestResponse.StartGameResponse(True, Colors.black)

    def place_piece(self, x, y):
        self.board.place_piece(self.color_of_current_move, x, y)
        self.color_of_current_move = self.color_of_current_move.get_opposite()

    def make_player_move(self, x, y):
        self.place_piece(x, y)
        return ReqestResponse.MakeMoveByPlayerResponse(True, self.color_of_current_move)


class SingleplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.color_of_human = None
        self.color_of_AI = None
        self.AI = None

    def start_new_game(self, size, color_of_human: Colors = Colors.black):
        self.color_of_human = color_of_human
        self.color_of_AI = color_of_human.get_opposite()
        response = super().start_new_game(size)
        self.AI = AI(self.board)
        return response

    def make_ai_move(self):
        x, y = self.AI.get_move()
        self.place_piece(x, y)
        return ReqestResponse.MakeMoveByAIResponse(x, y, self.color_of_current_move)


class MultiplayerGame(Game):
    def __init__(self):
        super().__init__()

    def start_new_game(self, size):
        return super().start_new_game(size)
