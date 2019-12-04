import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.weapons.dash import Dash


@pytest.mark.parametrize("mech_pos, attack_pos, direction, end_pos",
                         [((0, 0), (1, 0), (1, 0), (7, 0)),
                          ((1, 0), (2, 0), (1, 0), (7, 0)),
                          ((0, 0), (0, 1), (0, 1), (0, 7)),
                          ((0, 1), (0, 2), (0, 1), (0, 7)),
                          ((7, 7), (7, 6), (0, -1), (7, 0)),
                          ((7, 6), (7, 5), (0, -1), (7, 0)),
                          ((7, 7), (6, 7), (-1, 0), (0, 7)),
                          ((6, 7), (5, 7), (-1, 0), (0, 7))])
def test_apply_dash_unobstructed(mech_pos, attack_pos, direction, end_pos):
    board = Board()
    mech = CombatMech()

    board[mech_pos].set_object(mech)

    attack = Attack(attacker=mech.get_id(), weapon=Dash(), vector=direction)
    apply_attack(board, attack)

    assert mech == board[end_pos].get_object()


@pytest.mark.parametrize("mech_pos, attack_pos, direction, mech_blocker_pos, end_pos",
                         [((0, 0), (1, 0), (1, 0), (7, 0), (6, 0)),
                          ((0, 0), (1, 0), (1, 0), (4, 0), (3, 0)),
                          ((0, 0), (1, 0), (1, 0), (1, 0), (0, 0)),
                          ((0, 0), (0, 1), (0, 1), (0, 7), (0, 6)),
                          ((0, 0), (0, 1), (0, 1), (0, 4), (0, 3)),
                          ((0, 0), (0, 1), (0, 1), (0, 1), (0, 0))])
def test_apply_dash_blocked(mech_pos, attack_pos, direction, mech_blocker_pos, end_pos):
    board = Board()
    mech = CombatMech()
    mech_blocker = CombatMech()

    board[mech_pos].set_object(mech)
    board[mech_blocker_pos].set_object(mech_blocker)

    attack = Attack(attacker=mech.get_id(), weapon=Dash(), vector=direction)
    apply_attack(board, attack)

    assert mech == board[end_pos].get_object()
    assert mech_blocker == board[mech_blocker_pos].get_object()
