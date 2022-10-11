import tkinter as tk

from .display_repository.element_creator import ElementCreator
from .display_repository.game_settings import GameSettings
from .display_repository.image_storage import ImageStorage
from .api import *
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
        self.element_creator = ElementCreator()

        self.is_game_active = False
        self.leaderboard: List[Tuple[str, int]] = []

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
        self.element_creator.create_button('Лидерборд', self.frame_storage.menu_frame,
                                           callback=self.on_leaderboard_open)
        self.element_creator.create_button('Правила игры', self.frame_storage.menu_frame,
                                           callback=lambda: self.change_frame(self.frame_storage.menu_frame,
                                                                              self.frame_storage.rule_frame))

        self.element_creator.create_button('Выход', self.frame_storage.menu_frame, callback=lambda: self.window.quit())

        # Frame with game type config
        self.element_creator.create_label('Выберете режим игры', self.frame_storage.game_players_count_frame, width=20)
        self.element_creator.create_button('С компьютером', self.frame_storage.game_players_count_frame,
                                           callback=lambda: self.on_chosen_player_count(TypesOfGames.singleplayer))
        self.element_creator.create_button('Два игрока', self.frame_storage.game_players_count_frame,
                                           callback=lambda: self.on_chosen_player_count(TypesOfGames.multiplayer))
        self.element_creator.create_button('Назад', self.frame_storage.game_players_count_frame,
                                           callback=lambda: self.change_frame(
                                               self.frame_storage.game_players_count_frame,
                                               self.frame_storage.menu_frame))

        # Frame with field size config
        self.element_creator.create_label('Выберете размер игрового поля', self.frame_storage.game_size_frame, width=20)
        self.element_creator.create_button('9x9', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.on_chosen_field_size(9))
        self.element_creator.create_button('13x13', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.on_chosen_field_size(13))
        self.element_creator.create_button('19x19', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.on_chosen_field_size(19))
        self.element_creator.create_button('Назад', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.change_frame(
                                               self.frame_storage.game_size_frame,
                                               self.frame_storage.game_players_count_frame))

        # Frame with rules config
        self.element_creator.create_label('Правила игры', self.frame_storage.rule_frame, width=20)

        text = ' ' * 4 + f'\n\n{" " * 4}'.join(RULES)

        rule_label = self.element_creator.create_label(text, self.frame_storage.rule_frame, width=60,
                                                       font=CALIBRI_SMALL_FONT,
                                                       justify='left')
        self.element_creator.create_button('Назад', self.frame_storage.rule_frame, width=10,
                                           callback=lambda: self.change_frame(self.frame_storage.rule_frame,
                                                                              self.frame_storage.menu_frame))

        scroll = tk.Scrollbar(self.frame_storage.rule_frame, orient=tk.VERTICAL)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.config(command=rule_label)

        # Frame with leaderboard config
        if len(self.leaderboard) == 0:
            self.element_creator.create_label('Таблица лидеров пуста', self.frame_storage.leaderboard_frame, width=20)
        else:
            self.element_creator.create_label('Таблица лидеров', self.frame_storage.leaderboard_frame, width=20)
            for (name, score) in self.leaderboard:
                self.element_creator.create_label(f'{name} : {score}', self.frame_storage.leaderboard_frame, width=30)

        self.element_creator.create_button('Назад', self.frame_storage.leaderboard_frame, width=10,
                                           callback=lambda: self.change_frame(self.frame_storage.leaderboard_frame,
                                                                              self.frame_storage.menu_frame))

        # Frame with escape items config
        self.window.bind('<Escape>', lambda e: self.change_frame(self.frame_storage.game_frame,
                                                                 self.frame_storage.escape_frame)
        if self.is_game_active else None)

        self.element_creator.create_button('Продолжить игру', self.frame_storage.escape_frame, width=20,
                                           callback=lambda: self.change_frame(self.frame_storage.escape_frame,
                                                                              self.frame_storage.game_frame))

        self.element_creator.create_button('Выйти в главное меню', self.frame_storage.escape_frame, width=20,
                                           callback=lambda: _exit_game_by_user())

        def _exit_game_by_user():
            self.change_frame(self.frame_storage.escape_frame,
                              self.frame_storage.menu_frame)
            self.game_settings = GameSettings()
            self.is_game_active = False

    def on_leaderboard_open(self):
        self.leaderboard = self.game_settings.game_state.get_leaderboard().leaderboard
        self.change_frame(self.frame_storage.menu_frame,
                          self.frame_storage.leaderboard_frame)

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
        self.is_game_active = True

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
        self.clear_captured_pieces(make_move_player_response.captured_pieces)

        self.image_storage.change_ceil_image(
            self.game_settings.current_color.get_type_of_cells(), self.game_settings.field_cell[row][column])
        self.game_settings.current_color = make_move_player_response.current_color
        self.game_settings.update_info_label()

        if self.game_settings.game_type == TypesOfGames.singleplayer:
            make_move_by_ai_response: MakeMoveByAIResponse = self.game_settings.game_state.make_ai_move()
            self.clear_captured_pieces(make_move_by_ai_response.captured_pieces)
            self.image_storage.change_ceil_image(self.game_settings.current_color.get_type_of_cells(),
                                                 self.game_settings.field_cell[make_move_by_ai_response.y][
                                                     make_move_by_ai_response.x])

            self.game_settings.current_color = make_move_by_ai_response.current_turn

        current_score: GetCapturedCountResponse = self.game_settings.game_state.get_captured_pieces_count()
        self.game_settings.update_score(current_score.white_count, current_score.black_count)

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
