from typing import Optional
from game.enums import Colors


class StartGameResponse:
    def __init__(self, is_success: bool, current_turn: Colors):
        self.is_success: bool = is_success
        self.current_turn: Colors = current_turn


class MakeMoveByPlayerResponse:
    def __init__(self, is_success: bool, current_turn: Colors, error_message=None, captured_pieces=None):
        self.is_success: bool = is_success
        self.current_turn: Colors = current_turn
        self.error_message: Optional[str] = error_message
        self.captured_pieces = captured_pieces


class MakeMoveByAIResponse:
    def __init__(self, x: int, y: int, current_turn: Colors, captured_pieces=None):
        self.x: int = x
        self.y: int = y
        self.current_turn: Colors = current_turn
        self.captured_pieces = captured_pieces
