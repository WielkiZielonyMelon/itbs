import pytest

from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.mountain import Mountain
from src.game_objects.vek import Firefly
from src.helpers.get_possible_moves import get_possible_moves


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
    board.apply_web((-1, -1), pos)
    moves = get_possible_moves(board, pos)
    assert moves == []


@pytest.mark.parametrize("pos_start, mobility, pos_block, expected_moves",
                         [((0, 0), 2, (1, 0), [(0, 1), (1, 1), (0, 2)]),
                          ((0, 0), 2, (0, 1), [(1, 0), (1, 1), (2, 0)]),
                          ((7, 0), 2, (6, 0), [(7, 1), (7, 2), (6, 1)]),
                          ((7, 0), 2, (7, 1), [(6, 0), (5, 0), (6, 1)]),
                          ((7, 7), 2, (6, 7), [(7, 6), (7, 5), (6, 6)]),
                          ((7, 7), 2, (7, 6), [(6, 7), (5, 7), (6, 6)]),
                          ((0, 7), 2, (1, 7), [(0, 6), (0, 5), (1, 6)]),
                          ((0, 7), 2, (0, 6), [(1, 7), (2, 7), (1, 6)])])
def test_expected_moves_with_blocker_vek(pos_start, mobility, pos_block, expected_moves):
    board = Board()
    mech = CombatMech()
    mech._moves = mobility
    vek = Firefly()

    board[pos_start].set_object(mech)
    board.apply_web(pos_block, pos_start)
    board[pos_block].set_object(vek)
    moves = get_possible_moves(board, pos_start)
    assert moves == []


@pytest.mark.parametrize("pos_start, mobility, pos_block, expected_moves",
                         [((0, 0), 2, (1, 0), [(0, 1), (1, 1), (0, 2), (2, 0)]),
                          ((0, 0), 2, (0, 1), [(1, 0), (1, 1), (2, 0), (0, 2)]),
                          ((7, 0), 2, (6, 0), [(7, 1), (7, 2), (6, 1), (5, 0)]),
                          ((7, 0), 2, (7, 1), [(6, 0), (5, 0), (6, 1), (7, 2)]),
                          ((7, 7), 2, (6, 7), [(7, 6), (7, 5), (6, 6), (5, 7)]),
                          ((7, 7), 2, (7, 6), [(6, 7), (5, 7), (6, 6), (7, 5)]),
                          ((0, 7), 2, (1, 7), [(0, 6), (0, 5), (1, 6), (2, 7)]),
                          ((0, 7), 2, (0, 6), [(1, 7), (2, 7), (1, 6), (0, 5)])])
def test_expected_moves_with_blocker_mech(pos_start, mobility, pos_block, expected_moves):
    board = Board()
    mech = CombatMech()
    mech._moves = mobility
    mech_blocker = CombatMech()

    board[pos_start].set_object(mech)
    board.apply_web(pos_block, pos_start)
    board[pos_block].set_object(mech_blocker)
    moves = get_possible_moves(board, pos_start)
    assert moves == []


@pytest.mark.parametrize("blocker, exp_moves",
                         [(CombatMech, [(0, 0), (2, 0), (3, 1), (0, 2), (2, 2), (1, 3)]),
                          (Firefly, []),
                          (Mountain, [])])
def test_2_move_1_1_blocked(blocker, exp_moves):
    mobility = 2
    board = Board()
    mech = CombatMech()
    mech._moves = mobility

    pos_start = (1, 1)
    pos_block_0 = (0, 1)
    pos_block_1 = (2, 1)
    pos_block_2 = (1, 0)
    pos_block_3 = (1, 2)
    board[pos_start].set_object(mech)
    board.apply_web(pos_block_0, pos_start)
    board[pos_block_0].set_object(blocker())
    board[pos_block_1].set_object(blocker())
    board[pos_block_2].set_object(blocker())
    board[pos_block_3].set_object(blocker())
    moves = get_possible_moves(board, pos_start)
    assert moves == []


def test_moves_with_blocked_mech():
    board = Board()
    mech00 = CombatMech()
    mech00_pos = (0, 0)
    mech01 = CombatMech()
    mech01_pos = (1, 0)

    board[mech00_pos].set_object(mech00)
    board.apply_web(mech01_pos, mech00_pos)
    board[mech01_pos].set_object(mech01)
    board.apply_web(mech00_pos, mech01_pos)
    board[(0, 1)].set_object(Mountain())
    board[(1, 1)].set_object(Mountain())
    board[(2, 1)].set_object(Mountain())
    board[(3, 0)].set_object(Mountain())
    board[(3, 1)].set_object(Mountain())

    moves = get_possible_moves(board, mech00_pos)
    assert moves == []

    moves = get_possible_moves(board, mech01_pos)
    assert moves == []
