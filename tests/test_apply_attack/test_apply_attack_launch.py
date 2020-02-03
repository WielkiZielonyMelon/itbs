import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding, Building
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.mountain import Mountain
from src.game_objects.satellite_rocket import ReadySatelliteRocket
from src.game_objects.tiles.tile import GroundTile, ForestTile, FrozenAcidTile, IceTile, DamagedFrozenAcidTile, \
    DamagedIceTile, WaterTile, AcidTile, ForestFireTile
from src.game_objects.vek import Hornet, Firefly, Spiderling, BlastPsion, ShellPsion
from src.game_objects.weapons.burn import Burn
from src.game_objects.weapons.kill import Kill
from src.game_objects.weapons.launch import Launch


@pytest.mark.parametrize("tile_before, tile_after",
                         [(ForestTile, ForestFireTile),
                          (GroundTile, GroundTile),
                          (IceTile, DamagedIceTile),
                          (DamagedIceTile, WaterTile),
                          (FrozenAcidTile, DamagedFrozenAcidTile),
                          (DamagedFrozenAcidTile, AcidTile)])
def test_launch_rocket(tile_before, tile_after):
    board = Board()

    launch_pos = (1, 1)
    tiles_pos = [(0, 1), (2, 1), (1, 0), (1, 2)]

    board[launch_pos].set_object(ReadySatelliteRocket())
    board.fill_object_position_cache()

    for tile_pos in tiles_pos:
        board[tile_pos] = tile_before(_object=None)

    orig_launch = copy.deepcopy(board[launch_pos])

    attack = Attack(attacker=launch_pos, weapon=Launch(), vector=None)
    original_tiles = apply_attack(board, attack)

    assert original_tiles[launch_pos] == orig_launch
    for tile_pos in tiles_pos:
        assert board[tile_pos] == tile_after(_object=None)


def test_launch_exploding_vek_chain_reaction():
    board = Board()

    rocket0 = ReadySatelliteRocket()
    rocket0_pos = (2, 0)
    board[rocket0_pos] = ForestTile(_object=rocket0)

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
    psion1_pos = (0, 0)
    board[psion1_pos].set_object(psion1)

    orig_tile20 = copy.deepcopy(board[rocket0_pos])
    orig_tile30 = copy.deepcopy(board[spiderling0_pos])
    orig_tile31 = copy.deepcopy(board[(3, 1)])
    orig_tile40 = copy.deepcopy(board[spiderling1_pos])
    orig_tile41 = copy.deepcopy(board[(4, 1)])
    orig_tile50 = copy.deepcopy(board[spiderling2_pos])
    orig_tile51 = copy.deepcopy(board[(5, 1)])
    orig_tile60 = copy.deepcopy(board[spiderling3_pos])
    orig_tile61 = copy.deepcopy(board[(6, 1)])

    board.fill_object_position_cache()
    rocket0_attack = Attack(attacker=rocket0_pos, weapon=Launch(),
                            vector=None)

    original_tiles = apply_attack(board, rocket0_attack)
    assert len(original_tiles) == 9

    assert orig_tile20 == original_tiles[rocket0_pos]
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
    assert board[rocket0_pos].get_object() is None
    assert isinstance(board[spiderling0_pos], AcidTile)
    assert isinstance(board[(3, 1)], DamagedFrozenAcidTile)
    assert isinstance(board[spiderling1_pos], WaterTile)
    assert isinstance(board[(4, 1)], AcidTile)
    assert isinstance(board[spiderling2_pos], AcidTile)
    assert isinstance(board[(5, 1)], DamagedIceTile)
    assert isinstance(board[spiderling3_pos], WaterTile)
    assert isinstance(board[(6, 1)], WaterTile)


def test_launch_on_shell_psion():
    board = Board()

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    rocket0_pos = (1, 0)
    rocket0 = ReadySatelliteRocket()
    board[rocket0_pos].set_object(rocket0)
    board.fill_object_position_cache()

    attack = Attack(attacker=rocket0_pos, weapon=Launch(),
                    vector=None)
    apply_attack(board, attack)

    assert shell_psion0.get_health() == 0
    assert board[shell_psion0_pos].get_object() is None


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (Hornet())])
def test_launch_object_with_shell_psion_present(obj):
    board = Board()

    psion0_pos = (0, 0)
    psion0 = ShellPsion()
    board[psion0_pos].set_object(psion0)

    obj0_pos = (1, 3)
    obj0 = obj
    board[obj0_pos].set_object(obj0)

    rocket0_pos = (2, 3)
    rocket0 = ReadySatelliteRocket()
    board[rocket0_pos].set_object(rocket0)

    board.fill_object_position_cache()

    attack = Attack(attacker=rocket0_pos, weapon=Launch(),
                    vector=None)

    apply_attack(board, attack)
    assert obj0.get_health() == 0
    assert board[obj0_pos].get_object() is None


@pytest.mark.parametrize("obj",
                         [(JetMech()),
                          (CombatMech())])
def test_launch_corpse_object_with_shell_psion_present(obj):
    board = Board()

    psion0_pos = (0, 0)
    psion0 = ShellPsion()
    board[psion0_pos].set_object(psion0)

    obj0_pos = (1, 3)
    obj0 = obj
    board[obj0_pos].set_object(obj0)

    rocket0_pos = (2, 3)
    rocket0 = ReadySatelliteRocket()
    board[rocket0_pos].set_object(rocket0)

    board.fill_object_position_cache()

    attack = Attack(attacker=rocket0_pos, weapon=Launch(),
                    vector=None)

    apply_attack(board, attack)
    assert obj0.get_health() == 0
    assert board[obj0_pos].get_object() is not None


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (Hornet())])
def test_launch_on_shielded_object(obj):
    board = Board()

    obj0_pos = (1, 3)
    obj0 = obj
    obj0.set_shield()
    board[obj0_pos].set_object(obj0)

    rocket0_pos = (2, 3)
    rocket0 = ReadySatelliteRocket()
    board[rocket0_pos].set_object(rocket0)

    board.fill_object_position_cache()
    attack = Attack(attacker=rocket0_pos, weapon=Launch(),
                    vector=None)

    apply_attack(board, attack)
    assert obj0.get_health() == 0
    assert obj0.is_shielded() is False
    assert board[obj0_pos].get_object() is None


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech())])
def test_launch_on_shielded_object(obj):
    board = Board()

    obj0_pos = (1, 3)
    obj0 = obj
    obj0.set_shield()
    board[obj0_pos].set_object(obj0)

    rocket0_pos = (2, 3)
    rocket0 = ReadySatelliteRocket()
    board[rocket0_pos].set_object(rocket0)

    board.fill_object_position_cache()
    attack = Attack(attacker=rocket0_pos, weapon=Launch(),
                    vector=None)

    apply_attack(board, attack)
    assert obj0.get_health() == 0
    assert obj0.is_shielded() is False
    assert board[obj0_pos].get_object() is not None
