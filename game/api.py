from typing import Optional, List, Tuple
from game.enums import Colors
from game.go import Cell


class StartGameResponse:
    def __init__(self, current_turn: Colors):
        self.current_turn: Colors = current_turn


class MakeMoveByPlayerResponse:
    def __init__(self, is_success: bool, current_turn: Colors, captured_pieces=None, error_message=None,
                 end_game=False):
        self.is_success: bool = is_success
        self.current_color: Colors = current_turn
        self.error_message: Optional[str] = error_message
        self.captured_pieces: Optional[List[Cell]] = captured_pieces
        self.end_game: bool = end_game


class MakeMoveByAIResponse:
    def __init__(self, x: int, y: int, current_turn: Colors, captured_pieces=None, end_game=False):
        self.x: int = x
        self.y: int = y
        self.current_turn: Colors = current_turn
        self.captured_pieces: Optional[List[Cell]] = captured_pieces
        self.end_game: bool = end_game


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
