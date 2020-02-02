import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import ChasmTile, WaterTile, AcidTile, ForestTile, FrozenAcidTile, DamagedIceTile, \
    IceTile, ForestFireTile
from src.game_objects.vek import BlastPsion, Spiderling
from src.game_objects.weapons.push import Push


@pytest.mark.parametrize("pos, direction",
                         [((1, 0), (1, 0)),
                          ((0, 1), (0, 1)),
                          ((6, 0), (-1, 0)),
                          ((7, 1), (0, 1)),
                          ((7, 6), (0, -1)),
                          ((6, 7), (-1, 0)),
                          ((0, 6), (0, -1)),
                          ((1, 7), (1, 0))])
def test_push_empty_tile(pos, direction):
    board = Board()

    attack = Attack(attacker=pos, weapon=Push(), vector=direction)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 0


@pytest.mark.parametrize("before_push, direction, after_push",
                         [((1, 0), (1, 0), (2, 0)),
                          ((0, 1), (0, 1), (0, 2)),
                          ((6, 0), (-1, 0), (5, 0)),
                          ((7, 1), (0, 1), (7, 2)),
                          ((7, 6), (0, -1), (7, 5)),
                          ((6, 7), (-1, 0), (5, 7)),
                          ((0, 6), (0, -1), (0, 5)),
                          ((1, 7), (1, 0), (2, 7))])
def test_push_mech(before_push, direction, after_push):
    board = Board()
    mech = CombatMech()

    board[before_push].set_object(mech)
    attack = Attack(attacker=before_push, weapon=Push(), vector=direction)
    orig_before_push = copy.deepcopy(board[before_push])
    orig_after_push = copy.deepcopy(board[after_push])

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert original_tiles[before_push] == orig_before_push
    assert original_tiles[after_push] == orig_after_push

    assert not board[before_push].has_object()
    assert mech == board[after_push].get_object()


@pytest.mark.parametrize("before_push, direction",
                         [((0, 0), (-1, 0)),
                          ((0, 0), (0, -1)),
                          ((7, 7), (0, 1)),
                          ((7, 7), (1, 0))])
def test_push_mech_out_of_board(before_push, direction):
    board = Board()
    mech = CombatMech()

    board[before_push].set_object(mech)
    attack = Attack(attacker=before_push, weapon=Push(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 0

    assert mech == board[before_push].get_object()


def test_push_mountain():
    board = Board()
    mountain = Mountain()

    before_push = (1, 0)
    direction = (1, 0)
    board[before_push].set_object(mountain)
    attack = Attack(attacker=before_push, weapon=Push(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 0

    assert mountain == board[before_push].get_object()


@pytest.mark.parametrize("obj, push_pos, direction, block_pos",
                         [(CombatMech(), (1, 0), (1, 0), (2, 0)),
                          ])
def test_push_mech_against_object(obj, push_pos, direction, block_pos):
    board = Board()
    mech = CombatMech()

    board[push_pos].set_object(mech)
    board[block_pos].set_object(obj)

    orig_push_pos = copy.deepcopy(board[push_pos])
    orig_block_pos = copy.deepcopy(board[block_pos])

    pushed_expected_health = mech.get_health() - 1
    blocked_expected_health = obj.get_health() - 1

    attack = Attack(attacker=push_pos, weapon=Push(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_push_pos == original_tiles[push_pos]
    assert orig_block_pos == original_tiles[block_pos]

    assert mech.get_health() == pushed_expected_health
    assert obj.get_health() == blocked_expected_health


@pytest.mark.parametrize("death_tile, s05",
                         [(ChasmTile(_object=None), BlastPsion()),
                          (WaterTile(_object=None), BlastPsion()),
                          (AcidTile(_object=None), BlastPsion())])
def test_push_vek_to_death_chain_reaction(death_tile, s05):
    board = Board()
    s00 = Spiderling()
    s00_pos = (1, 0)
    board[s00_pos].set_object(s00)
    chasm0_pos = (0, 0)
    board[chasm0_pos] = death_tile

    s01 = Spiderling()
    s01_pos = (0, 1)
    board[s01_pos] = ForestTile(_object=s01)
    s02 = Spiderling()
    s02_pos = (0, 2)
    board[s02_pos] = FrozenAcidTile(_object=s02)
    s03 = Spiderling()
    s03_pos = (0, 3)
    board[s03_pos] = DamagedIceTile(_object=s03)
    s04 = Spiderling()
    s04_pos = (0, 4)
    board[s04_pos] = IceTile(_object=s04)
    s05_pos = (0, 5)
    board[s05_pos].set_object(s05)
    s05_expected_health = s05.get_health() - 1

    attack = Attack(attacker=s00_pos, weapon=Push(), vector=(-1, 0))

    orig00 = copy.deepcopy(board[s00_pos])
    orig01 = copy.deepcopy(board[s01_pos])
    orig02 = copy.deepcopy(board[s02_pos])
    orig03 = copy.deepcopy(board[s03_pos])
    orig04 = copy.deepcopy(board[s04_pos])
    orig05 = copy.deepcopy(board[s05_pos])

    orig10 = copy.deepcopy(board[(1, 0)])

    board.fill_object_position_cache()
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 7

    assert original_tiles[s00_pos] == orig00
    assert original_tiles[s01_pos] == orig01
    assert original_tiles[s02_pos] == orig02
    assert original_tiles[s03_pos] == orig03
    assert original_tiles[s04_pos] == orig04
    assert original_tiles[s05_pos] == orig05

    assert original_tiles[(1, 0)] == orig10

    assert None is board[s00_pos].get_object()
    assert None is board[s01_pos].get_object()
    assert None is board[s02_pos].get_object()
    assert None is board[s03_pos].get_object()
    assert None is board[s04_pos].get_object()
    assert s05_expected_health == board[s05_pos].get_object().get_health()

    assert isinstance(board[s01_pos], ForestFireTile)
    assert isinstance(board[s02_pos], AcidTile)
    assert isinstance(board[s03_pos], WaterTile)
    assert isinstance(board[s04_pos], DamagedIceTile)
