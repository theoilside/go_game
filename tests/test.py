from unittest import TestCase
import unittest
from ..game.go import *

BORDER = lambda x, y: Cell(CellTypes.border, CellStates.unmarked, x, y)
EMPTY = lambda x, y: Cell(CellTypes.empty, CellStates.unmarked, x, y)
BLACK = lambda x, y: Cell(CellTypes.black, CellStates.unmarked, x, y)
WHITE = lambda x, y: Cell(CellTypes.white, CellStates.unmarked, x, y)


def _assert_2d_list(self, actual, expected):
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
        self.assertEqual(len(actual[i]), len(expected[i]))
        self.assertListEqual(actual[i], expected[i])


class GenerateEmptyBoards(TestCase):
    def test_correct_size(self):
        board_actual = generate_empty_board(4)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), EMPTY(1, 1), EMPTY(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual, board_expected)

    def test_working_board_class(self):
        board_actual = Board(2).board
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), EMPTY(1, 1), EMPTY(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual, board_expected)

    def test_too_low_size(self):
        self.assertRaises(ValueError, lambda: generate_empty_board(-1))

    def test_too_big_size(self):
        self.assertRaises(ValueError, lambda: generate_empty_board(999999999))


class PlacePiecesTests(TestCase):
    def place_black_piece_at_coords(self, x, y):
        board = Board(2)
        board.place_piece(Colors.black, x, y)
        return board

    def test_placing(self):
        board_actual = self.place_black_piece_at_coords(0, 0)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), BLACK(1, 1), EMPTY(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual.board, board_expected)

    def test_placing_two_pieces(self):
        board_actual = self.place_black_piece_at_coords(0, 0)
        board_actual.place_piece(Colors.white, 1, 0)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), BLACK(1, 1), WHITE(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual.board, board_expected)

    def test_not_placing_piece_on_another_piece(self):
        board_actual = self.place_black_piece_at_coords(0, 0)
        board_actual.place_piece(Colors.white, 0, 0)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), BLACK(1, 1), EMPTY(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual.board, board_expected)

    def test_not_placing_on_borders(self):
        board_actual = self.place_black_piece_at_coords(2, 2)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), EMPTY(1, 1), EMPTY(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual.board, board_expected)

    def test_not_placing_with_too_big_coordinates(self):
        self.assertRaises(ValueError, lambda: self.place_black_piece_at_coords(5, 5))


class GetPiecesTests(TestCase):
    def test_getting_cell(self, x=1, y=1):
        board = Board(2)
        board.place_piece(Colors.black, 0, 0)
        cell_actual = board.get_cell(x, y)
        cell_expected = Cell(CellTypes.black, CellStates.unmarked, 1, 1)
        self.assertEqual(cell_actual, cell_expected)

    def test_getting_cell_with_wrong_coords(self):
        self.assertRaises(ValueError, lambda: self.test_getting_cell(5, 5))


if __name__ == '__main__':
    unittest.main()
