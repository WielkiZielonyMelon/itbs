from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech, ArtilleryMech, CannonMech
from src.game_objects.mountain import Mountain
from src.game_objects.satellite_rocket import SatelliteRocket, ReadySatelliteRocket
from src.game_objects.supply_train import SupplyTrainHead, SupplyTrainTail
from src.game_objects.tiles.tile import ForestTile, WaterTile
from src.game_objects.vek import Firefly, ShellPsion, Hornet, Scarab, AlphaHornet, BloodPsion, Leaper
from src.game_objects.weapons.accelerating_thorax import AcceleratingThorax
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.choo_choo import ChooChoo
from src.game_objects.weapons.emerging import Emerging
from src.game_objects.weapons.fangs import Fangs
from src.game_objects.weapons.launch import Launch
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.spitting_glands import SpittingGlands
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist
from src.solver.battle_plans import get_battle_plans


def create_board_01():
    board = Board()

    board[(0, 0)].set_object(CivilianBuilding(health=1))

    board[(0, 1)].set_object(CivilianBuilding(health=1))
    board[(3, 1)] = ForestTile(_object=None)
    board[(5, 1)] = WaterTile(_object=None)
    board[(7, 1)] = ForestTile(_object=None)

    board[(2, 2)] = ForestTile(_object=None)
    board[(3, 2)] = WaterTile(_object=None)
    board[(5, 2)] = WaterTile(_object=None)
    board[(6, 2)] = ForestTile(_object=None)

    board[(0, 3)].set_object(CivilianBuilding(health=1))
    artillery_mech = ArtilleryMech()
    board[(1, 3)].set_object(artillery_mech)
    board[(2, 3)] = ForestTile(_object=None)
    board[(3, 3)] = WaterTile(_object=None)

    board[(0, 4)].set_object(CivilianBuilding(health=2))
    cannon_mech = CannonMech()
    board[(3, 4)].set_object(cannon_mech)

    board[(1, 5)] = ForestTile(_object=None)
    combat_mech = CombatMech()
    board[(3, 5)].set_object(combat_mech)
    board[(5, 5)] = ForestTile(_object=None)

    board[(0, 6)].set_object(CivilianBuilding(health=2))
    supply_train_head = SupplyTrainHead()
    board[(4, 6)].set_object(supply_train_head)
    board[(7, 6)].set_object(Mountain())

    board[(0, 7)].set_object(CivilianBuilding(health=2))
    board[(3, 7)].set_object(Mountain())
    supply_train_tail = SupplyTrainTail()
    board[(4, 7)].set_object(supply_train_tail)
    board[(5, 7)].set_object(Mountain())
    board[(6, 7)].set_object(Mountain())
    board[(7, 7)].set_object(Mountain())

    enemy_actions = []

    obj = Firefly()
    board[(6, 4)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=AcceleratingThorax(), vector=(-1, 0)))

    obj = BloodPsion()
    board[(5, 6)].set_object(obj)

    obj = Leaper()
    board[(2, 4)].set_object(obj)
    board.apply_web((2, 4), (3, 4))
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=Fangs(), vector=(1, 0)))

    enemy_actions.append(Attack(attacker=(4, 6), weapon=ChooChoo(), vector=(0, -1)))

    emerging = [Attack(attacker=(7, 3), weapon=Emerging(), vector=None),
                Attack(attacker=(7, 4), weapon=Emerging(), vector=None)]

    return board, [], enemy_actions, emerging, combat_mech, cannon_mech, artillery_mech


def test_scenario_04_01():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board_01()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)

    exp_attacks = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(2, 2)),
                   Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(0, 2)),
                   Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(5, 3)),
                   Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, 1)),
                   Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(5, 4)),
                   Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(1, 0))]

    attacks = plans[0].get_executed_orders()
    exp_score = 1150
    assert plans[0].get_score() == exp_score
    assert attacks == exp_attacks
