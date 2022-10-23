import tkinter as tk
from tkinter.simpledialog import askstring

from .display_repository.element_creator import ElementCreator
from .display_repository.game_settings import GameSettings
from .display_repository.image_storage import ImageStorage
from .api import *
from .enums import CellTypes, AILevel
from .go import TypesOfGames
from .display_repository.consts import *
from .display_repository.frame_storage import FrameStorage


class Display:
    def __init__(self, window):
        self.window = window

        self.game_settings = GameSettings()
        self.frame_storage = FrameStorage(window)
        self.image_storage = ImageStorage()
        self.element_creator = ElementCreator()

        window.geometry(f'{WIDTH}x{HEIGHT}')
        window.title('Игра "Го"')
        window.iconbitmap(ICON_PATH)

        self.create_frames()

    def create_frames(self):
        self.frame_storage.configure_frames(self.element_creator, self.on_leaderboard_open, self.on_chosen_player_count,
                                            self.on_chosen_field_size, self.on_exit_game_by_user, self.on_chosen_ai)
        self.frame_storage.menu_frame.pack()

    def on_leaderboard_open(self):
        self.frame_storage.leaderboard = self.game_settings.game_api.get_leaderboard().leaderboard
        self.frame_storage.change_frame(self.frame_storage.menu_frame,
                                        self.frame_storage.leaderboard_frame)

    def on_chosen_player_count(self, game_type: TypesOfGames):
        self.game_settings.game_type = game_type
        if game_type == TypesOfGames.singleplayer:
            self.frame_storage.change_frame(self.frame_storage.players_count_frame, self.frame_storage.ai_frame)
        else:
            self.frame_storage.change_frame(self.frame_storage.players_count_frame, self.frame_storage.game_size_frame)

    def on_chosen_ai(self, ai_level: AILevel):
        self.game_settings.ai_level = ai_level
        self.frame_storage.change_frame(self.frame_storage.ai_frame, self.frame_storage.game_size_frame)

    def on_chosen_field_size(self, size):
        self.game_settings.size = size

        self.init_game_field()
        self.frame_storage.change_frame(self.frame_storage.game_size_frame, self.frame_storage.game_frame)
        self.frame_storage.is_game_active = True

        if self.game_settings.game_type == TypesOfGames.singleplayer:
            start_response = self.config_singleplayer()
        else:
            start_response = self.config_multiplayer()

        names_response = self.game_settings.game_api.get_player_names()
        self.game_settings.configure_names(names_response.white_name, names_response.black_name)

        self.game_settings.current_color = start_response.current_turn
        self.game_settings.configure_pass_buttons()

    def config_singleplayer(self) -> StartGameResponse:
        name = askstring('Имя', 'Как тебя зовут?')
        start_response = self.game_settings.game_api.start_singleplayer_game(self.game_settings.size, name,
                                                                             ai_level=self.game_settings.ai_level)
        return start_response

    def config_multiplayer(self) -> StartGameResponse:
        white_name = askstring('Белый', 'Как зовут белого игрока?')
        black_name = askstring('Чёрный', 'Как зовут чёрного игрока?')
        start_response = self.game_settings.game_api \
            .start_multiplayer_game(self.game_settings.size, black_name, white_name)
        return start_response

    def on_exit_game_by_user(self):
        old_frame = self.frame_storage.escape_frame
        self.game_settings = GameSettings()
        self.frame_storage = FrameStorage(self.window)
        self.create_frames()
        self.frame_storage.change_frame(old_frame, self.frame_storage.menu_frame)
        self.frame_storage.is_game_active = False

    def init_game_field(self):
        self.game_settings.init_game_state(self.frame_storage.game_frame, self.on_game_cell_pressed)

        return self.game_settings.field_cell

    def on_game_cell_pressed(self, row, column):
        # TODO: Вынести обработку нажатой клетки в отдельный модуль
        make_move_player_response: MakeMoveByPlayerResponse = \
            self.game_settings.game_api.make_player_move(x=column, y=row)

        # Если ход сделать нельзя, вывести ошибку
        if not make_move_player_response.is_success:
            self.game_settings.update_error_label(is_error=True)
            return
        self.game_settings.update_error_label(is_error=False)

        # Убрать с поля все захваченные фигуры
        self.clear_captured_pieces(make_move_player_response.captured_pieces)

        self.image_storage.change_ceil_image(
            self.game_settings.current_color.get_type_of_cells(), self.game_settings.field_cell[row][column])
        self.game_settings.current_color = make_move_player_response.current_color
        self.game_settings.update_info_label()

        if self.game_settings.game_type == TypesOfGames.singleplayer:
            make_move_by_ai_response: MakeMoveByAIResponse = self.game_settings.game_api.make_ai_move()
            self.clear_captured_pieces(make_move_by_ai_response.captured_pieces)
            self.image_storage.change_ceil_image(self.game_settings.current_color.get_type_of_cells(),
                                                 self.game_settings.field_cell[make_move_by_ai_response.y][
                                                     make_move_by_ai_response.x])

            self.game_settings.current_color = make_move_by_ai_response.current_turn

        current_score: GetCapturedCountResponse = self.game_settings.game_api.get_captured_pieces_count()
        self.game_settings.update_score(current_score.white_count, current_score.black_count)

        self.game_settings.configure_pass_buttons()

    def clear_captured_pieces(self, captured_pieces: List[Cell]):
        for captured_cell in captured_pieces:
            self.image_storage.change_ceil_image(CellTypes.empty,
                                                 self.game_settings.field_cell[captured_cell.y - 1][
                                                     captured_cell.x - 1])


def start_gui():
    main_window = tk.Tk()
    display = Display(main_window)
    main_window.focus_force()
    display.window.mainloop()
