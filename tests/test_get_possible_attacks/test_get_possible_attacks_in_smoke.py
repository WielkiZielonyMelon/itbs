import pytest

from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import WaterTile, LavaTile, AcidTile, SandTile, ForestTile, GroundTile
from src.helpers.get_possible_attacks import get_possible_attacks


@pytest.mark.parametrize("stable_tile",
                         [(GroundTile(_object=None)),
                          (ForestTile(_object=None)),
                          (SandTile(_object=None))])
def test_get_possible_attacks_in_land_smoke_combat_mech(stable_tile):
    board = Board()
    mech0 = CombatMech()
    stable_tile.set_smoke()
    stable_tile_pos = (0, 0)

    board[stable_tile_pos] = stable_tile
    board[stable_tile_pos].set_object(mech0)
    attacks = get_possible_attacks(board, mech0)

    assert attacks == []


@pytest.mark.parametrize("liquid_tile",
                         [(WaterTile(_object=None)),
                          (LavaTile(_object=None)),
                          (AcidTile(_object=None))])
def test_get_possible_attacks_in_water_smoke_jet_mech(liquid_tile):
    board = Board()
    mech0 = JetMech()
    liquid_tile.set_smoke()
    liquid_pos = (0, 0)

    board[liquid_pos] = liquid_tile
    board[liquid_pos].set_object(mech0)
    attacks = get_possible_attacks(board, mech0)

    assert attacks == []
