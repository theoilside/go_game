import tkinter as tk
from .consts import *


class ButtonCreator:
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
