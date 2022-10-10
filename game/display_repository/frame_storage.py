import tkinter as tk
from .consts import *
from PIL import ImageTk, Image


class FrameStorage:
    def __init__(self, window):
        self._window = window
        main_menu_bg_image = Image.open('./img/main_menu_bg.jpg')
        self._main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)

        self.menu_frame = self._create_menu_frame()
        self.leaderboard_frame = self._create_menu_frame()
        self.game_players_count_frame = self._create_menu_frame()
        self.game_size_frame = self._create_menu_frame()

        self.game_frame = tk.Frame(window)
        self.escape_frame = self._create_menu_frame()

    def _create_menu_frame(self):
        menu_frame = tk.Frame(self._window, width=WIDTH, height=HEIGHT)
        main_menu_bg_label = tk.Label(menu_frame, image=self._main_menu_bg)
        main_menu_bg_label.place(x=0, y=0)

        menu_frame.pack_propagate(False)
        return menu_frame
