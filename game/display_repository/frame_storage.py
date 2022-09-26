import tkinter as tk
from .consts import *
from PIL import ImageTk, Image


class FrameStorage:
    def __init__(self, window):
        self.window = window
        main_menu_bg_image = Image.open('./img/main_menu_bg.jpg')
        self.main_menu_bg = ImageTk.PhotoImage(main_menu_bg_image)

    def create_menu_frame(self):
        menu_frame = tk.Frame(self.window, width=WIDTH, height=HEIGHT)
        main_menu_bg_label = tk.Label(menu_frame, image=self.main_menu_bg)
        main_menu_bg_label.place(x=0, y=0)

        menu_frame.pack_propagate(False)
        return menu_frame
