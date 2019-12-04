import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CannonMech, CombatMech
from src.game_objects.tiles.tile import ForestTile, ForestFireTile, SandTile, GroundTile, ChasmTile, WaterTile, \
    AcidTile, FrozenAcidTile, DamagedIceTile, IceTile
from src.game_objects.vek import BlastPsion, Spiderling
from src.game_objects.weapons.taurus_cannon import TaurusCannon


def test_single_taurus_cannon():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)
    mech0_expected_health = mech0.get_health() - 2
    board[mech0_pos].set_object(mech0)

    cannon0 = CannonMech()
    cannon0_pos = (7, 0)
    cannon0_attack_vector = (-1, 0)
    cannon0_expected_health = cannon0.get_health()
    board[cannon0_pos].set_object(cannon0)

    orig_00 = copy.deepcopy(board[mech0_pos])
    attack = Attack(attacker=cannon0.get_id(), weapon=TaurusCannon(),
                    vector=cannon0_attack_vector)

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_00 == original_tiles[mech0_pos]

    assert mech0_expected_health == mech0.get_health()
    assert cannon0_expected_health == cannon0.get_health()


def test_single_taurus_cannon_push_object():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (1, 0)
    mech0_pos_after_attack = (0, 0)
    mech0_expected_health = mech0.get_health() - 2
    board[mech0_pos].set_object(mech0)

    cannon0 = CannonMech()
    cannon0_pos = (7, 0)
    cannon0_attack_vector = (-1, 0)
    cannon0_expected_health = cannon0.get_health()
    board[cannon0_pos].set_object(cannon0)

    orig_10 = copy.deepcopy(board[mech0_pos])
    orig_00 = copy.deepcopy(board[mech0_pos_after_attack])
    attack = Attack(attacker=cannon0.get_id(), weapon=TaurusCannon(),
                    vector=cannon0_attack_vector)

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_00 == original_tiles[mech0_pos_after_attack]
    assert orig_10 == original_tiles[mech0_pos]

    assert mech0_expected_health == mech0.get_health()
    assert cannon0_expected_health == cannon0.get_health()
    assert board[mech0_pos].get_object() is None
    assert board[mech0_pos_after_attack].get_object().get_health() == mech0_expected_health


def test_single_taurus_cannon_on_edge_forest_tile():
    board = Board()
    forest_pos = (0, 0)
    board[forest_pos] = ForestTile(_object=None)

    cannon0 = CannonMech()
    cannon0_pos = (7, 0)
    cannon0_attack_vector = (-1, 0)
    board[cannon0_pos].set_object(cannon0)

    orig_00 = copy.deepcopy(board[forest_pos])
    attack = Attack(attacker=cannon0.get_id(), weapon=TaurusCannon(),
                    vector=cannon0_attack_vector)

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_00 == original_tiles[forest_pos]

    assert isinstance(board[forest_pos], ForestFireTile)


def test_single_taurus_cannon_on_edge_sand_tile():
    board = Board()
    sand_pos = (0, 0)
    board[sand_pos] = SandTile(_object=None)

    cannon0 = CannonMech()
    cannon0_pos = (7, 0)
    cannon0_attack_vector = (-1, 0)
    board[cannon0_pos].set_object(cannon0)

    orig00 = copy.deepcopy(board[sand_pos])

    attack = Attack(attacker=cannon0.get_id(), weapon=TaurusCannon(),
                    vector=cannon0_attack_vector)

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig00 == original_tiles[sand_pos]

    assert isinstance(board[sand_pos], GroundTile)
    assert board[sand_pos].has_smoke()


def test_single_taurus_cannon_mech_on_forest_tile_in_middle():
    board = Board()

    cannon0 = CannonMech()
    cannon0_pos = (7, 0)
    cannon0_attack_vector = (-1, 0)
    board[cannon0_pos].set_object(cannon0)

    mech0 = CombatMech()
    mech0_expected_health = mech0.get_health() - 2
    forest0_pos = (3, 0)
    pos_after = (2, 0)
    board[forest0_pos] = ForestTile(_object=mech0)

    orig30 = copy.deepcopy(board[forest0_pos])
    orig20 = copy.deepcopy(board[pos_after])
    cannon0_attack = Attack(attacker=cannon0.get_id(), weapon=TaurusCannon(),
                            vector=cannon0_attack_vector)

    original_tiles = apply_attack(board, cannon0_attack)
    assert len(original_tiles) == 2
    assert orig30 == original_tiles[forest0_pos]
    assert orig20 == original_tiles[pos_after]

    assert isinstance(board[forest0_pos], ForestFireTile)
    assert mech0_expected_health == mech0.get_health()
    assert not mech0.is_on_fire()


def test_taurus_cannon_attack_neighbour_vek():
    board = Board()

    cannon0 = CannonMech()
    cannon0_pos = (2, 0)
    cannon0_attack_vector = (1, 0)
    board[cannon0_pos].set_object(cannon0)

    mech0 = CombatMech()
    mech0_pos = (3, 0)
    board[mech0_pos].set_object(mech0)

    mech1 = CombatMech()
    mech1_pos = (4, 0)
    board[mech1_pos].set_object(mech1)

    exp_mech1_health = mech0.get_health() - 1

    orig30 = copy.deepcopy(board[mech0_pos])
    orig40 = copy.deepcopy(board[mech1_pos])

    cannon0_attack = Attack(attacker=cannon0.get_id(), weapon=TaurusCannon(),
                            vector=cannon0_attack_vector)

    original_tiles = apply_attack(board, cannon0_attack)

    assert len(original_tiles) == 2
    assert orig30 == original_tiles[mech0_pos]
    assert orig40 == original_tiles[mech1_pos]

    assert board[mech0_pos].get_object() is None
    assert board[mech1_pos].get_object() == mech1
    assert exp_mech1_health == mech1.get_health()


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
    mech0 = CombatMech()
    mech0_pos = (2, 0)
    board[mech0_pos].set_object(mech0)

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

    attack = Attack(attacker=mech0.get_id(), weapon=TaurusCannon(), vector=(-1, 0))

    orig00 = copy.deepcopy(board[s00_pos])
    orig01 = copy.deepcopy(board[s01_pos])
    orig02 = copy.deepcopy(board[s02_pos])
    orig03 = copy.deepcopy(board[s03_pos])
    orig04 = copy.deepcopy(board[s04_pos])
    orig05 = copy.deepcopy(board[s05_pos])

    orig10 = copy.deepcopy(board[(1, 0)])
    orig11 = copy.deepcopy(board[(1, 1)])
    orig12 = copy.deepcopy(board[(1, 2)])
    orig13 = copy.deepcopy(board[(1, 3)])
    orig14 = copy.deepcopy(board[(1, 4)])

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 11

    assert original_tiles[s00_pos] == orig00
    assert original_tiles[s01_pos] == orig01
    assert original_tiles[s02_pos] == orig02
    assert original_tiles[s03_pos] == orig03
    assert original_tiles[s04_pos] == orig04
    assert original_tiles[s05_pos] == orig05

    assert original_tiles[(1, 0)] == orig10
    assert original_tiles[(1, 1)] == orig11
    assert original_tiles[(1, 2)] == orig12
    assert original_tiles[(1, 3)] == orig13
    assert original_tiles[(1, 4)] == orig14

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
