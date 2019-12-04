import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import GroundTile, ForestTile, FrozenAcidTile, IceTile, DamagedFrozenAcidTile, \
    DamagedIceTile, WaterTile, AcidTile
from src.game_objects.vek import Hornet, Firefly, Spiderling, BlastPsion
from src.game_objects.weapons.burn import Burn


def test_burn_empty_tile():
    board = Board()

    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=None)
    orig_tile = copy.deepcopy(board[fire_pos])

    attack = Attack(attacker=fire_pos, weapon=Burn(), vector=None)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1

    assert orig_tile == original_tiles[fire_pos]


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech()),
                          (Firefly()),
                          (Hornet()),
                          (Mountain())])
def test_burn_mech(obj):
    board = Board()

    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=obj)
    orig_tile = copy.deepcopy(board[fire_pos])

    exp_obj_health = obj.get_health() - 1

    attack = Attack(attacker=fire_pos, weapon=Burn(), vector=None)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1

    assert orig_tile == original_tiles[fire_pos]

    assert obj.get_health() == exp_obj_health


def test_burn_building():
    board = Board()
    building = CivilianBuilding(health=4)

    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=building)
    orig_tile = copy.deepcopy(board[fire_pos])

    exp_building_health = building.get_health()

    attack = Attack(attacker=fire_pos, weapon=Burn(), vector=None)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1

    assert orig_tile == original_tiles[fire_pos]

    assert building.get_health() == exp_building_health


def test_burn_attack_exploding_vek_chain_reaction():
    board = Board()

    vek0 = Firefly()
    vek0_pos = (2, 0)
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
    orig_tile70 = copy.deepcopy(board[(7, 0)])

    vek0_attack = Attack(attacker=spiderling0_pos, weapon=Burn(),
                         vector=None)

    original_tiles = apply_attack(board, vek0_attack)
    assert len(original_tiles) == 10

    assert orig_tile20 == original_tiles[vek0_pos]
    assert orig_tile30 == original_tiles[spiderling0_pos]
    assert orig_tile31 == original_tiles[(3, 1)]
    assert orig_tile40 == original_tiles[spiderling1_pos]
    assert orig_tile41 == original_tiles[(4, 1)]
    assert orig_tile50 == original_tiles[spiderling2_pos]
    assert orig_tile51 == original_tiles[(5, 1)]
    assert orig_tile60 == original_tiles[spiderling3_pos]
    assert orig_tile61 == original_tiles[(6, 1)]
    assert orig_tile70 == original_tiles[(7, 0)]

    assert board[spiderling0_pos].get_object() is None
    assert board[psion1_pos].get_object() == psion1
    assert board[vek0_pos].get_object() == vek0
    assert exp_vek0_health == vek0.get_health()
    assert isinstance(board[spiderling0_pos], DamagedFrozenAcidTile)
    assert isinstance(board[(3, 1)], DamagedFrozenAcidTile)
    assert isinstance(board[spiderling1_pos], WaterTile)
    assert isinstance(board[(4, 1)], AcidTile)
    assert isinstance(board[spiderling2_pos], AcidTile)
    assert isinstance(board[(5, 1)], DamagedIceTile)
    assert isinstance(board[spiderling3_pos], WaterTile)
    assert isinstance(board[(6, 1)], WaterTile)
