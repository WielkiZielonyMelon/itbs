from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech, ArtilleryMech, CannonMech
from src.game_objects.mountain import Mountain
from src.game_objects.satellite_rocket import SatelliteRocket
from src.game_objects.tiles.tile import ForestTile, ForestFireTile, WaterTile
from src.game_objects.vek import AlphaFirefly, Firefly, ShellPsion, Hornet, Scarab, AlphaHornet
from src.game_objects.weapons.accelerating_thorax import EnhancedThorax, AcceleratingThorax
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.emerging import Emerging
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.spitting_glands import SpittingGlands
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist
from src.solver.battle_plans import get_battle_plans


def create_board_01():
    board = Board()

    board[(1, 1)].set_object(CivilianBuilding(health=1))
    board[(2, 1)].set_object(CivilianBuilding(health=2))
    board[(3, 1)] = WaterTile(_object=None)
    board[(4, 1)] = WaterTile(_object=None)
    board[(7, 1)] = WaterTile(_object=None)

    board[(1, 2)].set_object(CivilianBuilding(health=1))
    board[(2, 2)].set_object(CivilianBuilding(health=2))
    combat_mech = CombatMech()
    board[(3, 2)].set_object(combat_mech)
    board[(4, 2)].set_object(SatelliteRocket())
    board[(6, 2)] = WaterTile(_object=None)
    board[(7, 2)] = WaterTile(_object=None)

    artillery_mech = ArtilleryMech()
    board[(1, 3)].set_object(artillery_mech)

    board[(0, 4)] = ForestTile(_object=None)
    cannon_mech = CannonMech()
    board[(3, 4)].set_object(cannon_mech)
    board[(5, 4)] = WaterTile(_object=None)

    board[(1, 5)].set_object(CivilianBuilding(health=1))
    board[(2, 5)].set_object(CivilianBuilding(health=2))
    board[(5, 5)] = WaterTile(_object=None)

    board[(1, 6)].set_object(CivilianBuilding(health=1))
    board[(2, 6)].set_object(CivilianBuilding(health=2))
    board[(4, 6)].set_object(SatelliteRocket())
    board[(7, 6)] = WaterTile(_object=None)

    board[(5, 7)] = ForestTile(_object=None)
    board[(6, 7)] = WaterTile(_object=None)
    board[(7, 7)] = WaterTile(_object=None)

    enemy_actions = []

    obj = AlphaHornet()
    board[(2, 4)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=LaunchingStinger(), vector=(0, 1)))

    obj = Scarab()
    board[(6, 3)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=SpittingGlands(), vector=(-5, 0)))

    obj = Hornet()
    board[(3, 5)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=Stinger(), vector=(0, -1)))

    emerging = [Attack(attacker=(5, 3), weapon=Emerging(), vector=None),
                Attack(attacker=(6, 5), weapon=Emerging(), vector=None)]

    return board, [], enemy_actions, emerging, combat_mech, cannon_mech, artillery_mech


def test_scenario_03_01():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board_01()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)

    exp_attacks = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(0, 5)),
                   Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                   Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(5, 3)),
                   Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(1, 0)),
                   Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(1, 4)),
                   Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(1, 0))]

    attacks = plans[0].get_executed_orders()
    exp_score = 1810
    assert plans[0].get_score() == exp_score
    assert attacks == exp_attacks
