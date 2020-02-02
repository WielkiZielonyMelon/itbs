import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import ChasmTile
from src.game_objects.vek import Firefly, Hornet
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.push import Push


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (Firefly())])
def test_move_object_over_chasm_dies(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = ChasmTile(_object=None)

    src = (0, 1)

    board[src].set_object(obj)
    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=(0, 0))
    apply_attack(board, attack)

    tile = board[pos]
    obj = tile.get_object()
    assert obj is None


@pytest.mark.parametrize("obj",
                         [(JetMech()),
                          (Hornet())])
def test_move_object_over_chasm_survives(obj):
    board = Board()
    pos = (0, 0)
    board[pos] = ChasmTile(_object=None)

    src = (0, 1)

    board[src].set_object(obj)
    board.fill_object_position_cache()
    attack = Attack(attacker=obj.get_id(), weapon=Move(), vector=(0, 0))
    apply_attack(board, attack)

    tile = board[pos]
    obj_after = tile.get_object()
    assert obj == obj_after


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (Firefly())])
def test_push_object_over_chasm_dies(obj):
    board = Board()
    obj_pos = (1, 0)
    chasm_pos = (0, 0)
    direction = (-1, 0)
    board[chasm_pos] = ChasmTile(_object=None)

    board[obj_pos].set_object(obj)

    board.fill_object_position_cache()
    attack = Attack(attacker=obj_pos, weapon=Push(),
                    vector=direction)

    apply_attack(board, attack)

    tile = board[chasm_pos]
    obj = tile.get_object()
    assert obj is None


@pytest.mark.parametrize("obj",
                         [(JetMech()),
                          (Hornet())])
def test_push_object_over_chasm_survives(obj):
    board = Board()
    obj_pos = (1, 0)
    chasm_pos = (0, 0)
    direction = (-1, 0)
    board[chasm_pos] = ChasmTile(_object=None)

    board[obj_pos].set_object(obj)

    board.fill_object_position_cache()
    attack = Attack(attacker=obj_pos, weapon=Push(),
                    vector=direction)

    apply_attack(board, attack)

    tile = board[chasm_pos]
    obj_after = tile.get_object()
    assert obj == obj_after
