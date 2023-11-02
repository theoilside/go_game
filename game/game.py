import datetime
import logging
from collections import namedtuple

from .ai import EasyAI, HardAI, NormalAI
from .api_responses import *
from .database import DatabaseAPI
from .enums import AILevel, CellStates, CellTypes, Colors
from .go import Board, FinalizedBoard

KOMI = 6.5


class Game:
    def __init__(self):
        self.board: Board | FinalizedBoard | None = None
        self.color_of_current_move: Colors = Colors.black
        self.black_name: str = 'Черные'
        self.white_name: str = 'Белые'
        self.is_passed_last_turn: bool = False
        self._captured_black: int = 0
        self._captured_white: int = 0
        self.black_points: int = 0
        self.white_points: int = 0

    def start_game(self, size: int, black_name: str | None, white_name: str | None) -> StartGameResponse:
        self.board = Board(size)
        if black_name:
            self.black_name = black_name
        if white_name:
            self.white_name = white_name
        return StartGameResponse(Colors.black)

    def request_move(self, x: int, y: int) -> MakeMoveByPlayerResponse:
        logging.debug(f"Запрос на постановку фигуры {self.color_of_current_move} игроком в позицию {x}-{y}")
        result_of_request = self._place_piece(x, y)
        if result_of_request.is_permitted_move:
            logging.debug(f"Фигура поставлена успешно")
            return MakeMoveByPlayerResponse(True, self.color_of_current_move, result_of_request.captured)
        logging.debug(f"Фигура не была поставлена")
        return MakeMoveByPlayerResponse(False, self.color_of_current_move)

    def _place_piece(self, x, y):
        Response = namedtuple('Response', ('is_permitted_move', 'captured'), defaults=(False, None))
        logging.debug(f'Попытка поставить фишку цвета {self.color_of_current_move} в клетку {x}-{y}')
        response = self.board.place_piece(self.color_of_current_move, x, y)
        if response.is_permitted_move:
            self.color_of_current_move = self.color_of_current_move.get_opposite()
            self._update_overall_captured(response.captured)
            logging.debug(f'Успешная попытка! Цвет текущего игрока сменился на {self.color_of_current_move}')
            return Response(True, response.captured)
        logging.debug(f'Поставить фишку цвета {self.color_of_current_move} в клетку {x}-{y} не удалось')
        return Response(False, None)

    def pass_button_pressed(self, pass_by_only_human: bool = False) -> PassButtonResponse:
        self.color_of_current_move = self.color_of_current_move.get_opposite()
        # Вызывается, когда пользователь нажал кнопку ПАС
        if self.is_passed_last_turn or pass_by_only_human:
            self.finalize_board()
            return PassButtonResponse(self.color_of_current_move, True)
        self.is_passed_last_turn = True
        return PassButtonResponse(self.color_of_current_move)

    def get_captured_pieces_count(self) -> GetCapturedCountResponse:
        return GetCapturedCountResponse(self._captured_white, self._captured_black)

    @staticmethod
    def get_leaderboard() -> GetLeaderboardResponse:
        db_api = DatabaseAPI()
        leaderboard = db_api.get_from_table()
        return GetLeaderboardResponse(leaderboard)

    @staticmethod
    def clear_leaderboard():
        db_api = DatabaseAPI()
        db_api.delete_from_table()

    def _update_overall_captured(self, new_captured):
        if new_captured:
            white_captured = new_captured[0].type.name == 'white'
            amount_of_captured = 0
            for i in range(len(new_captured)):
                amount_of_captured += 1
            amount_of_captured **= 1 / 2
            if white_captured:
                self._captured_white += int(amount_of_captured)
            else:
                self._captured_black += int(amount_of_captured)

    def finalize_board(self) -> FinalizedBoardResponse:
        self.board = FinalizedBoard(self.board)
        return FinalizedBoardResponse()

    def mark_dead_cell(self, x, y) -> MarkDeadResponse:
        cell = self.board.mark_cell(x + 1, y + 1)
        return MarkDeadResponse(cell.type, cell.state != CellStates.marked)

    def remove_pieces_at_coords(self) -> RemoveCellsResponse:
        self.board.mark_dead_cells()
        for cell in self.board.dead_cells:
            self.board.update_cell(cell, CellTypes.empty, CellStates.unmarked)
        return RemoveCellsResponse(self.board.dead_cells)

    def count_points(self, black_territory: int = None, white_territory: int = None) -> CountPointsResponse:
        # Необязательные аргументы: заранее введенные площади черных/белых.
        if black_territory and white_territory:
            self.black_points = max(black_territory - self._captured_black, 0)
            self.white_points = max(white_territory - self._captured_white + KOMI, 0)
        else:
            self.black_points = max(self.board.count_territory(Colors.black) - self._captured_black, 0)
            self.white_points = max(self.board.count_territory(Colors.white) - self._captured_white + KOMI, 0)
        self.add_score_to_leaderboard(self.black_points, self.white_points)
        return CountPointsResponse(self.black_points, self.white_points, True)

    def add_score_to_leaderboard(self, black_score: int, white_score: int) -> None:
        db_api = DatabaseAPI()
        if self.black_name == 'Черные' and self.white_name != 'Белые':
            db_api.add_new_result(self.white_name, white_score)
            # self.black_name = f'Черные {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
        elif self.black_name != 'Черные' and self.white_name == 'Белые':
            db_api.add_new_result(self.black_name, black_score)
            # self.white_name = f'Белые {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
        elif self.black_name != 'Черные' and self.white_name != 'Белые':
            db_api.add_new_result(self.black_name, black_score)
            db_api.add_new_result(self.white_name, white_score)
        elif self.black_name == 'Черные' and self.white_name == 'Белые':
            return

    def get_player_names(self) -> GetPlayerNamesResponse:
        return GetPlayerNamesResponse(self.white_name, self.black_name)


class SingleplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.color_of_human: Optional[Colors] = None
        self.color_of_AI: Optional[Colors] = None
        self.AI: Optional[EasyAI | NormalAI | HardAI] = None

    def start_singleplayer_game(self, size, human_name: str | None, color_of_human: Colors = Colors.black,
                                ai_level: AILevel = AILevel.normal):
        if not human_name:
            logging.debug(f"Начало одиночной игры с размером игрового поля {size}, цветом {color_of_human} "
                          f"игрока-человека без имени и уровнем ИИ {ai_level}")
            black_name = 'Черные'
            white_name = 'Белые'
        else:
            logging.debug(f"Начало одиночной игры с размером игрового поля {size}, цветом {color_of_human} "
                          f"игрока-человека под именем {human_name} и уровнем ИИ {ai_level}")
            if color_of_human == Colors.black:
                black_name = human_name
                white_name = 'Белые'
            else:
                black_name = 'Черные'
                white_name = human_name
        self.color_of_human = color_of_human
        self.color_of_AI = color_of_human.get_opposite()
        response = super().start_game(size, black_name, white_name)
        match ai_level:
            case AILevel.hard:
                self.AI = HardAI(self.board)
            case AILevel.easy:
                self.AI = EasyAI(self.board)
            case _:
                self.AI = NormalAI(self.board)
        return response

    def make_ai_move(self):
        logging.debug('Ход компьютера:')
        attempts_counter = 0
        while True:
            attempts_counter += 1
            if attempts_counter < 5:
                x, y = self.AI.get_move(self.color_of_current_move)
                logging.debug(f'Компьютер пытается сходить в выгодную клетку {x}-{y}')
            else:
                x, y = self.AI.make_random_move()
                logging.debug(f'Компьютер пытается сходить в случайную клетку {x}-{y}')
            result = self._place_piece(x, y)
            if result.is_permitted_move:
                self.is_passed_last_turn = False
                logging.debug(f'Компьютер сходил в клетку {x}-{y}')
                return MakeMoveByAIResponse(x, y, self.color_of_current_move, result.captured)


class MultiplayerGame(Game):
    def __init__(self):
        super().__init__()

    def start_multiplayer_game(self, size: int, black_name: str | None = None, white_name: str | None = None):
        logging.debug(f"Начало многопользовательской игры с размером игрового поля: {size}")
        return super().start_game(size, black_name, white_name)
