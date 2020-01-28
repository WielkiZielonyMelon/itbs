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
    for x in range(0, Board.BOARD_X_SIZE):
        for y in range(0, 2):
            board[(x, y)] = WaterTile(_object=None)

    high_tides = []
    for x in range(0, Board.BOARD_Y_SIZE):
        high_tides.append(Attack(attacker=(x, 2), weapon=Drown(), vector=None))

    board[(6, 2)] = ForestTile(_object=None)

    board[(0, 3)].set_object(CivilianBuilding(health=1))
    combat_mech = CombatMech()
    board[(3, 3)].set_object(combat_mech)

    board[(0, 4)].set_object(CivilianBuilding(health=1))
    board[(2, 4)].set_object(CivilianBuilding(health=1))
    board[(3, 4)].set_object(CivilianBuilding(health=2))

    board[(0, 5)].set_object(Mountain())
    artillery_mech = ArtilleryMech()
    board[(1, 5)] = ForestTile(_object=artillery_mech)
    board[(2, 5)].set_object(Mountain())
    board[(3, 5)].set_object(PowerGenerator())
    board[(5, 5)].set_object(CivilianBuilding(health=2))

    cannon_mech = CannonMech()
    board[(3, 6)].set_object(cannon_mech)
    board[(4, 6)] = TimePodTile(_object=None)

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


def create_board_02():
    board = Board()
    for x in range(0, Board.BOARD_X_SIZE):
        for y in range(0, 3):
            board[(x, y)] = WaterTile(_object=None)

    high_tides = []
    for x in range(1, Board.BOARD_Y_SIZE):
        high_tides.append(Attack(attacker=(x, 3), weapon=Drown(), vector=None))

    board[(0, 3)].set_object(CivilianBuilding(health=1))
    combat_mech = CombatMech()
    board[(4, 3)].set_object(combat_mech)

    board[(0, 4)].set_object(CivilianBuilding(health=1))
    artillery_mech = ArtilleryMech()
    board[(1, 4)].set_object(artillery_mech)
    board[(2, 4)].set_object(CivilianBuilding(health=1))
    board[(3, 4)].set_object(CivilianBuilding(health=2))

    board[(0, 5)].set_object(Mountain())
    board[(1, 5)] = ForestTile(_object=None)
    board[(2, 5)].set_object(Mountain())
    board[(3, 5)].set_object(PowerGenerator())
    board[(4, 5)] = ForestFireTile(_object=None)
    board[(5, 5)].set_object(CivilianBuilding(health=2))

    cannon_mech = CannonMech()
    board[(4, 6)].set_object(cannon_mech)

    board[(2, 7)] = ForestTile(_object=None)
    board[(7, 7)].set_object(Mountain())

    enemy_actions = []

    obj = ShellPsion()
    board[(5, 3)].set_object(obj)

    obj = Hornet()
    board[(5, 6)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=Stinger(), vector=(-1, 0)))

    obj = Scarab()
    board[(4, 4)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=SpittingGlands(), vector=(0, -2)))

    emerging = [Attack(attacker=(5, 4), weapon=Emerging(), vector=None),
                Attack(attacker=(6, 4), weapon=Emerging(), vector=None),
                Attack(attacker=(6, 5), weapon=Emerging(), vector=None)]

    return board, high_tides, enemy_actions, emerging, combat_mech, cannon_mech, artillery_mech


def create_board_03():
    board = Board()
    for x in range(0, Board.BOARD_X_SIZE):
        for y in range(0, 4):
            board[(x, y)] = WaterTile(_object=None)

    high_tides = [Attack(attacker=(1, 4), weapon=Drown(), vector=None)]
    for x in range(4, Board.BOARD_Y_SIZE):
        high_tides.append(Attack(attacker=(x, 4), weapon=Drown(), vector=None))

    board[(0, 3)] = GroundTile(_object=CivilianBuilding(health=1))
    artillery_mech = ArtilleryMech()
    board[(1, 3)].set_object(artillery_mech)
    combat_mech = CombatMech()
    board[(3, 3)].set_object(combat_mech)

    board[(0, 4)].set_object(CivilianBuilding(health=1))
    board[(2, 4)].set_object(CivilianBuilding(health=1))
    board[(3, 4)].set_object(CivilianBuilding(health=2))

    board[(0, 5)].set_object(Mountain())
    board[(1, 5)] = ForestTile(_object=None)
    board[(2, 5)].set_object(Mountain())
    board[(3, 5)].set_object(PowerGenerator())
    board[(4, 5)] = ForestFireTile(_object=None)
    board[(5, 5)].set_object(CivilianBuilding(health=2))

    board[(2, 7)] = ForestTile(_object=None)
    cannon_mech = CannonMech()
    board[(4, 7)].set_object(cannon_mech)
    board[(7, 7)].set_object(Mountain())

    enemy_actions = []

    obj = Hornet()
    board[(3, 6)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=Stinger(), vector=(0, -1)))

    obj = Scarab()
    board[(6, 4)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=SpittingGlands(), vector=(-3, 0)))

    obj = AlphaHornet()
    board[(4, 4)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=LaunchingStinger(), vector=(-1, 0)))

    obj = Hornet()
    board[(2, 3)].set_object(obj)
    enemy_actions.append(Attack(attacker=obj.get_id(), weapon=Stinger(), vector=(-1, 0)))

    emerging = []

    return board, high_tides, enemy_actions, emerging, combat_mech, cannon_mech, artillery_mech


def test_scenario_01_01():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board_01()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)

    exp_attacks = [[Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(1, 0)),
                    Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                    Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 6)),
                    Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1))],

                   [Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 6)),
                    Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(1, 0)),
                    Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                    Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1))]]

    attacks = plans[0].get_executed_orders()
    exp_score = 1205
    assert plans[0].get_score() == exp_score
    assert attacks in exp_attacks


def test_scenario_01_02():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board_02()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)

    exp_attacks = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(1, 3)),
                   Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(4, 0)),
                   Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 7)),
                   Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(0, -1)),
                   Attack(attacker=combat_mech.get_id(), weapon=TitanFist(), vector=(1, 0))]

    attacks = plans[0].get_executed_orders()
    exp_score = 1000
    assert plans[0].get_score() == exp_score
    assert attacks == exp_attacks


def test_scenario_01_03():
    board, environment, enemy_actions, emerging, \
        combat_mech, cannon_mech, artillery_mech = create_board_03()
    enemy_actions.extend(emerging)
    environment.extend(enemy_actions)
    plans = get_battle_plans(board, size=1, enemy_attacks=environment)

    exp_attacks = [Attack(attacker=artillery_mech.get_id(), weapon=Move(), vector=(1, 5)),
                   Attack(attacker=artillery_mech.get_id(), weapon=Artemis(), vector=(3, 0)),
                   Attack(attacker=combat_mech.get_id(), weapon=Move(), vector=(3, 2)),
                   Attack(attacker=cannon_mech.get_id(), weapon=Move(), vector=(4, 6)),
                   Attack(attacker=cannon_mech.get_id(), weapon=TaurusCannon(), vector=(-1, 0))]

    attacks = plans[0].get_executed_orders()
    exp_score = 1160
    assert plans[0].get_score() == exp_score
    assert attacks == exp_attacks
