from enums import *


class StartGameResponse:
    def __init__(self, is_success: bool, current_turn: Colors):
        self.is_success: bool = is_success
        self.current_turn: Colors = current_turn


class MakeMoveByPlayerResponse:
    def __init__(self, is_success: bool, current_turn: Colors):
        self.is_success: bool = is_success
        self.current_turn: Colors = current_turn


class MakeMoveByAIResponse:
    def __init__(self, x: int, y: int, current_turn: Colors):
        self.x: int = x
        self.y: int = y
        self.current_turn: Colors = current_turn
