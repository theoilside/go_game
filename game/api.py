from typing import Optional, List
from game.enums import Colors
from game.go import Cell


class StartGameResponse:
    def __init__(self, current_turn: Colors):
        self.current_turn: Colors = current_turn


class MakeMoveByPlayerResponse:
    def __init__(self, is_success: bool, current_turn: Colors, captured_pieces=None, error_message=None):
        self.is_success: bool = is_success
        self.current_color: Colors = current_turn
        self.error_message: Optional[str] = error_message
        self.captured_pieces: Optional[List[List[Cell]]] = captured_pieces


class MakeMoveByAIResponse:
    def __init__(self, x: int, y: int, current_turn: Colors, captured_pieces=None):
        self.x: int = x
        self.y: int = y
        self.current_turn: Colors = current_turn
        self.captured_pieces = captured_pieces
