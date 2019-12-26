import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.tiles.tile import DamagedIceTile, IceTile, ForestTile, ForestFireTile, WaterTile, FrozenAcidTile, \
    DamagedFrozenAcidTile, AcidTile
from src.game_objects.vek import Hornet, AlphaHornet
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("tile_before, tile_after",
                         [(ForestTile, ForestFireTile),
                          (IceTile, DamagedIceTile),
                          (DamagedIceTile, WaterTile),
                          (FrozenAcidTile, DamagedFrozenAcidTile),
                          (DamagedFrozenAcidTile, AcidTile)])
@pytest.mark.parametrize("tile_pos, attacker_pos",
                         [((0, 0), (0, 1)),
                          ((0, 0), (1, 0)),
                          ((0, 7), (0, 6)),
                          ((0, 7), (1, 7)),
                          ((7, 7), (6, 7)),
                          ((7, 7), (7, 6)),
                          ((7, 0), (6, 0)),
                          ((7, 0), (7, 1)),
                          ((1, 1), (0, 1)),
                          ((1, 1), (1, 0)),
                          ((1, 1), (1, 2)),
                          ((1, 1), (2, 1))])
@pytest.mark.parametrize("attacker, weapon",
                         [(CombatMech, TitanFist),
                          (Hornet, Stinger),
                          (AlphaHornet, LaunchingStinger)])
def test_melee_weapon_on_damageable_tile(tile_before, tile_after, tile_pos, attacker_pos, attacker, weapon):
    tile_before = tile_before(_object=None)
    attacker = attacker()
    weapon = weapon()

    board = Board()
    board[tile_pos] = tile_before
    board[attacker_pos].set_object(attacker)

    vector = (tile_pos[0] - attacker_pos[0], tile_pos[1] - attacker_pos[1])
    attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
    apply_attack(board, attack)

    assert isinstance(board[tile_pos], tile_after)


