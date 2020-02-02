import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import FireTile, GroundTile
from src.game_objects.vek import Firefly, Hornet
from src.game_objects.weapons.freeze import Freeze
from src.game_objects.weapons.repair import Repair


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech()),
                          (Firefly()),
                          (Hornet())])
def test_move_object_over_fire_tile(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = FireTile(_object=None)

    board[pos].set_object(obj)
    board[pos].apply_tile_effects()

    tile = board[pos]
    obj = tile.get_object()
    assert obj.is_on_fire()


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech()),
                          (Firefly()),
                          (Hornet())])
def test_move_object_over_fire_tile_freeze(obj):
    board = Board()
    pos = (0, 0)
    obj = CombatMech()
    board[pos] = FireTile(_object=obj)
    board[pos].apply_tile_effects()
    attack = Attack(attacker=pos, weapon=Freeze(), vector=None)

    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert not obj.is_on_fire()
    assert isinstance(tile, GroundTile)


def test_fire_tile_repair():
    board = Board()
    pos = (0, 0)
    obj = CombatMech()
    board[pos] = FireTile(_object=obj)
    board[pos].apply_tile_effects()
    attack = Attack(attacker=obj.get_id(), weapon=Repair(),
                    vector=None)

    board.fill_object_position_cache()
    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert not obj.is_on_fire()
    assert isinstance(tile, GroundTile)


def test_fire_tile_exceptions():
    board = Board()
    pos = (0, 0)
    board[pos] = FireTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].freeze()

    assert "Cannot freeze FireTile. Convert to GroundTile and then freeze object" \
           in str(context.value)

    with pytest.raises(Exception) as context:
        board[pos].repair()

    assert "Repairing FireTile not possible. Repair any object on FireTile and convert tile to GroundTile" \
           in str(context.value)
