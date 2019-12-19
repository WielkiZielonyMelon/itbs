import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import AcidTile, DamagedFrozenAcidTile, \
    FrozenAcidTile
from src.game_objects.vek import Firefly, Hornet
from src.game_objects.weapons.freeze import Freeze
from src.game_objects.weapons.push import Push
from src.game_objects.weapons.set_on_fire import SetOnFire
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("obj,on_acid",
                         [(CombatMech(), True),
                          (JetMech(), False),
                          (Hornet(), False)])
def test_move_object_over_acid_tile_survives(obj, on_acid):
    board = Board()
    pos = (0, 0)
    board[pos] = AcidTile(_object=None)

    board[pos].set_object(obj)
    board[pos].apply_tile_effects()

    tile = board[pos]
    obj = tile.get_object()
    assert obj.is_on_acid() == on_acid


@pytest.mark.parametrize("obj",
                         [(Firefly())])
def test_move_object_over_acid_tile_dies(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = AcidTile(_object=None)

    board[pos].set_object(obj)
    board[pos].apply_tile_effects()

    tile = board[pos]
    obj = tile.get_object()
    assert obj is None


@pytest.mark.parametrize("obj,on_acid",
                         [(CombatMech(), True),
                          (JetMech(), False),
                          (Hornet(), False)])
def test_push_object_over_acid_tile_survives(obj, on_acid):
    board = Board()
    pool_pos = (0, 0)
    obj_pos = (1, 0)
    direction = (-1, 0)
    board[pool_pos] = AcidTile(_object=None)
    attack = Attack(attacker=obj_pos, weapon=Push(), vector=direction)

    board[obj_pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pool_pos]
    obj = tile.get_object()
    assert obj.is_on_acid() == on_acid


@pytest.mark.parametrize("obj",
                         [(Firefly())])
def test_push_object_over_acid_tile_dies(obj):
    board = Board()
    pool_pos = (0, 0)
    obj_pos = (1, 0)
    direction = (-1, 0)
    board[pool_pos] = AcidTile(_object=None)
    attack = Attack(attacker=obj_pos, weapon=Push(),
                    vector=direction)

    board[obj_pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pool_pos]
    obj = tile.get_object()
    assert obj is None


@pytest.mark.parametrize("obj,on_acid",
                         [(CombatMech(), True),
                          (JetMech(), False),
                          (Hornet(), False)])
def test_freeze_object_over_acid_tile(obj, on_acid):
    board = Board()
    pos = (0, 0)
    board[pos] = AcidTile(_object=None)
    attack = Attack(attacker=None, weapon=Freeze(), vector=None)

    board[pos].set_object(obj)
    board[pos].apply_tile_effects()

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert obj.is_on_acid() == on_acid
    assert obj.is_frozen()
    assert isinstance(tile, FrozenAcidTile)


def test_freeze_acid_exceptions():
    board = Board()
    pos = (0, 0)
    board[pos] = AcidTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].freeze()

    assert ("Cannot freeze AcidTile. Convert to FrozenAcidTile " +
            "and then freeze object" in str(context.value))


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech()),
                          (Hornet())])
def test_freeze_object_over_acid_tile(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = DamagedFrozenAcidTile(_object=None)
    attack = Attack(attacker=pos, weapon=Freeze(), vector=None)

    board[pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert not obj.is_on_acid()
    assert obj.is_frozen()
    assert isinstance(tile, FrozenAcidTile)


@pytest.mark.parametrize("obj,on_fire,on_acid",
                         [(CombatMech(), False, True),
                          (JetMech(), True, False),
                          (Hornet(), True, False)])
def test_set_on_fire_object_over_damaged_frozen_acid_tile(obj, on_fire, on_acid):
    board = Board()
    pos = (0, 0)
    board[pos] = DamagedFrozenAcidTile(_object=None)
    attack = Attack(attacker=pos, weapon=SetOnFire(),
                    vector=None)

    board[pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert obj.is_on_fire() == on_fire
    assert obj.is_on_acid() == on_acid
    assert isinstance(tile, AcidTile)


@pytest.mark.parametrize("obj,on_fire,on_acid",
                         [(CombatMech(), False, True),
                          (JetMech(), True, False),
                          (Hornet(), True, False)])
def test_set_on_fire_object_over_frozen_acid_tile_survives(obj, on_fire, on_acid):
    board = Board()
    pos = (0, 0)
    board[pos] = FrozenAcidTile(_object=None)
    attack = Attack(attacker=pos, weapon=SetOnFire(),
                    vector=None)

    board[pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert obj.is_on_fire() == on_fire
    assert obj.is_on_acid() == on_acid
    assert isinstance(tile, AcidTile)


@pytest.mark.parametrize("obj",
                         [(Firefly())])
def test_set_on_fire_object_over_frozen_acid_tile_survives(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = FrozenAcidTile(_object=None)
    attack = Attack(attacker=pos, weapon=SetOnFire(),
                    vector=None)

    board[pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert obj is None


def test_damage_object_over_frozen_acid_tile_survives():
    board = Board()
    pos = (1, 0)
    direction = (-1, 0)
    pos_after_attack = (0, 0)
    board[pos] = DamagedFrozenAcidTile(_object=None)

    puncher = CombatMech()
    puncher_pos = (pos[0] - direction[0], pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)
    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(),
                    vector=direction)

    obj = CombatMech()
    board[pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pos]
    obj = board[pos_after_attack].get_object()
    assert not obj.is_on_acid()
    assert isinstance(tile, AcidTile)


def test_damage_object_over_frozen_acid_tile_blocked_survives():
    board = Board()
    pos = (1, 0)
    direction = (-1, 0)
    pos_after_attack = (0, 0)
    board[pos] = DamagedFrozenAcidTile(_object=None)

    puncher = CombatMech()
    puncher_pos = (pos[0] - direction[0], pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)
    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(),
                    vector=direction)

    obj = CombatMech()
    board[pos].set_object(obj)

    mountain = Mountain()
    mountain_exp_health = mountain.get_health() - 1
    board[pos_after_attack].set_object(mountain)

    apply_attack(board, attack)

    tile = board[pos]
    obj = board[pos].get_object()
    mountain = board[pos_after_attack].get_object()

    assert obj is None
    assert isinstance(tile, AcidTile)
    assert mountain.get_health() == mountain_exp_health


def test_damaged_frozen_acid_tile_exception():
    board = Board()
    pos = (0, 0)
    board[pos] = DamagedFrozenAcidTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].freeze()

    assert "Cannot freeze DamagedFrozenAcidTile. Convert to FrozenAcidTile and then freeze object" \
           in str(context.value)

    with pytest.raises(Exception) as context:
        board[pos].set_fire()

    assert "Cannot set fire on DamagedFrozenAcidTile. Set object on fire and convert tile to AcidTile" \
           in str(context.value)


def test_damage_object_over_frozen_acid_tile():
    board = Board()
    pos = (1, 0)
    direction = (-1, 0)
    pos_after_attack = (0, 0)
    board[pos] = FrozenAcidTile(_object=None)

    puncher = CombatMech()
    puncher_pos = (pos[0] - direction[0], pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)

    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(),
                    vector=direction)

    obj = CombatMech()
    board[pos].set_object(obj)

    apply_attack(board, attack)

    tile = board[pos]
    obj = board[pos_after_attack].get_object()
    assert not obj.is_on_acid()
    assert isinstance(tile, DamagedFrozenAcidTile)


def test_damage_object_over_frozen_acid_tile_blocked():
    board = Board()
    pos = (1, 0)
    direction = (-1, 0)
    pos_after_attack = (0, 0)
    board[pos] = FrozenAcidTile(_object=None)

    puncher = CombatMech()
    puncher_pos = (pos[0] - direction[0], pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)

    attack = Attack(attacker=puncher.get_id(), weapon=TitanFist(),
                    vector=direction)

    obj = CombatMech()
    board[pos].set_object(obj)
    mountain = Mountain()
    mountain_exp_health = mountain.get_health() - 1
    board[pos_after_attack].set_object(mountain)

    apply_attack(board, attack)

    tile = board[pos]
    obj = board[pos].get_object()
    mountain = board[pos_after_attack].get_object()

    assert obj is None
    assert isinstance(tile, DamagedFrozenAcidTile)
    assert mountain.get_health() == mountain_exp_health


def test_frozen_acid_tile_exception():
    board = Board()
    pos = (0, 0)
    board[pos] = FrozenAcidTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].set_fire()

    assert "Cannot set fire on FrozenAcidTile. Set object on fire and convert tile to AcidTile" \
           in str(context.value)
