import tkinter as tk
from PIL import ImageTk, Image

# Root settings
WIDTH = 1080
HEIGHT = 720

LABEL_COLOR = '#B88B5E'
BUTTON_COLOR = '#D09E6B'
BUTTON_PRESSED_COLOR = '#B88B5E'

window = tk.Tk()
window.geometry(f'{WIDTH}x{HEIGHT}')
window.title('Игра "Го"')
window.iconbitmap('icon.ico')


def change_frame(old_frame, new_frame):
    old_frame.pack_forget()
    new_frame.pack()


def create_menu_frame():
    menu_frame = tk.Frame(window, width=WIDTH, height=HEIGHT)
    main_menu_bg_label = tk.Label(menu_frame, image=main_menu_bg)
    main_menu_bg_label.place(x=0, y=0)

    menu_frame.pack_propagate(False)
    return menu_frame


game_settings = {
    'player_count': 1,
    'field_size': 9,
}

# Bg images
empty_ceil = tk.PhotoImage(file='./empty.png')
white_ceil = tk.PhotoImage(file='./white.png')
black_ceil = tk.PhotoImage(file='./black.png')

main_menu_bg_image = Image.open('./main_menu_bg.jpg')
main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)

# Menu
menu_frame = create_menu_frame()
menu_frame.pack()


def _create_border(parent):
    return tk.Frame(parent,
                    highlightbackground='black',
                    highlightthickness=2,
                    bd=0,
                    )


def create_label(text, parent=menu_frame, font='Calibri 34', width=15):
    border = _create_border(parent)
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


def create_button(text, parent=menu_frame, callback=None, font='Calibri 34', width=16):
    border = _create_border(parent)
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


game_name = create_label('Игра Го')
start_button = create_button('Начать игру', callback=lambda: change_frame(menu_frame, game_players_count_frame))
settings_button = create_button('Настройки')
exit_button = create_button('Выход', callback=lambda: window.quit())

# Players count
game_players_count_frame = create_menu_frame()


def save_chosen_player_count(count, game_settings_data):
    game_settings_data['player_count'] = count
    change_frame(game_players_count_frame, game_size_frame)


choose_player_count = create_label('Выберете режим игры', game_players_count_frame, width=20)
singleplayer_button = create_button('С компьютером', game_players_count_frame,
                                    callback=lambda: save_chosen_player_count(1, game_settings))
multiplayer_button = create_button('Два игрока', game_players_count_frame,
                                   callback=lambda: save_chosen_player_count(2, game_settings))

# Game size
game_size_frame = create_menu_frame()


def save_chosen_field_size(size, game_settings_data):
    game_settings_data['field_size'] = size
    # TODO: Отправить запрос на начало игры
    global game_field_ceil
    game_field_ceil = init_game_field()
    change_frame(game_size_frame, game_frame)


choose_field_size = create_label('Выберете размер игрового поля', game_size_frame, width=20)
field_size_9x9 = create_button('9x9', game_size_frame, width=10,
                               callback=lambda: save_chosen_field_size(9, game_settings))
field_size_13x13 = create_button('13x13', game_size_frame, width=10,
                                 callback=lambda: save_chosen_field_size(13, game_settings))
field_size_19x19 = create_button('19x19', game_size_frame, width=10,
                                 callback=lambda: save_chosen_field_size(19, game_settings))
field_size_custom = create_button('Другой', game_size_frame, width=10,
                                  callback=None)

# Game
game_frame = tk.Frame(window)
# game_frame.pack()

state = tk.Label(game_frame, text='Сейчас ходит белый игрок', font='Calibri 20')
game_field_ceil = None


def init_game_field():
    field_size = game_settings['field_size']
    state.grid(row=0, columnspan=field_size)
    game_field_ceil = []
    for x in range(1, field_size + 1):
        game_row_ceil = []
        for y in range(field_size):
            btn = tk.Label(game_frame,
                            text=' ',
                            image=empty_ceil,
                            borderwidth=0,
                            highlightthickness=0,
                            relief=tk.RAISED,
                            )
            btn.bind("<Button-1>", lambda e,x=x - 1, y=y: on_game_cell_pressed(x, y))

            btn.grid(row=x, column=y)
            game_row_ceil.append(btn)
        game_field_ceil.append(game_row_ceil)
    return game_field_ceil


is_white_turn = True  # TODO: Заглушка, убрать


def on_game_cell_pressed(row, column):
    # TODO: Отправить запрос на нажатие по клетке поля. Получить ответ и отобразить результат.
    global is_white_turn, state

    # Пока отображаем как для игры двух человек
    game_field_ceil[row][column].configure(image=white_ceil if is_white_turn else black_ceil)

    # Убрать
    is_white_turn = not is_white_turn
    state.configure(text=f'Сейчас ходит {"белый" if is_white_turn else "чёрный"} игрок')


window.mainloop()
