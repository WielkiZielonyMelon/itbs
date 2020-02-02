import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.tiles.tile import FireTile, DamagedIceTile, IceTile, ForestTile, FrozenAcidTile, ForestFireTile, \
    WaterTile, DamagedFrozenAcidTile, ChasmTile, AcidTile, AcidPool, GroundTile
from src.game_objects.vek import Firefly, BlastPsion, Spiderling, Hornet, FireflyLeader
from src.game_objects.weapons.move import Move


def test_simple_move():
    obj = CombatMech()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after == obj


def test_simple_move_to_acid_pool():
    obj = CombatMech()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)
    board[pos_after] = AcidPool(_object=None)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after.is_on_acid()
    assert isinstance(board[pos_after], GroundTile)


def test_simple_move_flying_vek_to_acid_pool():
    obj = Hornet()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)
    board[pos_after] = AcidPool(_object=None)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after.is_on_acid()
    assert isinstance(board[pos_after], GroundTile)


def test_simple_move_acided_mech_to_water():
    obj = CombatMech()
    obj.set_acid()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)
    board[pos_after] = WaterTile(_object=None)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after.is_on_acid()
    assert isinstance(board[pos_after], AcidTile)


def test_simple_move_acided_vek_to_water():
    obj = Firefly()
    obj.set_acid()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)
    board[pos_after] = WaterTile(_object=None)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after is None
    assert isinstance(board[pos_after], AcidTile)


def test_simple_move_acided_masive_vek_to_water():
    obj = FireflyLeader()
    obj.set_acid()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)
    board[pos_after] = WaterTile(_object=None)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after.is_on_acid()
    assert isinstance(board[pos_after], AcidTile)


def test_move_over_fire():
    obj = CombatMech()
    pos = (0, 0)
    pos_after = (1, 0)
    board = Board()
    board[pos].set_object(obj)
    board[pos_after] = FireTile(_object=None)

    orig_tile_pos = copy.deepcopy(board[pos])
    orig_tile_pos_after = copy.deepcopy(board[pos_after])

    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=pos_after)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 2
    assert original_tiles[pos] == orig_tile_pos
    assert original_tiles[pos].get_object().is_on_fire() is False
    assert original_tiles[pos_after] == orig_tile_pos_after

    obj_before = board[pos].get_object()
    assert obj_before is None
    obj_after = board[pos_after].get_object()
    assert obj_after == obj
    assert obj_after.is_on_fire()


@pytest.mark.parametrize("psion0",
                         [(BlastPsion())])
def test_move_vek_to_death_with_blast_psion_present(psion0):
    vek0 = Firefly()
    vek0_pos = (5, 3)
    vek0_pos_death = (5, 5)

    forest0_pos = (5, 6)
    ice_tile0_pos = (5, 4)
    damaged_ice_tile0_pos = (4, 5)
    frozen_acid0_pos = (6, 5)

    psion0_pos = (0, 0)

    board = Board()
    board[vek0_pos].set_object(vek0)
    board[vek0_pos_death] = ChasmTile(_object=None)
    board[forest0_pos] = ForestTile(_object=None)
    board[ice_tile0_pos] = IceTile(_object=None)
    board[damaged_ice_tile0_pos] = DamagedIceTile(_object=None)
    board[frozen_acid0_pos] = FrozenAcidTile(_object=None)
    board[psion0_pos].set_object(psion0)

    orig_vek0 = copy.deepcopy(board[vek0_pos])
    orig_vek0_pos_death = copy.deepcopy(board[vek0_pos_death])
    orig_forest0 = copy.deepcopy(board[forest0_pos])
    orig_ice_tile0 = copy.deepcopy(board[ice_tile0_pos])
    orig_damaged_ice_tile0 = copy.deepcopy(board[damaged_ice_tile0_pos])
    orig_frozen_acid0 = copy.deepcopy(board[frozen_acid0_pos])

    board.fill_object_position_cache()
    attack = Attack(attacker=vek0.get_id(), weapon=Move(), vector=vek0_pos_death)
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 6
    assert original_tiles[vek0_pos] == orig_vek0
    assert original_tiles[vek0_pos_death] == orig_vek0_pos_death
    assert original_tiles[forest0_pos] == orig_forest0
    assert original_tiles[ice_tile0_pos] == orig_ice_tile0
    assert original_tiles[damaged_ice_tile0_pos] == orig_damaged_ice_tile0
    assert original_tiles[frozen_acid0_pos] == orig_frozen_acid0

    obj_before = board[vek0_pos].get_object()
    assert obj_before is None
    obj_after = board[vek0_pos_death].get_object()
    assert obj_after is None

    assert isinstance(board[forest0_pos], ForestFireTile)
    assert isinstance(board[ice_tile0_pos], DamagedIceTile)
    assert isinstance(board[damaged_ice_tile0_pos], WaterTile)
    assert isinstance(board[frozen_acid0_pos], DamagedFrozenAcidTile)


@pytest.mark.parametrize("death_tile, s05",
                         [(ChasmTile(_object=None), BlastPsion()),
                          (WaterTile(_object=None), BlastPsion()),
                          (AcidTile(_object=None), BlastPsion())])
def test_move_chain_reaction(death_tile, s05):
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

    board.fill_object_position_cache()
    attack = Attack(attacker=s00.get_id(), weapon=Move(), vector=chasm0_pos)

    orig00 = copy.deepcopy(board[s00_pos])
    orig01 = copy.deepcopy(board[s01_pos])
    orig02 = copy.deepcopy(board[s02_pos])
    orig03 = copy.deepcopy(board[s03_pos])
    orig04 = copy.deepcopy(board[s04_pos])
    orig05 = copy.deepcopy(board[s05_pos])

    orig10 = copy.deepcopy(board[(1, 0)])

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
