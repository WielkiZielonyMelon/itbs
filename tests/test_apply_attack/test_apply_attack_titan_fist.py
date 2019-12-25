import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import ChasmTile, AcidTile, WaterTile, ForestTile, FrozenAcidTile, DamagedIceTile, \
    IceTile, ForestFireTile
from src.game_objects.vek import Firefly, BlastPsion, Spiderling, ShellPsion
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("punch_pos, direction",
                         [((1, 0), (1, 0)),
                          ((0, 1), (0, 1)),
                          ((6, 0), (-1, 0)),
                          ((7, 1), (0, 1)),
                          ((7, 6), (0, -1)),
                          ((6, 7), (-1, 0)),
                          ((0, 6), (0, -1)),
                          ((1, 7), (1, 0))])
def test_titan_fist_on_empty_tile(punch_pos, direction):
    board = Board()

    mech_pos = (punch_pos[0] - direction[0], punch_pos[1] - direction[1])
    mech = CombatMech()
    board[mech_pos].set_object(mech)

    attack = Attack(attacker=mech.get_id(), weapon=TitanFist(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 0


@pytest.mark.parametrize("before_punch, direction, after_punch",
                         [((1, 0), (1, 0), (2, 0)),
                          ((0, 1), (0, 1), (0, 2)),
                          ((6, 0), (-1, 0), (5, 0)),
                          ((7, 1), (0, 1), (7, 2)),
                          ((7, 6), (0, -1), (7, 5)),
                          ((6, 7), (-1, 0), (5, 7)),
                          ((0, 6), (0, -1), (0, 5)),
                          ((1, 7), (1, 0), (2, 7))])
def test_titan_fist_on_mech(before_punch, direction, after_punch):
    board = Board()
    puncher_pos = (before_punch[0] - direction[0], before_punch[1] - direction[1])
    puncher = CombatMech()
    board[puncher_pos].set_object(puncher)

    mech = CombatMech()

    board[before_punch].set_object(mech)
    old_health = mech.get_health()
    expected_damage = 2

    orig_punch = copy.deepcopy(board[before_punch])
    orig_after_punch = copy.deepcopy(board[after_punch])
    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_punch == original_tiles[before_punch]
    assert orig_after_punch == original_tiles[after_punch]

    assert not board[before_punch].has_object()
    assert (old_health - expected_damage) == mech.get_health()


@pytest.mark.parametrize("before_punch, direction",
                         [((0, 0), (-1, 0)),
                          ((0, 0), (0, -1)),
                          ((7, 7), (0, 1)),
                          ((7, 7), (1, 0))])
def test_titan_fist_mech_out_of_board(before_punch, direction):
    board = Board()
    puncher_pos = (before_punch[0] - direction[0], before_punch[1] - direction[1])
    puncher = CombatMech()
    board[puncher_pos].set_object(puncher)

    mech = CombatMech()

    board[before_punch].set_object(mech)
    old_health = mech.get_health()
    expected_damage = 2

    orig_tile = copy.deepcopy(board[before_punch])
    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[before_punch]

    assert (old_health - expected_damage) == mech.get_health()


def test_titan_fist_mount():
    board = Board()
    mountain = Mountain()

    before_punch = (1, 0)
    direction = (1, 0)
    board[before_punch].set_object(mountain)

    puncher_pos = (before_punch[0] - direction[0], before_punch[1] - direction[1])
    puncher = CombatMech()
    board[puncher_pos].set_object(puncher)

    old_health = mountain.get_health()
    expected_damage = 1

    orig_tile = copy.deepcopy(board[before_punch])

    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[before_punch]

    assert (old_health - expected_damage) == mountain.get_health()


@pytest.mark.parametrize("obj, punch_pos, direction, block_pos",
                         [(CombatMech(), (1, 0), (1, 0), (2, 0)),
                          (Mountain(), (1, 0), (1, 0), (2, 0))])
def test_titan_fist_against_object(obj, punch_pos, direction, block_pos):
    board = Board()
    mech = CombatMech()

    board[punch_pos].set_object(mech)
    board[block_pos].set_object(obj)

    block_health = obj.get_health()
    punch_health_expected = 0
    block_health_expected = block_health - 1

    puncher_pos = (punch_pos[0] - direction[0], punch_pos[1] - direction[1])
    puncher = CombatMech()
    board[puncher_pos].set_object(puncher)

    orig_pushed = copy.deepcopy(board[punch_pos])
    orig_blocked = copy.deepcopy(board[block_pos])

    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(), vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2

    assert orig_pushed == original_tiles[punch_pos]
    assert orig_blocked == original_tiles[block_pos]

    assert mech.get_health() == punch_health_expected
    assert obj.get_health() == block_health_expected


def test_titan_fist_extra_damage_on_mech():
    board = Board()
    mech = CombatMech()

    before_punch = (1, 0)
    direction = (1, 0)
    after_punch = (2, 0)

    puncher_pos = (before_punch[0] - direction[0], before_punch[1] - direction[1])
    puncher = CombatMech()
    board[puncher_pos].set_object(puncher)

    board[before_punch].set_object(mech)

    orig_before_punch = copy.deepcopy(board[before_punch])
    orig_after_punch = copy.deepcopy(board[after_punch])
    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(damage_plus_2=True),
                    vector=direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_before_punch == original_tiles[before_punch]
    assert orig_after_punch == original_tiles[after_punch]

    assert not board[before_punch].has_object()
    assert not board[after_punch].has_object()


def test_titan_fist_with_dash():
    board = Board()
    attack_mech = CombatMech()

    mech_pos_before = (0, 0)
    attack_direction = (1, 0)
    mech_pos_after = (4, 0)

    firefly = Firefly()
    vek_pos_before = (5, 0)
    vek_pos_after = (6, 0)
    vek_health_after_attack = 1

    board[mech_pos_before].set_object(attack_mech)
    board[vek_pos_before].set_object(firefly)
    orig_mech_before = copy.deepcopy(board[mech_pos_before])
    orig_mech_after = copy.deepcopy(board[mech_pos_after])
    orig_vek_before = copy.deepcopy(board[vek_pos_before])
    orig_vek_after = copy.deepcopy(board[vek_pos_after])

    attack = Attack(attacker=attack_mech.get_id(), weapon=TitanFist(dash=True),
                    vector=attack_direction)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 4
    assert orig_mech_before == original_tiles[mech_pos_before]
    assert orig_mech_after == original_tiles[mech_pos_after]
    assert orig_vek_before == original_tiles[vek_pos_before]
    assert orig_vek_after == original_tiles[vek_pos_after]

    assert board[mech_pos_after].get_object() == attack_mech
    firefly_after_attack = board[vek_pos_after].get_object()

    assert firefly_after_attack.get_health() == vek_health_after_attack


def test_titan_fist_cooperation():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (0, 0)
    mech0_move = (0, 1)
    mech0_dir = (0, 1)

    vek0 = Firefly()
    vek0_pos = (0, 2)
    vek0_pushed = (0, 3)

    mech1 = CombatMech()
    mech1_pos = (0, 7)
    mech1_move = (0, 4)
    mech1_dir = (0, -1)

    board[mech0_pos].set_object(mech0)
    board[vek0_pos].set_object(vek0)
    board[mech1_pos].set_object(mech1)

    orig_00 = copy.deepcopy(board[mech0_pos])
    orig_01 = copy.deepcopy(board[mech0_move])
    attack = Attack(attacker=mech0.get_id(), weapon=Move(), vector=mech0_move)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_00 == original_tiles[mech0_pos]
    assert orig_01 == original_tiles[mech0_move]

    orig_00 = copy.deepcopy(board[vek0_pos])
    orig_01 = copy.deepcopy(board[vek0_pushed])
    attack = Attack(attacker=mech0.get_id(), weapon=TitanFist(), vector=mech0_dir)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_00 == original_tiles[vek0_pos]
    assert orig_01 == original_tiles[vek0_pushed]

    orig_00 = copy.deepcopy(board[mech1_pos])
    orig_01 = copy.deepcopy(board[mech1_move])
    attack = Attack(attacker=mech1.get_id(), weapon=Move(), vector=mech1_move)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_00 == original_tiles[mech1_pos]
    assert orig_01 == original_tiles[mech1_move]

    orig_00 = copy.deepcopy(board[vek0_pushed])
    orig_01 = copy.deepcopy(board[vek0_pos])
    attack = Attack(attacker=mech1.get_id(), weapon=TitanFist(), vector=mech1_dir)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 2
    assert orig_00 == original_tiles[vek0_pushed]
    assert orig_01 == original_tiles[vek0_pos]

    assert board[vek0_pos].get_object() is None
    assert board[vek0_pushed].get_object() is None


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

    attack = Attack(attacker=mech0.get_id(), weapon=TitanFist(), vector=(-1, 0))

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


def test_titan_fist_shell_psion():
    board = Board()

    vek0_pos = (1, 1)
    vek0 = Firefly()
    board[vek0_pos].set_object(vek0)

    mech1_pos = (1, 2)
    mech1 = CombatMech()
    board[mech1_pos].set_object(mech1)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -1)
    attack = Attack(attacker=mech1.get_id(), weapon=TitanFist(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert vek0.get_health() == vek0.get_max_health() - 1
    assert board[vek0_pos].get_object() is None
    assert board[(1, 0)].get_object() == vek0


def test_titan_fist_shell_psion_on_mech():
    board = Board()

    mech0_pos = (1, 1)
    mech0 = CombatMech()
    board[mech0_pos].set_object(mech0)

    mech1_pos = (1, 2)
    mech1 = CombatMech()
    board[mech1_pos].set_object(mech1)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -1)
    attack = Attack(attacker=mech1.get_id(), weapon=TitanFist(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert mech0.get_health() == mech0.get_max_health() - 2
    assert board[mech0_pos].get_object() is None
    assert board[(1, 0)].get_object() == mech0


def test_titan_fist_shell_psion_on_psion():
    board = Board()

    mech0_pos = (1, 1)
    mech0 = CombatMech()
    board[mech0_pos].set_object(mech0)

    shell_psion0_pos = (1, 2)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, 1)
    attack = Attack(attacker=mech0.get_id(), weapon=TitanFist(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert shell_psion0.get_health() == shell_psion0.get_max_health() - 2
    assert board[shell_psion0_pos].get_object() is None
    assert board[(1, 3)].get_object() is None


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (CombatMech()),
                          (CivilianBuilding(health=2))])
def test_titan_fist_on_shielded_object(obj):
    board = Board()

    mech0_pos = (1, 1)
    mech0 = obj
    board[mech0_pos].set_object(mech0)
    mech0_attack_vector = (0, 1)
    vek0_attack = Attack(attacker=mech0.get_id(), weapon=TitanFist(),
                         vector=mech0_attack_vector)

    obj1_pos = (1, 2)
    obj1 = obj
    obj1.set_shield()
    board[obj1_pos].set_object(obj1)

    apply_attack(board, vek0_attack)
    assert obj1.get_health() == obj1.get_max_health()
    assert not obj1.is_shielded()
