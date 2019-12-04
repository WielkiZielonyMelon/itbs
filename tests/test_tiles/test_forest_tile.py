import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import ForestTile, ForestFireTile
from src.game_objects.vek import Hornet, Firefly
from src.game_objects.weapons.freeze import Freeze
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.set_on_fire import SetOnFire
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("weapon",
                         [(TitanFist())])
def test_forest_tile_repair(weapon):
    board = Board()
    fire_pos = (1, 0)
    direction = (1, 0)

    puncher = CombatMech()
    puncher_pos = (fire_pos[0] - direction[0], fire_pos[1] - direction[1])
    board[puncher_pos].set_object(puncher)

    board[fire_pos] = ForestTile(_object=None)

    attack = Attack(attacker=puncher.get_id(), weapon=weapon,
                    vector=direction)
    apply_attack(board, attack)

    # Lamely put another mech to repair
    repairer = CombatMech()
    board[fire_pos].set_object(repairer)
    board[fire_pos].apply_tile_effects()

    repair = Attack(attacker=repairer.get_id(), weapon=Repair(),
                    vector=None)

    tile = board[fire_pos]
    assert isinstance(tile, ForestFireTile)

    apply_attack(board, repair)

    tile = board[fire_pos]
    assert isinstance(tile, ForestTile)


def test_forest_tile_exceptions():
    pos = (0, 0)
    board = Board()
    board[pos] = ForestTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].set_fire()

    assert "Cannot set fire on ForestTile. Set object on fire and convert tile to ForestFireTile" \
           in str(context.value)


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech()),
                          (Firefly()),
                          (Hornet())])
def test_freeze_object_over_forest_fire(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = ForestFireTile(_object=obj)
    board[pos].apply_tile_effects()
    attack = Attack(attacker=pos, weapon=Freeze(), vector=None)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert not obj.is_on_fire()
    assert isinstance(tile, ForestTile)


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech())])
def test_repair_object_over_forest_fire(obj):
    board = Board()
    pos = (0, 0)
    obj = CombatMech()
    board[pos] = ForestFireTile(_object=obj)
    board[pos].apply_tile_effects()
    attack = Attack(obj.get_id(), weapon=Repair(), vector=None)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert not obj.is_on_fire()
    assert isinstance(tile, ForestTile)


def test_forest_fire_tile_exceptions():
    pos = (0, 0)
    board = Board()
    board[pos] = ForestFireTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].freeze()

    assert "Cannot freeze ForestFireTile. Convert to ForestTile and then freeze object" \
           in str(context.value)

    with pytest.raises(Exception) as context:
        board[pos].repair()

    assert "Repairing ForestFireTile not possible. Convert to ForestTile first and then repair object" \
           in str(context.value)
