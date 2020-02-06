import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.supply_train import SupplyTrainHead, SupplyTrainTail
from src.game_objects.weapons.choo_choo import ChooChoo


@pytest.mark.parametrize("head_pos, tail_pos, direction, end_head_pos, end_tail_pos",
                         [((0, 1), (0, 0), (0, 1), (0, 3), (0, 2)),
                          ((1, 0), (0, 0), (1, 0), (3, 0), (2, 0)),
                          ((0, 6), (0, 7), (0, -1), (0, 4), (0, 5)),
                          ((6, 0), (7, 0), (-1, 0), (4, 0), (5, 0)),
                          ((6, 1), (7, 1), (-1, 0), (4, 1), (5, 1)),
                          ((1, 6), (1, 7), (0, -1), (1, 4), (1, 5)),
                          ((6, 6), (7, 6), (-1, 0), (4, 6), (5, 6)),
                          ((6, 6), (6, 7), (0, -1), (6, 4), (6, 5))])
def test_apply_choo_choo_unobstructed(head_pos, tail_pos, direction, end_head_pos, end_tail_pos):
    board = Board()
    head = SupplyTrainHead()
    tail = SupplyTrainTail()

    board[head_pos].set_object(head)
    board[tail_pos].set_object(tail)
    board.fill_object_position_cache()
    orig_head_tile = copy.deepcopy(board[head_pos])
    orig_tail_tile = copy.deepcopy(board[tail_pos])

    attack = Attack(attacker=head_pos, weapon=ChooChoo(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert head == board[end_head_pos].get_object()
    assert tail == board[end_tail_pos].get_object()
    assert original_tiles[head_pos] == orig_head_tile
    assert original_tiles[tail_pos] == orig_tail_tile
