import tkinter as tk
from .consts import *
from ..enums import CellTypes


class ImageStorage:
    def __init__(self):
        self.empty_cell = tk.PhotoImage(file=EMPTY_CELL_PATH)
        self.white_cell = tk.PhotoImage(file=WHITE_CELL_PATH)
        self.black_cell = tk.PhotoImage(file=BLACK_CELL_PATH)

    def change_ceil_image(self, cell_type: CellTypes, label_to_change: tk.Label):
        match cell_type:
            case CellTypes.white:
                image = self.white_cell
            case CellTypes.black:
                image = self.black_cell
            case _:
                image = self.empty_cell

        label_to_change.configure(image=image)
