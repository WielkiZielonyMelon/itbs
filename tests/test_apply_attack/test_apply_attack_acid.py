import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech 
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import AcidPool, AcidTile, GroundTile, \
        WaterTile
from src.game_objects.vek import Hornet, Firefly
from src.game_objects.weapons.acid import Acid
from src.game_objects.weapons.titan_fist import TitanFist


def test_acid_on_empty_tile():
    board = Board()
    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=None)

    attack = Attack(attacker=fire_pos, weapon=Acid(), vector=None)
    apply_attack(board, attack)

    assert isinstance(board[fire_pos], AcidPool)


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (Hornet())])
def test_acidify_object_ground_tile(obj):
    board = Board()

    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=None)
    tile = board[fire_pos]
    tile.set_object(obj)
        
    exp_obj_health = obj.get_health()

    attack = Attack(attacker=fire_pos, weapon=Acid(), vector=None)
    apply_attack(board, attack)

    assert obj.get_health() == exp_obj_health
    assert obj.is_on_acid()
    assert isinstance(board[fire_pos], GroundTile)


@pytest.mark.parametrize("obj",
                         [(Mountain())])
def test_acidify_mountain_ground_tile(obj):
    board = Board()

    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=None)
    tile = board[fire_pos]
    tile.set_object(obj)

    exp_obj_health = obj.get_health()

    attack = Attack(attacker=fire_pos, weapon=Acid(), vector=None)
    apply_attack(board, attack)

    assert obj.get_health() == exp_obj_health
    assert not obj.is_on_acid()
    assert isinstance(board[fire_pos], GroundTile)


@pytest.mark.parametrize("obj",
                         [(CivilianBuilding(health=4))])
def test_acidify_building_ground_tile(obj):
    board = Board()

    fire_pos = (0, 0)

    board[fire_pos] = GroundTile(_object=None)
    tile = board[fire_pos]
    tile.set_object(obj)

    exp_obj_health = obj.get_health()

    attack = Attack(attacker=fire_pos, weapon=Acid(), vector=None)
    apply_attack(board, attack)

    assert obj.get_health() == exp_obj_health
    assert not obj.is_on_acid()
    assert isinstance(board[fire_pos], AcidPool)


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (Firefly()),
                          (Hornet())])
def test_kill_object_on_acid_over_water(obj):
    board = Board()
    pos = (1, 0)
    direction = (-1, 0)
    pos_after_attack = (0, 0)

    puncher = CombatMech()
    puncher_pos = (pos[0] - direction[0], pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)

    attack_acid = Attack(attacker=pos, weapon=Acid(), vector=None)
    attack_fist = Attack(attacker=puncher.get_id(), weapon=TitanFist(damage_plus_2=True), vector=direction)

    board[pos] = WaterTile(_object=None)
    board[pos_after_attack] = WaterTile(_object=None)
    board[pos].set_object(obj)

    apply_attack(board, attack_acid)
    apply_attack(board, attack_fist)

    tile = board[pos]
    obj = tile.get_object()

    assert obj is None
    assert isinstance(tile, WaterTile)

    tile = board[pos_after_attack]
    obj = tile.get_object()

    assert obj is None
    assert isinstance(tile, AcidTile)


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (Firefly()),
                          (Hornet())])
def test_kill_object_on_acid_over_ground_tile(obj):
    board = Board()
    pos = (1, 0)
    direction = (-1, 0)
    pos_after_attack = (0, 0)

    puncher = CombatMech()
    puncher_pos = (pos[0] - direction[0], pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)

    attack_acid = Attack(attacker=pos, weapon=Acid(), vector=None)
    attack_fist = Attack(attacker=puncher.get_id(), weapon=TitanFist(), vector=direction)

    board[pos] = WaterTile(_object=None)
    board[pos_after_attack] = GroundTile(_object=None)
    board[pos].set_object(obj)

    apply_attack(board, attack_acid)
    apply_attack(board, attack_fist)

    tile = board[pos]
    obj = tile.get_object()

    assert obj is None
    assert isinstance(tile, WaterTile)

    tile = board[pos_after_attack]
    obj = tile.get_object()

    assert obj is None
    assert isinstance(tile, AcidPool)
