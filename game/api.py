from typing import Optional, List, Tuple
from game.enums import Colors, CellTypes
from game.go import Cell


class StartGameResponse:
    def __init__(self, current_turn: Colors):
        self.current_turn: Colors = current_turn


class MakeMoveByPlayerResponse:
    def __init__(self, is_success: bool, current_turn: Colors, captured_pieces=None, error_message=None):
        self.is_success: bool = is_success
        self.current_color: Colors = current_turn
        self.error_message: Optional[str] = error_message
        self.captured_pieces: Optional[List[Cell]] = captured_pieces


class MakeMoveByAIResponse:
    def __init__(self, x: int, y: int, current_turn: Colors, captured_pieces=None):
        self.x: int = x
        self.y: int = y
        self.current_turn: Colors = current_turn
        self.captured_pieces: Optional[List[Cell]] = captured_pieces


class GetCapturedCountResponse:
    def __init__(self, white_count: int, black_count: int):
        self.white_count = white_count
        self.black_count = black_count


class GetLeaderboardResponse:
    def __init__(self, leaderboard: List[Tuple[str, int]]):
        self.leaderboard: List[Tuple[str, int]] = leaderboard


class PassButtonResponse:
    def __init__(self, current_turn: Colors, end_game: bool = False):
        self.current_turn = current_turn
        self.end_game = end_game


class FinalizedBoardResponse:
    def __init__(self, error_message=None):
        self.error_message = error_message


class RemoveCellsResponse:
    def __init__(self, removed_cells: List[Cell] = None, error_message=None):
        self.removed_cells = removed_cells
        self.error_message = error_message


class CountPointsResponse:
    def __init__(self, black_points: int, white_points: int, is_written_to_leaderboard: bool = False):
        self.black_points = black_points
        self.white_points = white_points
        self.is_written_to_leaderboard = is_written_to_leaderboard


class GetPlayerNamesResponse:
    def __init__(self, white_name, black_name):
        self.white_name = white_name
        self.black_name = black_name


class GetTypeOfCell:
    def __init__(self, cell_type: CellTypes, highlighted: bool):
        self.highlighted = highlighted
        self.cell_type = cell_type
