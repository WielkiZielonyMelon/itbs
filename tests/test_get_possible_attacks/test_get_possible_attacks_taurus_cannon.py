import unittest

import pytest

from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CannonMech
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.helpers.get_possible_attacks import get_possible_attacks


@pytest.mark.parametrize("pos,dir_1,dir_2",
                         [((0, 0), (1, 0), (0, 1)),
                          ((7, 0), (-1, 0), (0, 1)),
                          ((7, 7), (-1, 0), (0, -1)),
                          ((0, 7), (1, 0), (0, -1))])
def test_get_possible_attacks_taurus_cannon_in_corners(pos, dir_1, dir_2):
    board = Board()
    mech = CannonMech()

    board[pos].set_object(mech)
    attacks = get_possible_attacks(board, mech)

    expected_attacks = [Attack(attacker=mech.get_id(), weapon=TaurusCannon(), vector=dir_1),
                        Attack(attacker=mech.get_id(), weapon=TaurusCannon(), vector=dir_2),
                        Attack(attacker=mech.get_id(), weapon=Repair(), vector=None)]
    unittest.TestCase().assertCountEqual(attacks, expected_attacks)


def test_2_2():
    board = Board()
    pos = (2, 2)
    mech = CannonMech()

    board[pos].set_object(mech)
    attacks = get_possible_attacks(board, mech)
    expected_attacks = [Attack(attacker=mech.get_id(), weapon=TaurusCannon(), vector=(-1, 0)),
                        Attack(attacker=mech.get_id(), weapon=TaurusCannon(), vector=(1, 0)),
                        Attack(attacker=mech.get_id(), weapon=TaurusCannon(), vector=(0, -1)),
                        Attack(attacker=mech.get_id(), weapon=TaurusCannon(), vector=(0, 1)),
                        Attack(attacker=mech.get_id(), weapon=Repair(), vector=None)]
    unittest.TestCase().assertCountEqual(attacks, expected_attacks)
