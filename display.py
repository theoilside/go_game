import tkinter as tk
from PIL import ImageTk, Image

from ReqestResponse import StartGameResponse, MakeMoveByPlayerResponse, MakeMoveByAIResponse
from go import MultiplayerGame, SingleplayerGame, TypesOfGames, Colors

# Root settings
WIDTH = 1080
HEIGHT = 720

LABEL_COLOR = '#B88B5E'
BUTTON_COLOR = '#D09E6B'
BUTTON_PRESSED_COLOR = '#B88B5E'


class GameSettings:
    def __init__(self):
        self.size: int = 9
        self.game_type: TypesOfGames = TypesOfGames.singleplayer
        self.current_turn_color: Colors = Colors.black


window = tk.Tk()

# Bg images
empty_ceil = tk.PhotoImage(file='./empty.png')
white_ceil = tk.PhotoImage(file='./white.png')
black_ceil = tk.PhotoImage(file='./black.png')

main_menu_bg_image = Image.open('./main_menu_bg.jpg')
main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)


class Display:
    def __init__(self, window):
        self.game_field_ceil = None
        self.game_settings = GameSettings()

        window.geometry(f'{WIDTH}x{HEIGHT}')
        window.title('Игра "Го"')
        window.iconbitmap('icon.ico')

        self.window = window
        self.create_frames()

    def create_frames(self):
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
        field_size_custom = self.create_button('Другой', game_size_frame, width=10,
                                               callback=None)

        self.game_frame = tk.Frame(self.window)
        self.state = tk.Label(self.game_frame, text='Сейчас ходит белый игрок', font='Calibri 20')

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
    def change_frame(old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack()

    def create_menu_frame(self):
        menu_frame = tk.Frame(self.window, width=WIDTH, height=HEIGHT)
        main_menu_bg_label = tk.Label(menu_frame, image=main_menu_bg)
        main_menu_bg_label.place(x=0, y=0)

        menu_frame.pack_propagate(False)
        return menu_frame

    def save_chosen_player_count(self, game_type: TypesOfGames):
        self.game_settings.game_type = game_type
        self.change_frame(self.game_players_count_frame, self.game_size_frame)

    @staticmethod
    def _create_border(parent):
        return tk.Frame(parent,
                        highlightbackground='black',
                        highlightthickness=2,
                        bd=0,
                        )

    def save_chosen_field_size(self, size):
        self.game_settings.size = size
        self.game = SingleplayerGame() if self.game_settings.game_type == TypesOfGames.singleplayer else MultiplayerGame()

        start_game_response: StartGameResponse = self.game.start_new_game(self.game_settings.size)
        if not start_game_response.is_success:
            raise 'Невозомжно начать игру'
        self.game_settings.current_turn_color = start_game_response.current_turn
        if self.game_settings.game_type == TypesOfGames.multiplayer:
            self.state.configure(
                text=f'Сейчас ходит {"белый" if self.game_settings.current_turn_color == Colors.white else "чёрный"} игрок')
        else:
            self.state.configure(text='Вы играете за чёрных')

        self.game_field_ceil = self.init_game_field()
        self.change_frame(self.game_size_frame, self.game_frame)

    def init_game_field(self):
        field_size = self.game_settings.size
        self.state.grid(row=0, columnspan=field_size)
        game_field_ceil = []
        for x in range(1, field_size + 1):
            game_row_ceil = []
            for y in range(field_size):
                btn = tk.Label(self.game_frame,
                               text=' ',
                               image=empty_ceil,
                               borderwidth=0,
                               highlightthickness=0,
                               relief=tk.RAISED,
                               )
                btn.bind("<Button-1>", lambda e, x=x - 1, y=y: self.on_game_cell_pressed(x, y))

                btn.grid(row=x, column=y)
                game_row_ceil.append(btn)
            game_field_ceil.append(game_row_ceil)
        return game_field_ceil

    def on_game_cell_pressed(self, row, column):
        make_move_player_response: MakeMoveByPlayerResponse = self.game.make_player_move(x=column, y=row)
        if not make_move_player_response.is_success:
            raise 'Нельзя сделать такой ход'

        # Пока отображаем как для игры двух человек
        self.game_field_ceil[row][column].configure(
            image=white_ceil if self.game_settings.current_turn_color == Colors.white else black_ceil)

        self.game_settings.current_turn_color = make_move_player_response.current_turn

        if self.game_settings.game_type == TypesOfGames.multiplayer:
            self.state.configure(
                text=f'Сейчас ходит {"белый" if self.game_settings.current_turn_color == Colors.white else "чёрный"} игрок')

        if self.game_settings.game_type == TypesOfGames.singleplayer:
            make_move_by_ai_response: MakeMoveByAIResponse = self.game.make_ai_move()
            self.game_field_ceil[make_move_by_ai_response.y][make_move_by_ai_response.x].configure(
                image=white_ceil if self.game_settings.current_turn_color == Colors.white else black_ceil)

            self.game_settings.current_turn_color = make_move_by_ai_response.current_turn


display = Display(window)
display.window.mainloop()
