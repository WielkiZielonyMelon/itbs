import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, ArtilleryMech, CannonMech
from src.game_objects.tiles.tile import DamagedIceTile, IceTile, ForestTile, ForestFireTile, WaterTile, \
    FrozenAcidTile, DamagedFrozenAcidTile, AcidTile, SandTile, GroundTile
from src.game_objects.vek import Hornet, AlphaHornet, Scarab, AlphaFirefly, Firefly, ShellPsion
from src.game_objects.weapons.accelerating_thorax import AcceleratingThorax, EnhancedThorax
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.spitting_glands import SpittingGlands
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("tile_before, tile_after",
                         [(ForestTile, ForestFireTile),
                          (IceTile, DamagedIceTile),
                          (DamagedIceTile, WaterTile),
                          (FrozenAcidTile, DamagedFrozenAcidTile),
                          (DamagedFrozenAcidTile, AcidTile)])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((0, 0), (0, 1)),
                          ((0, 0), (1, 0)),
                          ((0, 7), (0, 6)),
                          ((0, 7), (1, 7)),
                          ((7, 7), (6, 7)),
                          ((7, 7), (7, 6)),
                          ((7, 0), (6, 0)),
                          ((7, 0), (7, 1)),
                          ((1, 1), (0, 1)),
                          ((1, 1), (1, 0)),
                          ((1, 1), (1, 2)),
                          ((1, 1), (2, 1))])
@pytest.mark.parametrize("attacker, weapon",
                         [(CombatMech, TitanFist),
                          (Hornet, Stinger),
                          (AlphaHornet, LaunchingStinger)])
def test_melee_weapon_on_damageable_tile(tile_before, tile_after, tile_pos, attacker_pos, attacker, weapon):
    tile_before = tile_before(_object=None)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    vector = (tile_pos[0] - attacker_pos[0], tile_pos[1] - attacker_pos[1])
    board.fill_object_position_cache()
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], tile_after)


@pytest.mark.parametrize("tile_before, tile_after",
                         [(ForestTile, ForestFireTile),
                          (IceTile, DamagedIceTile),
                          (DamagedIceTile, WaterTile),
                          (FrozenAcidTile, DamagedFrozenAcidTile),
                          (DamagedFrozenAcidTile, AcidTile)])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((0, 0), (0, 2)),
                          ((0, 0), (0, 7)),
                          ((0, 0), (2, 0)),
                          ((0, 0), (7, 0)),
                          ((0, 7), (0, 6)),
                          ((0, 7), (1, 7)),
                          ((7, 7), (6, 7)),
                          ((7, 7), (7, 6)),
                          ((7, 0), (6, 0)),
                          ((7, 0), (7, 1)),
                          ((2, 2), (0, 2)),
                          ((2, 2), (2, 0)),
                          ((2, 2), (4, 2)),
                          ((2, 2), (2, 4))])
@pytest.mark.parametrize("attacker, weapon",
                         [(ArtilleryMech, Artemis),
                          (Scarab, SpittingGlands)])
def test_artillery_weapon_on_damageable_tile(tile_before, tile_after, tile_pos, attacker_pos, attacker, weapon):
    tile_before = tile_before(_object=None)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    vector = (tile_pos[0] - attacker_pos[0], tile_pos[1] - attacker_pos[1])
    board.fill_object_position_cache()
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], tile_after)


@pytest.mark.parametrize("tile_before, tile_after",
                         [(ForestTile, ForestFireTile),
                          (IceTile, DamagedIceTile),
                          (DamagedIceTile, WaterTile),
                          (FrozenAcidTile, DamagedFrozenAcidTile),
                          (DamagedFrozenAcidTile, AcidTile)])
@pytest.mark.parametrize("object_on_tile",
                         [None,
                          CombatMech,
                          Firefly,
                          Hornet,
                          ShellPsion])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((0, 0), (0, 2)),
                          ((0, 0), (0, 7)),
                          ((0, 0), (2, 0)),
                          ((0, 0), (7, 0)),
                          ((0, 7), (0, 6)),
                          ((0, 7), (1, 7)),
                          ((7, 7), (6, 7)),
                          ((7, 7), (7, 6)),
                          ((7, 0), (6, 0)),
                          ((7, 0), (7, 1))])
@pytest.mark.parametrize("attacker, weapon",
                         [(Firefly, AcceleratingThorax),
                          (AlphaFirefly, EnhancedThorax),
                          (CannonMech, TaurusCannon)])
def test_projectile_weapon_on_damageable_tile(tile_before, tile_after, object_on_tile, tile_pos,
                                              attacker_pos, attacker, weapon):
    tile_before = tile_before(_object=object_on_tile() if object_on_tile is not None else None)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    if attacker_pos[0] > tile_pos[0]:
        vector = (-1, 0)
    elif attacker_pos[0] < tile_pos[0]:
        vector = (1, 0)
    elif attacker_pos[1] > tile_pos[1]:
        vector = (0, -1)
    elif attacker_pos[1] < tile_pos[1]:
        vector = (0, 1)
    else:
        raise Exception("Bad input data")
    board.fill_object_position_cache()
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], tile_after)


@pytest.mark.parametrize("tile_before",
                         [ForestTile,
                          IceTile,
                          DamagedIceTile,
                          FrozenAcidTile,
                          DamagedFrozenAcidTile])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((2, 2), (0, 2)),
                          ((2, 2), (2, 0)),
                          ((2, 2), (4, 2)),
                          ((2, 2), (2, 4))])
@pytest.mark.parametrize("attacker, weapon",
                         [(Firefly, AcceleratingThorax),
                          (AlphaFirefly, EnhancedThorax),
                          (CannonMech, TaurusCannon)])
def test_projectile_weapon_on_damageable_tile_in_middle_no_object(tile_before, tile_pos, attacker_pos, attacker,
                                                                  weapon):
    tile_after = tile_before
    tile_before = tile_before(_object=None)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    vector = (tile_pos[0] - attacker_pos[0], tile_pos[1] - attacker_pos[1])
    board.fill_object_position_cache()
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], tile_after)


@pytest.mark.parametrize("tile_before, tile_after",
                         [(ForestTile, ForestFireTile),
                          (IceTile, DamagedIceTile),
                          (DamagedIceTile, WaterTile),
                          (FrozenAcidTile, DamagedFrozenAcidTile),
                          (DamagedFrozenAcidTile, AcidTile)])
@pytest.mark.parametrize("object_on_tile",
                         [CombatMech,
                          Firefly,
                          Hornet,
                          ShellPsion])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((2, 2), (0, 2)),
                          ((2, 2), (2, 0)),
                          ((2, 2), (4, 2)),
                          ((2, 2), (2, 4))])
@pytest.mark.parametrize("attacker, weapon",
                         [(Firefly, AcceleratingThorax),
                          (AlphaFirefly, EnhancedThorax),
                          (CannonMech, TaurusCannon)])
def test_projectile_weapon_on_damageable_tile_in_middle_with_object(tile_before, tile_after, tile_pos, object_on_tile,
                                                                    attacker_pos, attacker, weapon):
    tile_before = tile_before(_object=object_on_tile())
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    vector = (tile_pos[0] - attacker_pos[0], tile_pos[1] - attacker_pos[1])
    board.fill_object_position_cache()
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], tile_after)


@pytest.mark.parametrize("object_on_tile",
                         [CombatMech,
                          Firefly,
                          Hornet,
                          ShellPsion])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((0, 0), (0, 2)),
                          ((0, 0), (0, 7)),
                          ((0, 0), (2, 0)),
                          ((0, 0), (7, 0)),
                          ((0, 7), (0, 6)),
                          ((0, 7), (1, 7)),
                          ((7, 7), (6, 7)),
                          ((7, 7), (7, 6)),
                          ((7, 0), (6, 0)),
                          ((7, 0), (7, 1))])
@pytest.mark.parametrize("attacker, weapon",
                         [(Firefly, AcceleratingThorax),
                          (AlphaFirefly, EnhancedThorax),
                          (CannonMech, TaurusCannon)])
def test_projectile_weapon_on_forest_tile_on_edge_with_object(object_on_tile, tile_pos, attacker_pos, attacker, weapon):
    object_on_tile = object_on_tile()
    tile_before = ForestTile(_object=object_on_tile)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    if attacker_pos[0] > tile_pos[0]:
        vector = (-1, 0)
    elif attacker_pos[0] < tile_pos[0]:
        vector = (1, 0)
    elif attacker_pos[1] > tile_pos[1]:
        vector = (0, -1)
    elif attacker_pos[1] < tile_pos[1]:
        vector = (0, 1)
    else:
        raise Exception("Bad input data")
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    board.fill_object_position_cache()
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], ForestFireTile)
    obj = board[tile_pos].get_object()
    if obj is not None:
        assert obj.is_on_fire()


@pytest.mark.parametrize("object_on_tile",
                         [None,
                          CombatMech,
                          Firefly,
                          Hornet,
                          ShellPsion])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((0, 0), (0, 2)),
                          ((0, 0), (0, 7)),
                          ((0, 0), (2, 0)),
                          ((0, 0), (7, 0)),
                          ((0, 7), (0, 6)),
                          ((0, 7), (1, 7)),
                          ((7, 7), (6, 7)),
                          ((7, 7), (7, 6)),
                          ((7, 0), (6, 0)),
                          ((7, 0), (7, 1))])
@pytest.mark.parametrize("attacker, weapon",
                         [(Firefly, AcceleratingThorax),
                          (AlphaFirefly, EnhancedThorax),
                          (CannonMech, TaurusCannon)])
def test_projectile_weapon_on_sand_on_edge(object_on_tile, tile_pos, attacker_pos, attacker, weapon):
    tile_before = SandTile
    tile_before = tile_before(_object=object_on_tile() if object_on_tile is not None else None)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    if attacker_pos[0] > tile_pos[0]:
        vector = (-1, 0)
    elif attacker_pos[0] < tile_pos[0]:
        vector = (1, 0)
    elif attacker_pos[1] > tile_pos[1]:
        vector = (0, -1)
    elif attacker_pos[1] < tile_pos[1]:
        vector = (0, 1)
    else:
        raise Exception("Bad input data")
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    board.fill_object_position_cache()
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], GroundTile)
    assert board[tile_pos].has_smoke()


