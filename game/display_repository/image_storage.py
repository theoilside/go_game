import tkinter as tk

from ..enums import CellTypes
from .consts import *


class ImageStorage:
    def __init__(self):
        self.empty_cell = tk.PhotoImage(file=EMPTY_CELL_PATH)
        self.white_cell = tk.PhotoImage(file=WHITE_CELL_PATH)
        self.black_cell = tk.PhotoImage(file=BLACK_CELL_PATH)
        self.white_red_cell = tk.PhotoImage(file=WHITE_RED_CELL_PATH)
        self.black_red_cell = tk.PhotoImage(file=BLACK_RED_CELL_PATH)

    def change_cell_image(self, cell_type: CellTypes, label_to_change: tk.Label):
        match cell_type:
            case CellTypes.white:
                image = self.white_cell
            case CellTypes.black:
                image = self.black_cell
            case _:
                image = self.empty_cell

        label_to_change.configure(image=image)

    def highlight_cell(self, label_to_change: tk.Label, cell_type: CellTypes, highlighted: bool):
        match cell_type, highlighted:
            case CellTypes.black, False:
                image = self.black_red_cell
            case CellTypes.white, False:
                image = self.white_red_cell
            case CellTypes.black, True:
                image = self.black_cell
            case CellTypes.white, True:
                image = self.white_cell
            case _:
                image = self.empty_cell

        label_to_change.configure(image=image)
