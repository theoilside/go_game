from collections import namedtuple
from .api import *
from .enums import Colors, CellStates, CellTypes, AILevel
from .go import Board, FinalizedBoard
from .ai import RandomAI, SmartAI
from .database import DatabaseAPI
import logging

KOMI = 6.5


# TODO: Rewrite with decorator
class Game:
    def __init__(self):
        self.board = None
        self.color_of_current_move = Colors.black
        self.black_name = 'Черные'
        self.white_name = 'Белые'
        self.is_passed_last_turn: bool = False
        self._captured_black = 0
        self._captured_white = 0
        self.black_points = 0
        self.white_points = 0

        self._dead_cells = []

    def start_game(self, size: int, black_name: str | None, white_name: str | None) -> StartGameResponse:
        self.board = Board(size)
        if black_name:
            self.black_name = black_name
        if white_name:
            self.white_name = white_name
        return StartGameResponse(Colors.black)

    def make_player_move(self, x, y):
        logging.debug(f"Запрос на постановку фигуры {self.color_of_current_move} игроком в позицию {x}-{y}")
        response = self.place_piece(x, y)
        if response.is_success:
            self.is_passed_last_turn = False
            logging.debug(f"Фигура поставлена успешно")
            return MakeMoveByPlayerResponse(True, self.color_of_current_move, response.captured_pieces)
        logging.debug(f"Фигура не была поставлена")
        return MakeMoveByPlayerResponse(False, self.color_of_current_move, 'Cannot make move!')

    def place_piece(self, x, y):
        result = self._place_piece(x, y)
        if result.is_permitted_move:
            logging.debug(f"Фигура поставлена успешно")
            return MakeMoveByPlayerResponse(True, self.color_of_current_move, result.captured)
        logging.debug(f"Фигура не была поставлена")
        return MakeMoveByPlayerResponse(False, self.color_of_current_move, 'Cannot make move!')

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

    def put_dead_cell(self, x, y):
        cell: Cell = self.board.get_cell(x+1, y+1)
        if cell.type == CellTypes.white or cell.type == CellTypes.black:
            cell.check_dead()
        return GetTypeOfCell(cell.type, not cell.dead)

    @staticmethod
    def get_leaderboard() -> GetLeaderboardResponse:
        db_api = DatabaseAPI()
        leaderboard = db_api.get_from_table()
        return GetLeaderboardResponse(leaderboard)

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

    def remove_pieces_at_coords(self):
        removed_cells = []
        for _ in self.board.board:
            for cell in _:
                if cell.dead:
                    removed_cells.append(cell)
                    self.board.update_cell(cell, CellTypes.empty, CellStates.unmarked)
        return RemoveCellsResponse(removed_cells)

    def finalize_board(self) -> FinalizedBoardResponse:
        self.board = FinalizedBoard(self.board)
        return FinalizedBoardResponse()

    def count_points(self, black_territory: int = None, white_territory: int = None) -> CountPointsResponse:
        # Необязательные аргументы: заранее введенные площади черных/белых.
        if black_territory and white_territory:
            self.black_points = black_territory - self._captured_black
            self.white_points = white_territory - self._captured_white + KOMI
        else:
            self.black_points = self.board.count_territory(Colors.black) - self._captured_black
            self.white_points = self.board.count_territory(Colors.white) - self._captured_white + KOMI
        return CountPointsResponse(self.black_points, self.white_points)

    def add_score_to_leaderboard(self):
        # TODO: Реализовать метод
        # Добавляет результат метода get_score в бд лидерборда.
        ...

    def get_player_names(self) -> GetPlayerNamesResponse:
        return GetPlayerNamesResponse(self.white_name, self.black_name)


class SingleplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.color_of_human: Optional[Colors] = None
        self.color_of_AI: Optional[Colors] = None
        self.AI: Optional[SmartAI | RandomAI] = None

    def start_singleplayer_game(self, size, human_name: str | None, color_of_human: Colors = Colors.black,
                                ai_level: AILevel = AILevel.smart):
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

        if ai_level == AILevel.smart:
            self.AI = SmartAI(self.board)
        else:
            self.AI = RandomAI(self.board)

        return response

    def make_ai_move(self):
        logging.debug('Ход компьютера:')
        while True:
            x, y = self.AI.get_move()
            logging.debug(f'Компьютер пытается сходить в клетку {x}-{y}')
            result = self._place_piece(x, y)
            if result.is_permitted_move:
                self.is_passed_last_turn = False
                captured = result.captured
                break
        logging.debug(f'Компьютер сходил в клетку {x}-{y}')
        return MakeMoveByAIResponse(x, y, self.color_of_current_move, captured)


class MultiplayerGame(Game):
    def __init__(self):
        super().__init__()

    def start_multiplayer_game(self, size: int, black_name: str | None = None, white_name: str | None = None):
        logging.debug(f"Начало многопользовательской игры с размером игрового поля: {size}")
        return super().start_game(size, black_name, white_name)
