import tkinter as tk
from .consts import *


class ImageStorage:
    def __init__(self):
        self.empty_cell = tk.PhotoImage(file=EMPTY_CELL_PATH)
        self.white_cell = tk.PhotoImage(file=WHITE_CELL_PATH)
        self.black_cell = tk.PhotoImage(file=BLACK_CELL_PATH)
