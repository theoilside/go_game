import tkinter as tk
from tkinter import messagebox

from .display_repository.button_creator import ButtonCreator
from .display_repository.game_settings import GameSettings
from .display_repository.image_storage import ImageStorage
from .request_response import StartGameResponse, MakeMoveByPlayerResponse, MakeMoveByAIResponse
from .go import TypesOfGames, Colors
from .display_repository.consts import *
from .display_repository.frame_storage import FrameStorage


class Display:
    def __init__(self, window):
        self.window = window

        self.game_field_ceil = None
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
                                           callback=lambda: self.save_chosen_player_count(TypesOfGames.singleplayer))
        self.element_creator.create_button('Два игрока', self.frame_storage.game_players_count_frame,
                                           callback=lambda: self.save_chosen_player_count(TypesOfGames.multiplayer))

        # Frame with field size config
        self.element_creator.create_label('Выберете размер игрового поля', self.frame_storage.game_size_frame, width=20)
        self.element_creator.create_button('9x9', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.save_chosen_field_size(9))
        self.element_creator.create_button('13x13', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.save_chosen_field_size(13))
        self.element_creator.create_button('19x19', self.frame_storage.game_size_frame, width=10,
                                           callback=lambda: self.save_chosen_field_size(19))

        self.game_settings.info_label = tk.Label(self.frame_storage.game_frame, font='Calibri 20')

    @staticmethod
    def change_frame(old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack()

    def save_chosen_player_count(self, game_type: TypesOfGames):
        self.game_settings.game_type = game_type
        self.change_frame(self.frame_storage.game_players_count_frame, self.frame_storage.game_size_frame)

    def save_chosen_field_size(self, size):
        self.game_settings.size = size

        start_game_response: StartGameResponse = self.game_settings.game_state.start_new_game(self.game_settings.size)
        if not start_game_response.is_success:
            raise 'Невозомжно начать игру'
        self.game_settings.current_turn_color = start_game_response.current_turn
        if self.game_settings.game_type == TypesOfGames.multiplayer:
            self.game_settings.configure_label_multiplayer()
        else:
            self.game_settings.configure_label_singleplayer(Colors.black)

        self.game_field_ceil = self.init_game_field()
        self.change_frame(self.frame_storage.game_size_frame, self.frame_storage.game_frame)

    def init_game_field(self):
        field_size = self.game_settings.size
        self.game_settings.info_label.grid(row=0, columnspan=field_size)

        game_field_ceil = []
        for x in range(1, field_size + 1):
            game_row_ceil = []
            for y in range(field_size):
                btn = tk.Label(self.frame_storage.game_frame,
                               text=' ',
                               image=self.image_storage.empty_cell,
                               borderwidth=0,
                               highlightthickness=0,
                               )
                btn.bind("<Button-1>", lambda e, a=x - 1, b=y: self.on_game_cell_pressed(a, b))

                btn.grid(row=x, column=y)
                game_row_ceil.append(btn)
            game_field_ceil.append(game_row_ceil)

        pass_button = tk.Button(self.frame_storage.game_frame, text='ПАСС', font='Calibri 34 bold', bg=BUTTON_COLOR,
                                activebackground=BUTTON_PRESSED_COLOR, )
        pass_button.grid(row=field_size + 3, columnspan=field_size, pady=(20, 0))
        return game_field_ceil

    def on_game_cell_pressed(self, row, column):
        make_move_player_response: MakeMoveByPlayerResponse = \
            self.game_settings.game_state.make_player_move(x=column, y=row)
        if not make_move_player_response.is_success:
            messagebox.showinfo('Нельзя сделать такой ход', make_move_player_response.error_message)
            return

        self.image_storage.change_ceil_image(
            self.game_settings.current_turn_color.get_type_of_cells(), self.game_field_ceil[row][column])
        self.game_settings.current_turn_color = make_move_player_response.current_turn
        self.game_settings.update_label()

        if self.game_settings.game_type == TypesOfGames.singleplayer:
            make_move_by_ai_response: MakeMoveByAIResponse = self.game_settings.game_state.make_ai_move()

            self.image_storage.change_ceil_image(self.game_settings.current_turn_color.get_type_of_cells(),
                                                 self.game_field_ceil[make_move_by_ai_response.y][
                                                     make_move_by_ai_response.x])

            self.game_settings.current_turn_color = make_move_by_ai_response.current_turn


def start_gui():
    main_window = tk.Tk()
    display = Display(main_window)
    display.window.mainloop()
