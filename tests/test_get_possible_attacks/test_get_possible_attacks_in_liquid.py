import unittest

import pytest

from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import WaterTile, LavaTile, AcidTile
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.repair import Repair
from src.helpers.get_possible_attacks import get_possible_attacks


@pytest.mark.parametrize("liquid_tile",
                         [(WaterTile(_object=None)),
                          (LavaTile(_object=None)),
                          (AcidTile(_object=None))])
def test_get_possible_attacks_in_water_combat_mech(liquid_tile):
    board = Board()
    mech0 = CombatMech()
    liquid_pos = (0, 0)

    board[liquid_pos] = liquid_tile
    board[liquid_pos].set_object(mech0)
    attacks = get_possible_attacks(board, mech0)

    assert attacks == []


@pytest.mark.parametrize("liquid_tile",
                         [(WaterTile(_object=None)),
                          (LavaTile(_object=None)),
                          (AcidTile(_object=None))])
def test_get_possible_attacks_in_water_jet_mech(liquid_tile):
    board = Board()
    mech0 = JetMech()
    liquid_pos = (0, 0)

    board[liquid_pos] = liquid_tile
    board[liquid_pos].set_object(mech0)
    attacks = get_possible_attacks(board, mech0)
    exp_attacks = [Attack(attacker=mech0.get_id(), weapon=AerialBombs(), vector=(0, 2)),
                   Attack(attacker=mech0.get_id(), weapon=AerialBombs(), vector=(2, 0)),
                   Attack(attacker=mech0.get_id(), weapon=Repair(), vector=None)]

    tc = unittest.TestCase()
    tc.assertCountEqual(attacks, exp_attacks)
