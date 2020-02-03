from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding, PowerGenerator
from src.game_objects.mech import CombatMech, ArtilleryMech, CannonMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import WaterTile, ForestTile, TimePodTile, ForestFireTile, GroundTile
from src.game_objects.vek import AlphaFirefly, Firefly, ShellPsion, Hornet, Scarab, AlphaHornet
from src.game_objects.weapons.accelerating_thorax import EnhancedThorax, AcceleratingThorax
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.drown import Drown
from src.game_objects.weapons.emerging import Emerging
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.spitting_glands import SpittingGlands
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist
from src.solver.battle_plans import get_battle_plans


def create_board_01():
    board = Board()

    board[(1, 0)] = ForestTile(_object=None)

    board[(1, 1)] = ForestTile(_object=None)
    board[(2, 1)] = ForestTile(_object=None)
    cannon_mech = CannonMech()
    board[(3, 1)].set_object(cannon_mech)
    board[(5, 1)] = ForestTile(_object=None)
    board[(6, 1)] = ForestTile(_object=None)

    board[(1, 2)].set_object(CivilianBuilding(health=1))
    board[(2, 2)].set_object(CivilianBuilding(health=1))
    board[(3, 2)].set_object(Mountain())

    building = CivilianBuilding(health=1)
    building.set_shield()
    board[(1, 3)].set_object(building)
    board[(2, 3)].set_object(Mountain())
    board[(3, 3)].set_object(Mountain())
    board[(6, 3)].set_object(Mountain())
    board[(7, 3)].set_object(Mountain())

    board[(1, 4)].set_object(Mountain())
    board[(2, 4)].set_object(Mountain())
    building = CivilianBuilding(health=2)
    building.set_shield()
    board[(3, 4)].set_object(building)
    board[(6, 4)].set_object(Mountain())
    board[(7, 4)].set_object(Mountain())

    board[(1, 5)].set_object(Mountain())
    board[(2, 5)].set_object(CivilianBuilding(health=2))
    building = CivilianBuilding(health=2)
    building.set_shield()
    board[(3, 5)].set_object(building)

    artillery_mech = ArtilleryMech()
    board[(1, 6)].set_object(artillery_mech)
    combat_mech = CombatMech()
    board[(3, 6)] = ForestTile(_object=combat_mech)

    board[(4, 7)] = ForestTile(_object=None)

    enemy_actions = []

    obj = Scarab()
    board[(5, 6)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=SpittingGlands(), vector=(-4, 0)))

    obj = Firefly()
    board[(4, 1)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=AcceleratingThorax(), vector=(-1, 0)))

    obj = Firefly()
    board[(6, 5)] = ForestTile(_object=obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=AcceleratingThorax(), vector=(-1, 0)))

    emerging = [Attack(attacker=(5, 2), weapon=Emerging(), vector=None),
                Attack(attacker=(6, 2), weapon=Emerging(), vector=None)]

    return board, [], enemy_actions, emerging, combat_mech, cannon_mech, artillery_mech


def test_scenario_02_01():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board_01()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)

    exp_attacks = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(0, 6)),
                   Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(5, 0)),
                   Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(5, 0)),
                   Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, 1)),
                   Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(6, 6)),
                   Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(0, -1))]

    attacks = plans[0].get_executed_orders()
    exp_score = 1200
    assert plans[0].get_score() == exp_score
    assert attacks == exp_attacks


