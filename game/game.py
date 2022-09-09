import request_response
from game.enums import Colors
from go import Board, AI
import logging


class Game:
    def __init__(self):
        self.board = None
        self.color_of_current_move = Colors.black

    def start_new_game(self, size):
        self.board = Board(size)
        return ReqestResponse.StartGameResponse(True, Colors.black)

    def make_player_move(self, x, y):
        logging.debug(f"Запрос на постановку фигуры {self.color_of_current_move} игроком в позицию {x}-{y}")
        if self.place_piece(x, y):
            logging.debug(f"Фигура поставлена успешно")
            return ReqestResponse.MakeMoveByPlayerResponse(True, self.color_of_current_move)

        logging.debug(f"Фигура не была поставлена")
        return ReqestResponse.MakeMoveByPlayerResponse(False, self.color_of_current_move, 'Cannot make move!')

    def place_piece(self, x, y):
        logging.debug(f'Попытка поставить фишку цвета {self.color_of_current_move} в клетку {x}-{y}')
        if self.board.place_piece(self.color_of_current_move, x, y):
            self.color_of_current_move = self.color_of_current_move.get_opposite()
            logging.debug(f'Успешная попытка! Цвет текущего игрока сменился на {self.color_of_current_move}')
            return True
        logging.debug(f'Поставить фишку цвета {self.color_of_current_move} в клетку {x}-{y} не удалось')
        return False


class SingleplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.color_of_human = None
        self.color_of_AI = None
        self.AI = None

    def start_new_game(self, size, color_of_human: Colors = Colors.black):
        logging.debug(
            f"Начало одиночной игры с размером игрового поля: {size} и цветом игрока-человека {color_of_human}")
        self.color_of_human = color_of_human
        self.color_of_AI = color_of_human.get_opposite()
        response = super().start_new_game(size)
        self.AI = AI(self.board)
        return response

    def make_ai_move(self):
        logging.debug('Ход компьютера:')
        while True:
            x, y = self.AI.get_move()
            logging.debug(f'Компьютер пытается сходить в клетку {x}-{y}')
            if self.place_piece(x, y):
                break

        logging.debug(f'Компьютер сходил в клетку {x}-{y}')
        return ReqestResponse.MakeMoveByAIResponse(x, y, self.color_of_current_move)


class MultiplayerGame(Game):
    def __init__(self):
        super().__init__()

    def start_new_game(self, size):
        logging.debug(f"Начало многопользовательской игры с размером игрового поля: {size}")
        return super().start_new_game(size)
