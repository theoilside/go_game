from unittest import TestCase
import unittest
from ..game.go import *


class TestGenerateEmptyBoard(TestCase):
    def test_on_correct_size(self):
        board_actual = generate_empty_board(4)

        border_cell = lambda x, y: Cell(CellTypes.border, CellStates.unmarked, x, y)
        field_cell = lambda x, y: Cell(CellTypes.empty, CellStates.unmarked, x, y)

        board_expected = [
            [border_cell(0, 0), border_cell(1, 0), border_cell(2, 0), border_cell(3, 0)],
            [border_cell(0, 1), field_cell(1, 1), field_cell(2, 1), border_cell(3, 1)],
            [border_cell(0, 2), field_cell(1, 2), field_cell(2, 2), border_cell(3, 2)],
            [border_cell(0, 3), border_cell(1, 3), border_cell(2, 3), border_cell(3, 3)],
        ]
        self._assert2dList(board_actual, board_expected)

    def _assert2dList(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
        for i in range(len(actual)):
            self.assertEqual(len(actual[i]), len(expected[i]))
            self.assertListEqual(actual[i], expected[i])

    def test_on_incorrect_size(self):
        self.assertRaises(ValueError, lambda: generate_empty_board(-1))

    def test_on_large_size(self):
        self.assertRaises(ValueError, lambda: generate_empty_board(999999999999999999999))


if __name__ == '__main__':
    unittest.main()
