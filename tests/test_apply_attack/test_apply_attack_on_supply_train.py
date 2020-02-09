import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.supply_train import SupplyTrainHead, SupplyTrainTail, SupplyTrainWreck
from src.game_objects.vek import Hornet, AlphaHornet
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("train_tail_pos, train_head_pos, attacker_pos, direction",
                         [((0, 0), (0, 1), (0, 2), (0, -1)),
                          ((0, 0), (0, 1), (1, 1), (-1, 0)),
                          ((0, 0), (1, 0), (2, 0), (-1, 0)),
                          ((0, 0), (1, 0), (1, 1), (0, -1)),
                          ((0, 7), (0, 6), (0, 5), (0, 1)),
                          ((0, 7), (0, 6), (1, 6), (-1, 0)),
                          ((0, 7), (1, 7), (2, 7), (-1, 0)),
                          ((0, 7), (1, 7), (1, 6), (0, 1)),
                          ((7, 7), (6, 7), (5, 7), (1, 0)),
                          ((7, 0), (6, 0), (5, 0), (1, 0))])
@pytest.mark.parametrize("attacker, weapon",
                         [(CombatMech, TitanFist),
                          (Hornet, Stinger),
                          (AlphaHornet, LaunchingStinger)])
def test_melee_weapon_on_supply_train(train_tail_pos, train_head_pos, attacker_pos, direction, attacker, weapon):
    board = Board()
    train_head = SupplyTrainHead()
    train_tail = SupplyTrainTail()
    board[train_head_pos].set_object(train_head)
    board[train_tail_pos].set_object(train_tail)

    attacker = attacker()
    board[attacker_pos].set_object(attacker)
    board.fill_object_position_cache()

    orig_head = copy.deepcopy(board[train_head_pos])
    orig_tail = copy.deepcopy(board[train_tail_pos])
    attack = Attack(attacker=attacker.get_id(), weapon=weapon(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert original_tiles[train_head_pos] == orig_head
    assert original_tiles[train_tail_pos] == orig_tail

    wreck_head = board[train_head_pos].get_object()
    wreck_tail = board[train_tail_pos].get_object()
    assert wreck_head.get_health() == 1
    assert wreck_tail.get_health() == 1
    assert isinstance(wreck_head, SupplyTrainWreck)
    assert isinstance(wreck_tail, SupplyTrainWreck)
