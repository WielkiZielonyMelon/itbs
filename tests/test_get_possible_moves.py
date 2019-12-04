import pytest
import unittest

from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.helpers.get_possible_moves import get_possible_moves


def test_no_mech():
    board = Board()
    moves = get_possible_moves(board, None)
    expected_moves = []
    assert moves == expected_moves


@pytest.mark.parametrize("pos, mobility,expected_moves",
                         [((0, 0), 0, []),
                          ((0, 0), 1, [(0, 1), (1, 0)]),
                          ((0, 0), 2, [(0, 1), (1, 0), (1, 1), (2, 0), (0, 2)]),
                          ((7, 0), 2, [(7, 1), (6, 0), (6, 1), (5, 0), (7, 2)]),
                          ((7, 7), 2, [(7, 6), (6, 7), (6, 6), (5, 7), (7, 5)]),
                          ((0, 7), 2, [(0, 6), (1, 7), (1, 6), (2, 7), (0, 5)])])
def test_expected_moves(pos, mobility, expected_moves):
    board = Board()
    mech = CombatMech()
    mech._moves = mobility

    board[pos].set_object(mech)
    moves = get_possible_moves(board, mech)
    unittest.TestCase().assertCountEqual(moves, expected_moves)


@pytest.mark.parametrize("pos_start, mobility, pos_block, expected_moves",
                         [((0, 0), 2, (1, 0), [(0, 1), (1, 1), (0, 2)]),
                          ((0, 0), 2, (0, 1), [(1, 0), (1, 1), (2, 0)]),
                          ((7, 0), 2, (6, 0), [(7, 1), (7, 2), (6, 1)]),
                          ((7, 0), 2, (7, 1), [(6, 0), (5, 0), (6, 1)]),
                          ((7, 7), 2, (6, 7), [(7, 6), (7, 5), (6, 6)]),
                          ((7, 7), 2, (7, 6), [(6, 7), (5, 7), (6, 6)]),
                          ((0, 7), 2, (1, 7), [(0, 6), (0, 5), (1, 6)]),
                          ((0, 7), 2, (0, 6), [(1, 7), (2, 7), (1, 6)])])
def test_expected_moves_with_blocker(pos_start, mobility, pos_block, expected_moves):
    board = Board()
    mech = CombatMech()
    mech._moves = mobility
    mech_blocker = CombatMech()

    board[pos_start].set_object(mech)
    board[pos_block].set_object(mech_blocker)
    moves = get_possible_moves(board, mech)
    unittest.TestCase().assertCountEqual(moves, expected_moves)


def test_2_move_1_1_blocked_fully():
    mobility = 2
    board = Board()
    mech = CombatMech()
    mech._moves = mobility
    mech_blocker = CombatMech()

    pos_start = (1, 1)
    pos_block_0 = (0, 1)
    pos_block_1 = (2, 1)
    pos_block_2 = (1, 0)
    pos_block_3 = (1, 2)
    board[pos_start].set_object(mech)
    board[pos_block_0].set_object(mech_blocker)
    board[pos_block_1].set_object(mech_blocker)
    board[pos_block_2].set_object(mech_blocker)
    board[pos_block_3].set_object(mech_blocker)
    moves = get_possible_moves(board, mech)
    expected_moves = []
    unittest.TestCase().assertCountEqual(moves, expected_moves)
