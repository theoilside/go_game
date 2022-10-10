import tkinter as tk

from .display_repository.button_creator import ButtonCreator
from .display_repository.game_settings import GameSettings
from .display_repository.image_storage import ImageStorage
from .api import StartGameResponse, MakeMoveByPlayerResponse, MakeMoveByAIResponse
from .enums import CellTypes
from .go import TypesOfGames
from .display_repository.consts import *
from .display_repository.frame_storage import FrameStorage


class Display:
    def __init__(self, window):
        self.window = window

        self.game_settings = GameSettings()
        self.frame_storage = FrameStorage(window)
        self.image_storage = ImageStorage()
        self.element_creator = ButtonCreator()

        window.geometry(f'{WIDTH}x{HEIGHT}')
        window.title('Игра "Го"')
        window.iconbitmap(ICON_PATH)

        self.create_frames()

    def create_frames(self):
        self.frame_storage.menu_frame.pack()

        # Main frame config
        self.element_creator.create_label('Игра Го', self.frame_storage.menu_frame)
        self.element_creator.create_button('Начать игру', self.frame_storage.menu_frame,
                                           callback=lambda:
                                           self.change_frame(self.frame_storage.menu_frame,
                                                             self.frame_storage.game_players_count_frame))
        self.element_creator.create_button('Настройки', self.frame_storage.menu_frame)
        self.element_creator.create_button('Выход', self.frame_storage.menu_frame, callback=lambda: self.window.quit())

        # Frame with game type config
        self.element_creator.create_label('Выберете режим игры', self.frame_storage.game_players_count_frame, width=20)
        self.element_creator.create_button('С компьютером', self.frame_storage.game_players_count_frame,
                                           callback=lambda: self.on_chosen_player_count(TypesOfGames.singleplayer))
        self.element_creator.create_button('Два игрока', self.frame_storage.game_players_count_frame,
                                           callback=lambda: self.on_chosen_player_count(TypesOfGames.multiplayer))

        # Frame with field size config
        self.element_creator.create_label('Выберете размер игрового поля', self.frame_storage.game_size_frame, width=20)
        self.element_creator.create_button('9x9', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.on_chosen_field_size(9))
        self.element_creator.create_button('13x13', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.on_chosen_field_size(13))
        self.element_creator.create_button('19x19', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.on_chosen_field_size(19))

    @staticmethod
    def change_frame(old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack()

    def on_chosen_player_count(self, game_type: TypesOfGames):
        self.game_settings.game_type = game_type
        self.change_frame(self.frame_storage.game_players_count_frame, self.frame_storage.game_size_frame)

    def on_chosen_field_size(self, size):
        self.game_settings.size = size

        start_game_response: StartGameResponse = self.game_settings.game_state.start_new_game(size)
        self.game_settings.current_color = start_game_response.current_turn
        self.init_game_field()
        self.change_frame(self.frame_storage.game_size_frame, self.frame_storage.game_frame)

    def init_game_field(self):
        self.game_settings.init_game_state(self.frame_storage.game_frame, self.on_game_cell_pressed)

        return self.game_settings.field_cell

    def on_game_cell_pressed(self, row, column):
        make_move_player_response: MakeMoveByPlayerResponse = \
            self.game_settings.game_state.make_player_move(x=column, y=row)

        # Если ход сделать нельзя, вывести ошибку
        if not make_move_player_response.is_success:
            self.game_settings.update_error_label(is_error=True)
            return
        self.game_settings.update_error_label(is_error=False)

        # Убрать с поля все захваченные фигуры
        for captured_cell in make_move_player_response.captured_pieces:
            self.image_storage.change_ceil_image(CellTypes.empty,
                                                 self.game_settings.field_cell[captured_cell.y - 1][
                                                     captured_cell.x - 1])

        self.image_storage.change_ceil_image(
            self.game_settings.current_color.get_type_of_cells(), self.game_settings.field_cell[row][column])
        self.game_settings.current_color = make_move_player_response.current_color
        self.game_settings.update_info_label()

        # Если игра многопользовательская, то не делать ничего
        if self.game_settings.game_type == TypesOfGames.multiplayer:
            return

        # Иначе ход сделает компьютер
        make_move_by_ai_response: MakeMoveByAIResponse = self.game_settings.game_state.make_ai_move()
        self.image_storage.change_ceil_image(self.game_settings.current_color.get_type_of_cells(),
                                             self.game_settings.field_cell[make_move_by_ai_response.y][
                                                 make_move_by_ai_response.x])

        self.game_settings.current_color = make_move_by_ai_response.current_turn


def start_gui():
    main_window = tk.Tk()
    display = Display(main_window)
    display.window.mainloop()
