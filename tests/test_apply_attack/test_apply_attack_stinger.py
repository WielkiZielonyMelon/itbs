import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech
from src.game_objects.tiles.tile import ForestTile, ForestFireTile, FrozenAcidTile, IceTile, DamagedFrozenAcidTile, \
    DamagedIceTile, AcidTile, WaterTile
from src.game_objects.vek import Spiderling, BlastPsion, Hornet, Firefly, ShellPsion
from src.game_objects.weapons.stinger import Stinger


def test_single_stinger():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)
    mech0_expected_health = mech0.get_health() - 1
    board[mech0_pos].set_object(mech0)
    orig_tile = copy.deepcopy(board[mech0_pos])

    vek0 = Hornet()
    vek0_pos = (1, 0)
    vek0_attack_vector = (-1, 0)
    vek0_expected_health = vek0.get_health()
    board[vek0_pos].set_object(vek0)

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    original_tiles = apply_attack(board, vek0_attack)
    assert len(original_tiles) == 1
    assert original_tiles[mech0_pos] == orig_tile

    assert mech0_expected_health == mech0.get_health()
    assert vek0_expected_health == vek0.get_health()


def test_single_stinger_on_edge():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (7, 0)
    vek0_attack_vector = (1, 0)
    vek0_expected_health = vek0.get_health()
    board[vek0_pos] = ForestTile(_object=vek0)

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    apply_attack(board, vek0_attack)

    assert vek0_expected_health == vek0.get_health()
    assert isinstance(board[vek0_pos], ForestTile)


def test_single_stinger_forest_tile():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (7, 0)
    vek0_attack_vector = (-1, 0)
    vek0_expected_health = vek0.get_health()
    board[vek0_pos].set_object(vek0)

    forest0_pos = (6, 0)
    board[forest0_pos] = ForestTile(_object=None)

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    apply_attack(board, vek0_attack)

    assert vek0_expected_health == vek0.get_health()
    assert isinstance(board[forest0_pos], ForestFireTile)


def test_single_stinger_mech_on_forest_tile():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (7, 0)
    vek0_attack_vector = (-1, 0)
    vek0_expected_health = vek0.get_health()
    board[vek0_pos].set_object(vek0)

    mech0 = CombatMech()
    mech0_expected_health = mech0.get_health() - 1
    forest0_pos = (6, 0)
    board[forest0_pos] = ForestTile(_object=mech0)

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    apply_attack(board, vek0_attack)

    assert vek0_expected_health == vek0.get_health()
    assert isinstance(board[forest0_pos], ForestFireTile)
    assert mech0_expected_health == mech0.get_health()
    assert mech0.is_on_fire()


def test_single_stinger_mech_on_forest_tile_in_middle():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (4, 0)
    vek0_attack_vector = (-1, 0)
    vek0_expected_health = vek0.get_health()
    board[vek0_pos].set_object(vek0)

    mech0 = CombatMech()
    mech0_expected_health = mech0.get_health() - 1
    forest0_pos = (3, 0)
    board[forest0_pos] = ForestTile(_object=mech0)

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    apply_attack(board, vek0_attack)

    assert vek0_expected_health == vek0.get_health()
    assert isinstance(board[forest0_pos], ForestFireTile)
    assert mech0_expected_health == mech0.get_health()
    assert mech0.is_on_fire()


def test_stinger_attack_neighbour_mech():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (2, 0)
    vek0_attack_vector = (1, 0)
    board[vek0_pos].set_object(vek0)

    mech0 = CombatMech()
    mech0_pos = (3, 0)
    board[mech0_pos].set_object(mech0)
    orig_tile = copy.deepcopy(board[mech0_pos])

    mech1 = CombatMech()
    mech1_pos = (4, 0)
    board[mech1_pos].set_object(mech1)

    exp_mech0_health = mech0.get_health() - 1
    exp_mech1_health = mech1.get_health()

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    original_tiles = apply_attack(board, vek0_attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[mech0_pos]

    assert board[mech0_pos].get_object() == mech0
    assert board[mech1_pos].get_object() == mech1
    assert exp_mech0_health == mech0.get_health()
    assert exp_mech1_health == mech1.get_health()


def test_stinger_attack_neighbour_exploding_vek():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (2, 0)
    vek0_attack_vector = (1, 0)
    board[vek0_pos].set_object(vek0)

    spiderling0 = Spiderling()
    spiderling0_pos = (3, 0)
    board[spiderling0_pos].set_object(spiderling0)

    psion1 = BlastPsion()
    psion1_pos = (4, 0)
    board[psion1_pos].set_object(psion1)

    exp_psion1_health = psion1.get_health() - 1
    exp_vek0_health = vek0.get_health() - 1

    orig_tile20 = copy.deepcopy(board[vek0_pos])
    orig_tile30 = copy.deepcopy(board[spiderling0_pos])
    orig_tile40 = copy.deepcopy(board[psion1_pos])

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    original_tiles = apply_attack(board, vek0_attack)
    assert len(original_tiles) == 3

    assert orig_tile20 == original_tiles[vek0_pos]
    assert orig_tile30 == original_tiles[spiderling0_pos]
    assert orig_tile40 == original_tiles[psion1_pos]

    assert board[spiderling0_pos].get_object() is None
    assert board[psion1_pos].get_object() == psion1
    assert board[vek0_pos].get_object() == vek0
    assert exp_psion1_health == psion1.get_health()
    assert exp_vek0_health == vek0.get_health()


def test_stinger_attack_neighbour_exploding_vek_chain_reaction():
    board = Board()

    vek0 = Hornet()
    vek0_pos = (2, 0)
    vek0_attack_vector = (1, 0)
    board[vek0_pos] = ForestTile(_object=vek0)

    spiderling0 = Spiderling()
    spiderling0_pos = (3, 0)
    board[spiderling0_pos] = FrozenAcidTile(_object=spiderling0)
    board[(3, 1)] = FrozenAcidTile(_object=None)

    spiderling1 = Spiderling()
    spiderling1_pos = (4, 0)
    board[spiderling1_pos] = IceTile(_object=spiderling1)
    board[(4, 1)] = DamagedFrozenAcidTile(_object=None)

    spiderling2 = Spiderling()
    spiderling2_pos = (5, 0)
    board[spiderling2_pos] = DamagedFrozenAcidTile(_object=spiderling2)
    board[(5, 1)] = IceTile(_object=None)

    spiderling3 = Spiderling()
    spiderling3_pos = (6, 0)
    board[spiderling3_pos] = DamagedIceTile(_object=spiderling3)
    board[(6, 1)] = DamagedIceTile(_object=None)

    psion1 = BlastPsion()
    psion1_pos = (1, 0)
    board[psion1_pos].set_object(psion1)

    exp_vek0_health = vek0.get_health() - 1

    orig_tile20 = copy.deepcopy(board[vek0_pos])
    orig_tile30 = copy.deepcopy(board[spiderling0_pos])
    orig_tile31 = copy.deepcopy(board[(3, 1)])
    orig_tile40 = copy.deepcopy(board[spiderling1_pos])
    orig_tile41 = copy.deepcopy(board[(4, 1)])
    orig_tile50 = copy.deepcopy(board[spiderling2_pos])
    orig_tile51 = copy.deepcopy(board[(5, 1)])
    orig_tile60 = copy.deepcopy(board[spiderling3_pos])
    orig_tile61 = copy.deepcopy(board[(6, 1)])

    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    original_tiles = apply_attack(board, vek0_attack)
    assert len(original_tiles) == 9

    assert orig_tile20 == original_tiles[vek0_pos]
    assert orig_tile30 == original_tiles[spiderling0_pos]
    assert orig_tile31 == original_tiles[(3, 1)]
    assert orig_tile40 == original_tiles[spiderling1_pos]
    assert orig_tile41 == original_tiles[(4, 1)]
    assert orig_tile50 == original_tiles[spiderling2_pos]
    assert orig_tile51 == original_tiles[(5, 1)]
    assert orig_tile60 == original_tiles[spiderling3_pos]
    assert orig_tile61 == original_tiles[(6, 1)]

    assert board[spiderling0_pos].get_object() is None
    assert board[psion1_pos].get_object() == psion1
    assert board[vek0_pos].get_object() == vek0
    assert exp_vek0_health == vek0.get_health()
    assert isinstance(board[spiderling0_pos], AcidTile)
    assert isinstance(board[(3, 1)], DamagedFrozenAcidTile)
    assert isinstance(board[spiderling1_pos], WaterTile)
    assert isinstance(board[(4, 1)], AcidTile)
    assert isinstance(board[spiderling2_pos], AcidTile)
    assert isinstance(board[(5, 1)], DamagedIceTile)
    assert isinstance(board[spiderling3_pos], WaterTile)
    assert isinstance(board[(6, 1)], WaterTile)


def test_stinger_shell_psion():
    board = Board()

    vek0_pos = (1, 1)
    vek0 = Firefly()
    board[vek0_pos].set_object(vek0)

    vek1_pos = (1, 2)
    vek1 = Hornet()
    board[vek1_pos].set_object(vek1)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -1)
    attack = Attack(attacker=vek1.get_id(), weapon=Stinger(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert vek0.get_health() == vek0.get_max_health()


def test_stinger_shell_psion_on_mech():
    board = Board()

    mech0_pos = (1, 1)
    mech0 = CombatMech()
    board[mech0_pos].set_object(mech0)

    vek1_pos = (1, 2)
    vek1 = Hornet()
    board[vek1_pos].set_object(vek1)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -1)
    attack = Attack(attacker=vek1.get_id(), weapon=Stinger(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert mech0.get_health() == mech0.get_max_health() - 1


def test_stinger_shell_psion_on_psion():
    board = Board()

    vek1_pos = (1, 2)
    vek1 = Hornet()
    board[vek1_pos].set_object(vek1)

    shell_psion0_pos = (1, 1)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -1)
    attack = Attack(attacker=vek1.get_id(), weapon=Stinger(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert shell_psion0.get_health() == shell_psion0.get_max_health() - 1


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (CombatMech()),
                          (CivilianBuilding(health=2))])
def test_stinger_on_shielded_object(obj):
    board = Board()

    vek0_pos = (1, 1)
    vek0 = Hornet()
    board[vek0_pos].set_object(vek0)
    vek0_attack_vector = (0, 1)
    vek0_attack = Attack(attacker=vek0.get_id(), weapon=Stinger(),
                         vector=vek0_attack_vector)

    obj1_pos = (1, 2)
    obj1 = obj
    obj1.set_shield()
    board[obj1_pos].set_object(obj1)

    apply_attack(board, vek0_attack)
    assert obj1.get_health() == obj1.get_max_health()
    assert not obj1.is_shielded()
