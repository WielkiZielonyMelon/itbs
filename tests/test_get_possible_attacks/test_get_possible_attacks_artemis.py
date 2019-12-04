import pytest
import unittest

from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import ArtilleryMech
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.artemis import Artemis
from src.helpers.get_possible_attacks import get_possible_attacks


@pytest.mark.parametrize("mech_pos,vectors",
                         [((0, 0), [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]),
                          ((7, 0), [(-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                                    (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]),
                           ((7, 7), [(-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                                     (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]),
                          ((0, 7), [(0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7),
                                    (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)])])
def test_get_possible_attacks_artemis_in_corners(mech_pos, vectors):
    board = Board()
    mech = ArtilleryMech()

    board[mech_pos].set_object(mech)
    attacks = get_possible_attacks(board, mech)

    expected_attacks = [Attack(attacker=mech.get_id(), weapon=Artemis(), vector=v) for v in vectors]
    expected_attacks.append(Attack(attacker=mech.get_id(), weapon=Repair(), vector=None))
    unittest.TestCase().assertCountEqual(attacks, expected_attacks)


def test_1_1():
    board = Board()
    pos = (1, 1)
    mech = ArtilleryMech()

    board[pos].set_object(mech)
    attacks = get_possible_attacks(board, mech)
    vectors = [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    expected_attacks = [Attack(attacker=mech.get_id(), weapon=Artemis(), vector=v) for v in vectors]
    expected_attacks.append(Attack(attacker=mech.get_id(), weapon=Repair(), vector=None))
    unittest.TestCase().assertCountEqual(attacks, expected_attacks)
