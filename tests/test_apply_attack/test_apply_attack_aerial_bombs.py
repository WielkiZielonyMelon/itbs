import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import ForestTile, DamagedIceTile, IceTile, WaterTile, FrozenAcidTile, \
    DamagedFrozenAcidTile, AcidTile, DamagedFrozenLavaTile, FrozenLavaTile, LavaTile
from src.game_objects.vek import Hornet
from src.game_objects.weapons.aerial_bombs import AerialBombs


@pytest.mark.parametrize("mech_pos, vector, smoke_pos",
                         [((0, 0), (2, 0), (1, 0)),
                          ((0, 0), (0, 2), (0, 1)),
                          ((7, 0), (-2, 0), (6, 0)),
                          ((7, 0), (0, 2), (7, 1)),
                          ((7, 7), (-2, 0), (6, 7)),
                          ((7, 7), (0, -2), (7, 6)),
                          ((0, 7), (2, 0), (1, 7)),
                          ((0, 7), (0, -2), (0, 6))])
def test_aerial_bombs_on_empty_tile(mech_pos, vector, smoke_pos):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()


@pytest.mark.parametrize("mech_pos, vector, smoke_pos, frozen_tile, tile_exp",
                         [((0, 0), (2, 0), (1, 0), IceTile(_object=None), DamagedIceTile),
                          ((0, 0), (0, 2), (0, 1), DamagedIceTile(_object=None), WaterTile),
                          ((7, 0), (-2, 0), (6, 0), FrozenAcidTile(_object=None), DamagedFrozenAcidTile),
                          ((7, 0), (0, 2), (7, 1), DamagedFrozenAcidTile(_object=None), AcidTile),
                          ((7, 7), (-2, 0), (6, 7), FrozenLavaTile(_object=None), DamagedFrozenLavaTile),
                          ((7, 7), (0, -2), (7, 6), DamagedFrozenLavaTile(_object=None), LavaTile),
                          ((0, 7), (2, 0), (1, 7), IceTile(_object=None), DamagedIceTile),
                          ((0, 7), (0, -2), (0, 6), IceTile(_object=None), DamagedIceTile)])
def test_aerial_bombs_on_frozen_tile(mech_pos, vector, smoke_pos, frozen_tile, tile_exp):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)
    board[smoke_pos] = frozen_tile

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert isinstance(board[smoke_pos], tile_exp)


@pytest.mark.parametrize("mech_pos, vector, smoke_pos",
                         [((0, 0), (2, 0), (1, 0)),
                          ((0, 0), (0, 2), (0, 1)),
                          ((7, 0), (-2, 0), (6, 0)),
                          ((7, 0), (0, 2), (7, 1)),
                          ((7, 7), (-2, 0), (6, 7)),
                          ((7, 7), (0, -2), (7, 6)),
                          ((0, 7), (2, 0), (1, 7)),
                          ((0, 7), (0, -2), (0, 6))])
def test_aerial_bombs_on_mech(mech_pos, vector, smoke_pos):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)
    victim = CombatMech()
    board[smoke_pos].set_object(victim)
    exp_victim_health = victim.get_health() - 1

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert exp_victim_health == victim.get_health()


@pytest.mark.parametrize("mech_pos, vector, smoke_pos",
                         [((0, 0), (2, 0), (1, 0)),
                          ((0, 0), (0, 2), (0, 1)),
                          ((7, 0), (-2, 0), (6, 0)),
                          ((7, 0), (0, 2), (7, 1)),
                          ((7, 7), (-2, 0), (6, 7)),
                          ((7, 7), (0, -2), (7, 6)),
                          ((0, 7), (2, 0), (1, 7)),
                          ((0, 7), (0, -2), (0, 6))])
def test_aerial_bombs_on_mech_forest_tile(mech_pos, vector, smoke_pos):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)
    victim = CombatMech()
    board[smoke_pos] = ForestTile(_object=victim)

    exp_victim_health = victim.get_health() - 1

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert exp_victim_health == victim.get_health()
    assert isinstance(board[smoke_pos], ForestTile)
    assert not victim.is_on_fire()


@pytest.mark.parametrize("mech_pos, vector, smoke_pos, frozen_tile, tile_exp",
                         [((0, 0), (2, 0), (1, 0), IceTile(_object=None), DamagedIceTile),
                          ((0, 0), (0, 2), (0, 1), DamagedIceTile(_object=None), WaterTile),
                          ((7, 0), (-2, 0), (6, 0), FrozenAcidTile(_object=None), DamagedFrozenAcidTile),
                          ((7, 0), (0, 2), (7, 1), DamagedFrozenAcidTile(_object=None), AcidTile),
                          ((7, 7), (-2, 0), (6, 7), FrozenLavaTile(_object=None), DamagedFrozenLavaTile),
                          ((7, 7), (0, -2), (7, 6), DamagedFrozenLavaTile(_object=None), LavaTile),
                          ((0, 7), (2, 0), (1, 7), IceTile(_object=None), DamagedIceTile),
                          ((0, 7), (0, -2), (0, 6), IceTile(_object=None), DamagedIceTile)])
def test_aerial_bombs_on_frozen_tile_with_mech(mech_pos, vector, smoke_pos, frozen_tile, tile_exp):
    board = Board()
    mech = JetMech()
    victim = CombatMech()
    exp_victim_health = victim.get_health() - 1
    board[mech_pos].set_object(mech)
    board[smoke_pos] = frozen_tile
    board[smoke_pos].set_object(victim)

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert isinstance(board[smoke_pos], tile_exp)
    assert victim.get_health() == exp_victim_health


@pytest.mark.parametrize("mech_pos, vector, smoke_pos, frozen_tile, tile_exp",
                         [((0, 0), (2, 0), (1, 0), IceTile(_object=None), DamagedFrozenAcidTile),
                          ((0, 0), (0, 2), (0, 1), DamagedIceTile(_object=None), AcidTile),
                          ((7, 0), (-2, 0), (6, 0), FrozenAcidTile(_object=None), DamagedFrozenAcidTile),
                          ((7, 0), (0, 2), (7, 1), DamagedFrozenAcidTile(_object=None), AcidTile),
                          ((7, 7), (-2, 0), (6, 7), FrozenLavaTile(_object=None), DamagedFrozenAcidTile),
                          ((7, 7), (0, -2), (7, 6), DamagedFrozenLavaTile(_object=None), AcidTile),
                          ((0, 7), (2, 0), (1, 7), WaterTile(_object=None), AcidTile),
                          ((0, 7), (0, -2), (0, 6), WaterTile(_object=None), AcidTile)])
def test_aerial_bombs_on_frozen_tile_with_acided_vek(mech_pos, vector, smoke_pos, frozen_tile, tile_exp):
    board = Board()
    mech = JetMech()
    victim = Hornet()
    victim.set_acid()
    board[mech_pos].set_object(mech)
    board[smoke_pos] = frozen_tile
    board[smoke_pos].set_object(victim)

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert isinstance(board[smoke_pos], tile_exp)


@pytest.mark.parametrize("mech_pos, vector, smoke_pos_1, smoke_pos_2",
                         [((0, 0), (3, 0), (1, 0), (2,0)),
                          ((0, 0), (0, 3), (0, 1), (0, 2)),
                          ((7, 0), (-3, 0), (6, 0), (5, 0)),
                          ((7, 0), (0, 3), (7, 1), (7, 2)),
                          ((7, 7), (-3, 0), (6, 7), (5, 7)),
                          ((7, 7), (0, -3), (7, 6), (7, 5)),
                          ((0, 7), (3, 0), (1, 7), (2,  7)),
                          ((0, 7), (0, -3), (0, 6), (0, 5))])
def test_aerial_bombs_on_empty_tile_extra_range(mech_pos, vector, smoke_pos_1, smoke_pos_2):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(range_plus_1=True), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos_1].has_smoke()
    assert board[smoke_pos_2].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()


@pytest.mark.parametrize("mech_pos, vector, smoke_pos_1, smoke_pos_2",
                         [((0, 0), (3, 0), (1, 0), (2,0)),
                          ((0, 0), (0, 3), (0, 1), (0, 2)),
                          ((7, 0), (-3, 0), (6, 0), (5, 0)),
                          ((7, 0), (0, 3), (7, 1), (7, 2)),
                          ((7, 7), (-3, 0), (6, 7), (5, 7)),
                          ((7, 7), (0, -3), (7, 6), (7, 5)),
                          ((0, 7), (3, 0), (1, 7), (2,  7)),
                          ((0, 7), (0, -3), (0, 6), (0, 5))])
def test_aerial_bombs_on_mech_extra_range(mech_pos, vector, smoke_pos_1, smoke_pos_2):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)
    victim1 = CombatMech()
    board[smoke_pos_1].set_object(victim1)
    exp_victim_health_1 = victim1.get_health() - 1
    victim2 = CombatMech()
    board[smoke_pos_2].set_object(victim2)
    exp_victim_health_2 = victim2.get_health() - 1

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(range_plus_1=True), vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos_1].has_smoke()
    assert board[smoke_pos_2].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert exp_victim_health_1 == victim1.get_health()
    assert exp_victim_health_2 == victim2.get_health()


@pytest.mark.parametrize("mech_pos, vector, smoke_pos_1, smoke_pos_2",
                         [((0, 0), (3, 0), (1, 0), (2,0)),
                          ((0, 0), (0, 3), (0, 1), (0, 2)),
                          ((7, 0), (-3, 0), (6, 0), (5, 0)),
                          ((7, 0), (0, 3), (7, 1), (7, 2)),
                          ((7, 7), (-3, 0), (6, 7), (5, 7)),
                          ((7, 7), (0, -3), (7, 6), (7, 5)),
                          ((0, 7), (3, 0), (1, 7), (2,  7)),
                          ((0, 7), (0, -3), (0, 6), (0, 5))])
def test_aerial_bombs_on_vek_dies_extra_range_extra_damage(mech_pos, vector, smoke_pos_1, smoke_pos_2):
    board = Board()
    mech = JetMech()
    board[mech_pos].set_object(mech)
    victim1 = Hornet()
    board[smoke_pos_1].set_object(victim1)
    victim2 = Hornet()
    board[smoke_pos_2].set_object(victim2)

    attack = Attack(attacker=mech.get_id(), weapon=AerialBombs(damage_plus_1=True, range_plus_1=True),
                    vector=vector)
    apply_attack(board, attack)

    assert board[smoke_pos_1].has_smoke()
    assert board[smoke_pos_2].has_smoke()
    assert not board[mech_pos].has_smoke()

    mech_pos = board.find_object_position(mech)
    assert not board[mech_pos].has_smoke()
    assert board[smoke_pos_1].get_object() is None
    assert board[smoke_pos_2].get_object() is None
