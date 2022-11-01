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


class UpdatePiecesTests(TestCase):
    def test_updating_cell(self, x=1, y=1):
        board = Board(2)
        board.place_piece(Colors.black, 0, 0)
        cell = board.get_cell(x, y)
        board.update_cell(cell, CellTypes.white)
        cell_actual = board.get_cell(x, y)
        cell_expected = Cell(CellTypes.white, CellStates.unmarked, 1, 1)
        self.assertEqual(cell_actual, cell_expected)


class CapturePiecesTests(TestCase):
    def test_capturing_one_piece(self):
        board = Board(3)
        board.place_piece(Colors.white, 1, 1)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 0, 1)
        board.place_piece(Colors.black, 2, 1)
        board.place_piece(Colors.black, 1, 2)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0), BORDER(4, 0)],
            [BORDER(0, 1), EMPTY(1, 1), BLACK(2, 1), EMPTY(3, 1), BORDER(4, 1)],
            [BORDER(0, 2), BLACK(1, 2), EMPTY(2, 2), BLACK(3, 2), BORDER(4, 2)],
            [BORDER(0, 3), EMPTY(1, 3), BLACK(2, 3), EMPTY(3, 3), BORDER(4, 3)],
            [BORDER(0, 4), BORDER(1, 4), BORDER(2, 4), BORDER(3, 4), BORDER(4, 4)]
        ]
        _assert_2d_list(self, board.board, board_expected)

    def test_capturing_group(self):
        board = Board(3)
        board.place_piece(Colors.white, 0, 0)
        board.place_piece(Colors.white, 0, 1)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 1, 1)
        board.place_piece(Colors.black, 0, 2)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0), BORDER(4, 0)],
            [BORDER(0, 1), EMPTY(1, 1), BLACK(2, 1), EMPTY(3, 1), BORDER(4, 1)],
            [BORDER(0, 2), EMPTY(1, 2), BLACK(2, 2), EMPTY(3, 2), BORDER(4, 2)],
            [BORDER(0, 3), BLACK(1, 3), EMPTY(2, 3), EMPTY(3, 3), BORDER(4, 3)],
            [BORDER(0, 4), BORDER(1, 4), BORDER(2, 4), BORDER(3, 4), BORDER(4, 4)]
        ]
        _assert_2d_list(self, board.board, board_expected)

    def test_capturing_in_suicide_situation(self):
        board = Board(4)
        board.place_piece(Colors.white, 1, 0)
        board.place_piece(Colors.white, 0, 1)
        board.place_piece(Colors.white, 2, 1)
        board.place_piece(Colors.white, 1, 2)
        board.place_piece(Colors.black, 0, 2)
        board.place_piece(Colors.black, 1, 3)
        board.place_piece(Colors.black, 2, 2)
        board.place_piece(Colors.black, 1, 1)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0), BORDER(4, 0), BORDER(5, 0)],
            [BORDER(0, 1), EMPTY(1, 1), WHITE(2, 1), EMPTY(3, 1), EMPTY(4, 1), BORDER(5, 1)],
            [BORDER(0, 2), WHITE(1, 2), BLACK(2, 2), WHITE(3, 2), EMPTY(4, 2), BORDER(5, 2)],
            [BORDER(0, 3), BLACK(1, 3), EMPTY(2, 3), BLACK(3, 3), EMPTY(4, 3), BORDER(5, 3)],
            [BORDER(0, 4), EMPTY(1, 4), BLACK(2, 4), EMPTY(3, 4), EMPTY(4, 4), BORDER(5, 4)],
            [BORDER(0, 5), BORDER(1, 5), BORDER(2, 5), BORDER(3, 5), BORDER(4, 5), BORDER(5, 5)]
        ]
        _assert_2d_list(self, board.board, board_expected)


class RuleOfSuicideTests(TestCase):
    def test_suicide_rule(self):
        board = Board(3)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 0, 1)
        board.place_piece(Colors.black, 2, 1)
        board.place_piece(Colors.black, 1, 2)
        board.place_piece(Colors.white, 1, 1)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0), BORDER(4, 0)],
            [BORDER(0, 1), EMPTY(1, 1), BLACK(2, 1), EMPTY(3, 1), BORDER(4, 1)],
            [BORDER(0, 2), BLACK(1, 2), EMPTY(2, 2), BLACK(3, 2), BORDER(4, 2)],
            [BORDER(0, 3), EMPTY(1, 3), BLACK(2, 3), EMPTY(3, 3), BORDER(4, 3)],
            [BORDER(0, 4), BORDER(1, 4), BORDER(2, 4), BORDER(3, 4), BORDER(4, 4)]
        ]
        _assert_2d_list(self, board.board, board_expected)


class RuleOfKOTests(TestCase):
    def test_ko_rule(self):
        board = Board(4)
        board.place_piece(Colors.white, 1, 0)
        board.place_piece(Colors.white, 0, 1)
        board.place_piece(Colors.white, 2, 1)
        board.place_piece(Colors.white, 1, 2)
        board.place_piece(Colors.black, 0, 2)
        board.place_piece(Colors.black, 1, 3)
        board.place_piece(Colors.black, 2, 2)
        board.place_piece(Colors.black, 1, 1)
        board.place_piece(Colors.white, 1, 2)
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0), BORDER(4, 0), BORDER(5, 0)],
            [BORDER(0, 1), EMPTY(1, 1), WHITE(2, 1), EMPTY(3, 1), EMPTY(4, 1), BORDER(5, 1)],
            [BORDER(0, 2), WHITE(1, 2), BLACK(2, 2), WHITE(3, 2), EMPTY(4, 2), BORDER(5, 2)],
            [BORDER(0, 3), BLACK(1, 3), EMPTY(2, 3), BLACK(3, 3), EMPTY(4, 3), BORDER(5, 3)],
            [BORDER(0, 4), EMPTY(1, 4), BLACK(2, 4), EMPTY(3, 4), EMPTY(4, 4), BORDER(5, 4)],
            [BORDER(0, 5), BORDER(1, 5), BORDER(2, 5), BORDER(3, 5), BORDER(4, 5), BORDER(5, 5)]
        ]
        _assert_2d_list(self, board.board, board_expected)


class CountLibertiesTests(TestCase):
    def test_counting_trivial_liberties(self):
        board = Board(3)
        board.place_piece(Colors.black, 0, 0)
        liberties_actual = sum(board.get_liberties(Colors.black), [])
        liberties_expected = [Cell(CellTypes.empty, CellStates.unmarked, 2, 1),
                              Cell(CellTypes.empty, CellStates.unmarked, 1, 2)]
        self.assertListEqual(liberties_actual, liberties_expected)

    def test_counting_complex_liberties(self):
        board = Board(3)
        board.place_piece(Colors.black, 0, 0)
        board.place_piece(Colors.black, 2, 2)
        liberties_actual = sum(board.get_liberties(Colors.black), [])
        liberties_expected = [Cell(CellTypes.empty, CellStates.unmarked, 2, 1),
                              Cell(CellTypes.empty, CellStates.unmarked, 1, 2),
                              Cell(CellTypes.empty, CellStates.unmarked, 3, 2),
                              Cell(CellTypes.empty, CellStates.unmarked, 2, 3)]
        self.assertListEqual(liberties_actual, liberties_expected)


class RestoreStatesTests(TestCase):
    def test_restoring_states(self):
        board_actual = Board(2)
        cell_a = board_actual.get_cell(1, 1)
        cell_b = board_actual.get_cell(2, 1)
        board_actual.update_cell(cell_a, None, CellStates.marked)
        board_actual.update_cell(cell_b, None, CellStates.marked)
        board_actual.restore_states()
        board_expected = [
            [BORDER(0, 0), BORDER(1, 0), BORDER(2, 0), BORDER(3, 0)],
            [BORDER(0, 1), EMPTY(1, 1), EMPTY(2, 1), BORDER(3, 1)],
            [BORDER(0, 2), EMPTY(1, 2), EMPTY(2, 2), BORDER(3, 2)],
            [BORDER(0, 3), BORDER(1, 3), BORDER(2, 3), BORDER(3, 3)],
        ]
        _assert_2d_list(self, board_actual.board, board_expected)


class CountTerritoryTests(TestCase):
    def test_counting_small_trivial_territory(self):
        board = Board(3)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 0, 1)
        board.place_piece(Colors.white, 1, 1)
        board = FinalizedBoard(board)
        territory_actual = board.count_territory(Colors.black)
        self.assertEqual(territory_actual, 1)

    def test_counting_big_trivial_territory(self):
        board = Board(4)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 0, 2)
        board.place_piece(Colors.black, 1, 2)
        board.place_piece(Colors.black, 2, 1)
        board.place_piece(Colors.white, 3, 3)
        board = FinalizedBoard(board)
        territory_actual = board.count_territory(Colors.black)
        self.assertEqual(territory_actual, 3)

    def test_counting_complex_territory(self):
        board = Board(4)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 0, 1)
        board.place_piece(Colors.black, 1, 2)
        board.place_piece(Colors.black, 2, 1)
        board.place_piece(Colors.white, 3, 3)
        board = FinalizedBoard(board)
        territory_actual = board.count_territory(Colors.black)
        self.assertEqual(territory_actual, 2)

    def test_counting_empty_territory(self):
        board = Board(3)
        board.place_piece(Colors.black, 1, 0)
        board.place_piece(Colors.black, 0, 1)
        board.place_piece(Colors.white, 1, 1)
        board = FinalizedBoard(board)
        territory_actual = board.count_territory(Colors.white)
        self.assertEqual(territory_actual, 0)


if __name__ == '__main__':
    unittest.main()
