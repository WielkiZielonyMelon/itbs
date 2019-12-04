import pytest

from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding, PowerGenerator
from src.game_objects.mech import CombatMech, ArtilleryMech, CannonMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import WaterTile, ForestTile
from src.game_objects.vek import AlphaFirefly, Firefly
from src.game_objects.weapons.accelerating_thorax import EnhancedThorax, AcceleratingThorax
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.drown import Drown
from src.game_objects.weapons.emerging import Emerging
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist
from src.solver.battle_plans import get_battle_plans


def create_board():
    board = Board()
    for x in range(0, Board.BOARD_MAX_X_SIZE):
        for y in range(0, 2):
            board[(x, y)] = WaterTile(_object=None)

    high_tides = []
    for x in range(0, Board.BOARD_MAX_Y_SIZE):
        high_tides.append(Attack(attacker=(x, 2), weapon=Drown(), vector=None))

    board[(6, 2)] = ForestTile(_object=None)

    board[(0, 3)].set_object(CivilianBuilding(health=1))
    combat_mech = CombatMech()
    board[(3, 3)].set_object(combat_mech)
    # TODO: do not modify max moves
    board[(3, 3)].get_object()._moves = 1

    board[(0, 4)].set_object(CivilianBuilding(health=1))
    board[(2, 4)].set_object(CivilianBuilding(health=1))
    board[(3, 4)].set_object(CivilianBuilding(health=2))

    board[(0, 5)].set_object(Mountain())
    artillery_mech = ArtilleryMech()
    board[(1, 5)] = ForestTile(_object=artillery_mech)
    # TODO: do not modify max moves
    board[(1, 5)].get_object()._moves = 1
    board[(2, 5)].set_object(Mountain())
    board[(3, 5)].set_object(PowerGenerator())
    board[(5, 5)].set_object(CivilianBuilding(health=2))

    cannon_mech = CannonMech()
    board[(3, 6)].set_object(cannon_mech)
    # TODO: do not modify max moves
    board[(3, 6)].get_object()._moves = 1
    # TODO: Add timepod
    # board[(4, 6)] = TimePod()

    board[(2, 7)] = ForestTile(_object=None)
    board[(7, 7)].set_object(Mountain())

    enemy_actions = []

    obj = Firefly()
    board[(4, 4)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=AcceleratingThorax(), vector=(-1, 0)))

    obj = AlphaFirefly()
    board[(4, 3)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=EnhancedThorax(), vector=(-1, 0)))

    obj = Firefly()
    board[(4, 5)] = ForestTile(_object=obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=AcceleratingThorax(), vector=(1, 0)))

    emerging = [Attack(attacker=(5, 3), weapon=Emerging(), vector=None),
                Attack(attacker=(7, 4), weapon=Emerging(), vector=None),
                Attack(attacker=(6, 5), weapon=Emerging(), vector=None)]

    return board, high_tides, enemy_actions, emerging, combat_mech, cannon_mech, artillery_mech


def test_scenario_01_01():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)
    exp_attacks_01 = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(1, 4)),
                      Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 6)),
                      Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1)),
                      Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                      Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(4, 3)),
                      Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(0, 1))]

    # TODO: This will not work after placing time pod
    exp_attacks_02 = [Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 6)),
                      Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1)),
                      Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(1, 4)),
                      Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                      Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(4, 3)),
                      Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(0, 1))]

    # TODO: This will not work after placing time pod
    exp_attacks_03 = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(1, 4)),
                      Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                      Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(4, 3)),
                      Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 7)),
                      Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1)),
                      Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(0, 1))]

    # TODO: This will not work after placing time pod
    exp_attacks_04 = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(1, 4)),
                      Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=( 3, 0)),
                      Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 7)),
                      Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1)),
                      Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(4, 3)),
                      Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(0, 1))]

    attacks = plans[0].get_executed_orders()
    exp_score = 575
    assert plans[0].get_score() == exp_score
    assert attacks in [exp_attacks_01] #, exp_attacks_02, exp_attacks_03, exp_attacks_04]
