import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from .settings import GameSettings
from .request_response import StartGameResponse, MakeMoveByPlayerResponse, MakeMoveByAIResponse
from .enums import CellTypes
from .go import TypesOfGames, Colors

# Root settings
WIDTH = 1080
HEIGHT = 720

LABEL_COLOR = '#B88B5E'
BUTTON_COLOR = '#D09E6B'
BUTTON_PRESSED_COLOR = '#B88B5E'
BLACK_COLOR = '#000000'


class Display:
    def __init__(self, window):
        self.game_field_ceil = None
        self.game_settings = GameSettings()

        window.geometry(f'{WIDTH}x{HEIGHT}')
        window.title('Игра "Го"')
        window.iconbitmap('./img/icon.ico')

        self.window = window
        self.create_frames()

    def create_frames(self):
        # Bg images
        self.empty_ceil = tk.PhotoImage(file='./img/empty.png')
        self.white_ceil = tk.PhotoImage(file='./img/white.png')
        self.black_ceil = tk.PhotoImage(file='./img/black.png')

        main_menu_bg_image = Image.open('./img/main_menu_bg.jpg')
        self.main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)

        menu_frame = self.create_menu_frame()
        menu_frame.pack()

        game_name = self.create_label('Игра Го', menu_frame)
        start_button = self.create_button('Начать игру', menu_frame,
                                          callback=lambda: self.change_frame(menu_frame, game_players_count_frame))
        settings_button = self.create_button('Настройки', menu_frame)
        exit_button = self.create_button('Выход', menu_frame, callback=lambda: self.window.quit())

        game_players_count_frame = self.create_menu_frame()
        self.game_players_count_frame = game_players_count_frame

        choose_player_count = self.create_label('Выберете режим игры', game_players_count_frame, width=20)
        singleplayer_button = self.create_button('С компьютером', game_players_count_frame,
                                                 callback=lambda: self.save_chosen_player_count(
                                                     TypesOfGames.singleplayer))
        multiplayer_button = self.create_button('Два игрока', game_players_count_frame,
                                                callback=lambda: self.save_chosen_player_count(
                                                    TypesOfGames.multiplayer))

        # Game size
        game_size_frame = self.create_menu_frame()
        self.game_size_frame = game_size_frame

        choose_field_size = self.create_label('Выберете размер игрового поля', game_size_frame, width=20)
        field_size_9x9 = self.create_button('9x9', game_size_frame, width=10,
                                            callback=lambda: self.save_chosen_field_size(9))
        field_size_13x13 = self.create_button('13x13', game_size_frame, width=10,
                                              callback=lambda: self.save_chosen_field_size(13))
        field_size_19x19 = self.create_button('19x19', game_size_frame, width=10,
                                              callback=lambda: self.save_chosen_field_size(19))
        # field_size_custom = self.create_button('Другой', game_size_frame, width=10,
        #                                        callback=None)

        self.game_frame = tk.Frame(self.window)
        self.game_settings.info_label = tk.Label(self.game_frame, font='Calibri 20')

    def create_label(self, text, parent, font='Calibri 34', width=15):
        border = self._create_border(parent)
        label = tk.Label(border,
                         text=text,
                         font=font,
                         bg=LABEL_COLOR,
                         width=width,
                         wraplength=500,
                         )

        label.pack()
        border.pack(pady=10)
        return label

    def create_button(self, text, parent, callback=None, font='Calibri 34', width=16):
        border = self._create_border(parent)
        button = tk.Button(border,
                           text=text,
                           font=font,
                           command=callback,
                           bg=BUTTON_COLOR,
                           activebackground=BUTTON_PRESSED_COLOR,
                           width=width,
                           )

        button.pack()
        border.pack(pady=10)
        return button

    @staticmethod
    def _create_border(parent):
        return tk.Frame(parent,
                        highlightbackground=BLACK_COLOR,
                        highlightthickness=2,
                        bd=0,
                        )

    @staticmethod
    def change_frame(old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack()

    def create_menu_frame(self):
        menu_frame = tk.Frame(self.window, width=WIDTH, height=HEIGHT)
        main_menu_bg_label = tk.Label(menu_frame, image=self.main_menu_bg)
        main_menu_bg_label.place(x=0, y=0)

        menu_frame.pack_propagate(False)
        return menu_frame

    def save_chosen_player_count(self, game_type: TypesOfGames):
        self.game_settings.game_type = game_type
        self.change_frame(self.game_players_count_frame, self.game_size_frame)

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
        self.change_frame(self.game_size_frame, self.game_frame)

    def init_game_field(self):
        field_size = self.game_settings.size
        self.game_settings.info_label.grid(row=0, columnspan=field_size)

        game_field_ceil = []
        for x in range(1, field_size + 1):
            game_row_ceil = []
            for y in range(field_size):
                btn = tk.Label(self.game_frame,
                               text=' ',
                               image=self.empty_ceil,
                               borderwidth=0,
                               highlightthickness=0,
                               )
                btn.bind("<Button-1>", lambda e, x=x - 1, y=y: self.on_game_cell_pressed(x, y))

                btn.grid(row=x, column=y)
                game_row_ceil.append(btn)
            game_field_ceil.append(game_row_ceil)

        pass_button = tk.Button(self.game_frame, text='ПАСС', font='Calibri 34 bold', bg=BUTTON_COLOR,
                                activebackground=BUTTON_PRESSED_COLOR, )
        pass_button.grid(row=field_size + 3, columnspan=field_size, pady=(20, 0))
        return game_field_ceil

    def change_ceil_image(self, cell_type: CellTypes, label_to_change: tk.Label):
        match cell_type:
            case CellTypes.white:
                image = self.white_ceil
            case CellTypes.black:
                image = self.black_ceil
            case _:
                image = self.empty_ceil

        label_to_change.configure(image=image)

    def on_game_cell_pressed(self, row, column):
        make_move_player_response: MakeMoveByPlayerResponse = \
            self.game_settings.game_state.make_player_move(x=column, y=row)
        if not make_move_player_response.is_success:
            messagebox.showinfo('Нельзя сделать такой ход', make_move_player_response.error_message)
            return

        self.change_ceil_image(
            self.game_settings.current_turn_color.get_type_of_cells(), self.game_field_ceil[row][column])
        self.game_settings.current_turn_color = make_move_player_response.current_turn
        self.game_settings.update_label()

        if self.game_settings.game_type == TypesOfGames.singleplayer:
            make_move_by_ai_response: MakeMoveByAIResponse = self.game_settings.game_state.make_ai_move()

            self.change_ceil_image(self.game_settings.current_turn_color.get_type_of_cells(),
                                   self.game_field_ceil[make_move_by_ai_response.y][make_move_by_ai_response.x])

            self.game_settings.current_turn_color = make_move_by_ai_response.current_turn


def start_gui():
    main_window = tk.Tk()
    display = Display(main_window)
    display.window.mainloop()
