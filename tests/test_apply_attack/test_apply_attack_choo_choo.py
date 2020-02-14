import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import JetMech, CombatMech, ArtilleryMech, CannonMech
from src.game_objects.supply_train import SupplyTrainHead, SupplyTrainTail, SupplyTrainWreck
from src.game_objects.vek import Hornet, Firefly, ShellPsion
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
    orig_end_head_tile = copy.deepcopy(board[end_head_pos])
    orig_end_tail_tile = copy.deepcopy(board[end_tail_pos])

    attack = Attack(attacker=head_pos, weapon=ChooChoo(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 4
    assert head == board[end_head_pos].get_object()
    assert tail == board[end_tail_pos].get_object()
    assert original_tiles[head_pos] == orig_head_tile
    assert original_tiles[tail_pos] == orig_tail_tile
    assert original_tiles[end_head_pos] == orig_end_head_tile
    assert original_tiles[end_tail_pos] == orig_end_tail_tile


@pytest.mark.parametrize("head_pos, tail_pos, direction, vek_pos",
                         [((0, 1), (0, 0), (0, 1), (0, 2)),
                          ((1, 0), (0, 0), (1, 0), (2, 0)),
                          ((0, 6), (0, 7), (0, -1), (0, 5)),
                          ((6, 0), (7, 0), (-1, 0), (5, 0)),
                          ((6, 1), (7, 1), (-1, 0), (5, 1)),
                          ((1, 6), (1, 7), (0, -1), (1, 5)),
                          ((6, 6), (7, 6), (-1, 0), (5, 6)),
                          ((6, 6), (6, 7), (0, -1), (6, 5))])
@pytest.mark.parametrize("vek",
                         [Hornet,
                          Firefly,
                          ShellPsion])
def test_apply_choo_choo_obstructed_with_vek_0_away(head_pos, tail_pos, direction, vek, vek_pos):
    board = Board()
    head = SupplyTrainHead()
    tail = SupplyTrainTail()
    vek = vek()

    board[head_pos].set_object(head)
    board[tail_pos].set_object(tail)
    board[vek_pos].set_object(vek)
    board.fill_object_position_cache()

    orig_head_tile = copy.deepcopy(board[head_pos])
    orig_tail_tile = copy.deepcopy(board[tail_pos])
    orig_vek_tile = copy.deepcopy(board[vek_pos])

    attack = Attack(attacker=head_pos, weapon=ChooChoo(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 3
    assert isinstance(board[head_pos].get_object(), SupplyTrainWreck)
    assert isinstance(board[tail_pos].get_object(), SupplyTrainWreck)
    assert board[vek_pos].get_object() is None
    assert original_tiles[head_pos] == orig_head_tile
    assert original_tiles[tail_pos] == orig_tail_tile
    assert original_tiles[vek_pos] == orig_vek_tile


@pytest.mark.parametrize("head_pos, tail_pos, direction, mech_pos",
                         [((0, 1), (0, 0), (0, 1), (0, 2)),
                          ((1, 0), (0, 0), (1, 0), (2, 0)),
                          ((0, 6), (0, 7), (0, -1), (0, 5)),
                          ((6, 0), (7, 0), (-1, 0), (5, 0)),
                          ((6, 1), (7, 1), (-1, 0), (5, 1)),
                          ((1, 6), (1, 7), (0, -1), (1, 5)),
                          ((6, 6), (7, 6), (-1, 0), (5, 6)),
                          ((6, 6), (6, 7), (0, -1), (6, 5))])
@pytest.mark.parametrize("mech",
                         [CombatMech,
                          ArtilleryMech,
                          JetMech])
def test_apply_choo_choo_obstructed_with_mech_0_away(head_pos, tail_pos, direction, mech, mech_pos):
    board = Board()
    head = SupplyTrainHead()
    tail = SupplyTrainTail()
    mech = mech()

    board[head_pos].set_object(head)
    board[tail_pos].set_object(tail)
    board[mech_pos].set_object(mech)
    board.fill_object_position_cache()

    orig_head_tile = copy.deepcopy(board[head_pos])
    orig_tail_tile = copy.deepcopy(board[tail_pos])
    orig_mech_tile = copy.deepcopy(board[mech_pos])

    attack = Attack(attacker=head_pos, weapon=ChooChoo(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 3
    assert isinstance(board[head_pos].get_object(), SupplyTrainWreck)
    assert isinstance(board[tail_pos].get_object(), SupplyTrainWreck)
    assert board[mech_pos].get_object().get_id() == mech.get_id()
    assert original_tiles[head_pos] == orig_head_tile
    assert original_tiles[tail_pos] == orig_tail_tile
    assert original_tiles[mech_pos] == orig_mech_tile
    assert mech.get_health() == 0


@pytest.mark.parametrize("head_pos, tail_pos, direction, vek_pos, end_head_pos",
                         [((0, 1), (0, 0), (0, 1), (0, 3), (0, 2)),
                          ((1, 0), (0, 0), (1, 0), (3, 0), (2, 0)),
                          ((0, 6), (0, 7), (0, -1), (0, 4), (0, 5)),
                          ((6, 0), (7, 0), (-1, 0), (4, 0), (5, 0)),
                          ((6, 1), (7, 1), (-1, 0), (4, 1), (5, 1)),
                          ((1, 6), (1, 7), (0, -1), (1, 4), (1, 5)),
                          ((6, 6), (7, 6), (-1, 0), (4, 6), (5, 6)),
                          ((6, 6), (6, 7), (0, -1), (6, 4), (6, 5))])
@pytest.mark.parametrize("vek",
                         [Hornet,
                          Firefly,
                          ShellPsion])
def test_apply_choo_choo_obstructed_with_vek_1_away(head_pos, tail_pos, direction, vek, vek_pos, end_head_pos):
    board = Board()
    head = SupplyTrainHead()
    tail = SupplyTrainTail()
    vek = vek()

    board[head_pos].set_object(head)
    board[tail_pos].set_object(tail)
    board[vek_pos].set_object(vek)
    board.fill_object_position_cache()

    orig_head_tile = copy.deepcopy(board[head_pos])
    orig_tail_tile = copy.deepcopy(board[tail_pos])
    orig_end_head_tile = copy.deepcopy(board[end_head_pos])
    orig_vek_tile = copy.deepcopy(board[vek_pos])

    attack = Attack(attacker=head_pos, weapon=ChooChoo(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 4
    assert original_tiles[head_pos] == orig_head_tile
    assert original_tiles[tail_pos] == orig_tail_tile
    assert original_tiles[end_head_pos] == orig_end_head_tile
    assert original_tiles[vek_pos] == orig_vek_tile

    assert isinstance(board[end_head_pos].get_object(), SupplyTrainWreck)
    assert isinstance(board[head_pos].get_object(), SupplyTrainWreck)
    assert board[vek_pos].get_object() is None
    assert board[tail_pos].get_object() is None


@pytest.mark.parametrize("head_pos, tail_pos, direction, mech_pos, end_head_pos",
                         [((0, 1), (0, 0), (0, 1), (0, 3), (0, 2)),
                          ((1, 0), (0, 0), (1, 0), (3, 0), (2, 0)),
                          ((0, 6), (0, 7), (0, -1), (0, 4), (0, 5)),
                          ((6, 0), (7, 0), (-1, 0), (4, 0), (5, 0)),
                          ((6, 1), (7, 1), (-1, 0), (4, 1), (5, 1)),
                          ((1, 6), (1, 7), (0, -1), (1, 4), (1, 5)),
                          ((6, 6), (7, 6), (-1, 0), (4, 6), (5, 6)),
                          ((6, 6), (6, 7), (0, -1), (6, 4), (6, 5))])
@pytest.mark.parametrize("mech",
                         [CannonMech,
                          JetMech,
                          ArtilleryMech])
def test_apply_choo_choo_obstructed_with_mech_1_away(head_pos, tail_pos, direction, mech, mech_pos, end_head_pos):
    board = Board()
    head = SupplyTrainHead()
    tail = SupplyTrainTail()
    mech = mech()

    board[head_pos].set_object(head)
    board[tail_pos].set_object(tail)
    board[mech_pos].set_object(mech)
    board.fill_object_position_cache()

    orig_head_tile = copy.deepcopy(board[head_pos])
    orig_tail_tile = copy.deepcopy(board[tail_pos])
    orig_end_head_tile = copy.deepcopy(board[end_head_pos])
    orig_mech_tile = copy.deepcopy(board[mech_pos])

    attack = Attack(attacker=head_pos, weapon=ChooChoo(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 4
    assert original_tiles[head_pos] == orig_head_tile
    assert original_tiles[tail_pos] == orig_tail_tile
    assert original_tiles[end_head_pos] == orig_end_head_tile
    assert original_tiles[mech_pos] == orig_mech_tile

    assert isinstance(board[end_head_pos].get_object(), SupplyTrainWreck)
    assert isinstance(board[head_pos].get_object(), SupplyTrainWreck)
    assert board[mech_pos].get_object().get_id() == mech.get_id()
    assert board[mech_pos].get_object().get_health() == 0
    assert board[tail_pos].get_object() is None
