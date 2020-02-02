import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.tiles.tile import FireTile, GroundTile
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.set_on_fire import SetOnFire


def test_set_object_on_fire_over_ground_tile():
    board = Board()
    pos = (0, 0)
    board[pos] = GroundTile(_object=None)

    obj = CombatMech()
    src = (0, 1)

    board[src].set_object(obj)
    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=(0, 0))

    apply_attack(board, attack)

    attack = Attack(attacker=pos, weapon=SetOnFire(),
                    vector=None)
    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert obj.is_on_fire()
    assert isinstance(tile, FireTile)


def test_ground_tile_exceptions():
    pos = (0, 0)
    board = Board()
    board[pos] = GroundTile(_object=None)

    with pytest.raises(Exception) as context:
        board[pos].set_fire()

    assert "Cannot set fire on GroundTile. Set object on fire and convert tile to FireTile" \
           in str(context.value)
