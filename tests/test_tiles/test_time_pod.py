from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.tiles.tile import GroundTile, TimePodTile
from src.game_objects.vek import Firefly
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.titan_fist import TitanFist


def test_time_pod_titan_fist():
    board = Board()

    time_pod_pos = (1, 1)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is False
    board[time_pod_pos] = TimePodTile(_object=None)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is False

    mech_pos = (1, 2)
    mech = CombatMech()
    board[mech_pos].set_object(mech)
    attack_dir = (0, -1)

    attack = Attack(attacker=mech.get_id(), weapon=TitanFist(), vector=attack_dir)
    apply_attack(board, attack)

    assert isinstance(board[time_pod_pos], GroundTile)
    assert board.is_time_pod_destroyed() is True
    assert board.is_time_pod_picked_up() is False


def test_time_pod_pick_up():
    board = Board()

    time_pod_pos = (1, 1)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is False
    board[time_pod_pos] = TimePodTile(_object=None)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is False

    mech_pos = (1, 2)
    mech = CombatMech()
    board[mech_pos].set_object(mech)

    attack = Attack(attacker=mech.get_id(), weapon=Move(), vector=time_pod_pos)
    apply_attack(board, attack)

    assert isinstance(board[time_pod_pos], GroundTile)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is True


def test_time_pod_run_over_by_vek():
    board = Board()

    time_pod_pos = (1, 1)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is False
    board[time_pod_pos] = TimePodTile(_object=None)
    assert board.is_time_pod_destroyed() is False
    assert board.is_time_pod_picked_up() is False

    mech_pos = (1, 2)
    vek = Firefly()
    board[mech_pos].set_object(vek)

    attack = Attack(attacker=vek.get_id(), weapon=Move(), vector=time_pod_pos)
    apply_attack(board, attack)

    assert isinstance(board[time_pod_pos], GroundTile)
    assert board.is_time_pod_destroyed() is True
    assert board.is_time_pod_picked_up() is False
