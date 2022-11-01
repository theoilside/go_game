import tkinter as tk
from typing import Literal

from .consts import *


class ElementCreator:
    def create_label(self, text, parent: tk.Frame, font=CALIBRI_LARGE_FONT, width=15,
                     justify: Literal["left", "center", "right"] = 'center'):
        border = self._create_border(parent)
        label = tk.Label(border,
                         text=text,
                         font=font,
                         bg=LABEL_COLOR,
                         width=width,
                         justify=justify
                         )

        label.pack()
        border.pack(pady=10)
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))
        return label

    def create_button(self, text, parent: tk.Frame, callback=None, callback2=None, font=CALIBRI_LARGE_FONT, width=16):
        border = self._create_border(parent)
        button = tk.Button(border,
                           text=text,
                           font=font,
                           command=lambda: [callback(), callback2()],
                           bg=BUTTON_COLOR,
                           activebackground=BUTTON_PRESSED_COLOR,
                           width=width,
                           highlightbackground=BUTTON_COLOR,  # For Mac OS
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
