import unittest

from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import AcidTile
from src.game_objects.weapons.accelerating_thorax import AcceleratingThorax
from src.game_objects.weapons.titan_fist import TitanFist
from src.game_objects.weapons.move import Move
from src.game_objects.vek import Firefly, Hornet, AlphaFirefly
from src.solver.battle_plans import get_battle_plans
from src.helpers.get_score_of_board import get_score_of_board


def test_find_player_objects():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (1, 2)
    board[mech0_pos].set_object(mech0)
    mech1 = CombatMech()
    mech1_pos = (4, 5)
    board[mech1_pos].set_object(mech1)
    mech2 = CombatMech()
    mech2_pos = (7, 0)
    board[mech2_pos].set_object(mech2)
    mech3 = JetMech()
    mech3_pos = (3, 2)
    board[mech3_pos].set_object(mech3)

    vek0 = Firefly()
    board[(0, 0)].set_object(vek0)
    vek1 = Firefly()
    board[(3, 4)].set_object(vek1)
    vek2 = Firefly()
    board[(7, 7)].set_object(vek2)
    vek3 = Hornet()
    board[(5, 5)].set_object(vek3)

    expected_pos = [mech0_pos, mech1_pos, mech2_pos, mech3_pos]
    received = board.find_player_objects()

    unittest.TestCase().assertCountEqual(expected_pos, received)


def test_find_object_position():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (1, 2)
    board[mech0_pos].set_object(mech0)
    mech1 = CombatMech()
    mech1_pos = (4, 5)
    board[mech1_pos].set_object(mech1)
    mech2 = CombatMech()
    mech2_pos = (7, 0)
    board[mech2_pos].set_object(mech2)
    mech3 = JetMech()
    mech3_pos = (3, 2)
    board[mech3_pos].set_object(mech3)

    vek0 = Firefly()
    vek0_pos = (0, 0)
    board[vek0_pos].set_object(vek0)
    vek1 = Firefly()
    vek1_pos = (3, 4)
    board[vek1_pos].set_object(vek1)
    vek2 = Firefly()
    vek2_pos = (7, 7)
    board[vek2_pos].set_object(vek2)
    vek3 = Hornet()
    vek3_pos = (5, 5)
    board[vek3_pos].set_object(vek3)

    tc = unittest.TestCase()

    tc.assertEqual(board.find_object_position(mech0),
                   mech0_pos)
    tc.assertEqual(board.find_object_position(mech1),
                   mech1_pos)
    tc.assertEqual(board.find_object_position(mech2),
                   mech2_pos)
    tc.assertEqual(board.find_object_position(mech3),
                   mech3_pos)

    tc.assertEqual(board.find_object_position(vek0), vek0_pos)
    tc.assertEqual(board.find_object_position(vek1), vek1_pos)
    tc.assertEqual(board.find_object_position(vek2), vek2_pos)
    tc.assertEqual(board.find_object_position(vek3), vek3_pos)


def test_get_score_of_board():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (1, 2)
    board[mech0_pos].set_object(mech0)
    mech1 = CombatMech()
    mech1_pos = (4, 5)
    board[mech1_pos].set_object(mech1)
    mech2 = CombatMech()
    mech2_pos = (7, 0)
    board[mech2_pos].set_object(mech2)
    mech3 = JetMech()
    mech3_pos = (3, 2)
    board[mech3_pos].set_object(mech3)

    vek0 = Firefly()
    board[(0, 0)].set_object(vek0)
    vek1 = Firefly()
    board[(3, 4)].set_object(vek1)
    vek2 = Firefly()
    board[(7, 7)].set_object(vek2)
    vek3 = Hornet()
    board[(5, 5)].set_object(vek3)

    expected_score = 400
    unittest.TestCase().assertEqual(expected_score, get_score_of_board(board))


def test_solver_get_best_battle_plans_mech_can_die():
    """Scenario where one mech can kill another"""
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)

    mech1 = CombatMech()
    mech1_pos = (0, 1)

    mountain0 = Mountain()
    mountain0_pos = (0, 2)

    board[mech0_pos].set_object(mech0)
    board[mech1_pos].set_object(mech1)
    board[mountain0_pos].set_object(mountain0)

    plans = get_battle_plans(board, size=1, enemy_attacks=[])
    exp_score = 400
    plan0 = plans[0]
    tc = unittest.TestCase()
    tc.assertEqual(exp_score, plan0.get_score())


def test_solver_get_best_battle_plans_combat_mech():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)

    vek0 = Firefly()
    vek0_pos = (0, 1)

    acid_pool_pos = (0, 2)

    board[mech0_pos].set_object(mech0)

    board[vek0_pos].set_object(vek0)
    board[acid_pool_pos] = AcidTile(_object=None)

    plans = get_battle_plans(board, size=1, enemy_attacks=[])
    exp_score_0 = 200
    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=TitanFist(),
                            vector=vek0_pos)]
    exp_attacks = [exp_attacks_0]

    plan0 = plans[0]
    tc = unittest.TestCase()
    tc.assertEqual(exp_score_0, plan0.get_score())

    attacks = [plan0.get_executed_orders()]

    tc.assertCountEqual(exp_attacks, attacks)


def test_solver_combat_mech_firefly_attacks_acid_pool():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)

    vek0 = Firefly()
    vek0_pos = (0, 1)
    vek0_vec = (0, -1)
    vek0_attack = Attack(attacker=vek0.get_id(), weapon=AcceleratingThorax(),
                         vector=vek0_vec)

    acid_pool_pos = (0, 2)

    board[mech0_pos].set_object(mech0)

    board[vek0_pos].set_object(vek0)
    board[acid_pool_pos] = AcidTile(_object=None)

    plans = get_battle_plans(board, size=1, enemy_attacks=[vek0_attack])
    exp_score_0 = 200
    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=TitanFist(),
                            vector=vek0_pos)]
    exp_attacks = [exp_attacks_0]

    plan0 = plans[0]
    tc = unittest.TestCase()
    tc.assertEqual(exp_score_0, plan0.get_score())

    attacks = [plan0.get_executed_orders()]

    tc.assertCountEqual(exp_attacks, attacks)


def test_solver_combat_mech_firefly_attacks():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)

    vek0 = Firefly()
    vek0_pos = (0, 1)
    vek0_vec = (0, -1)
    vek0_attack = Attack(attacker=vek0.get_id(), weapon=AcceleratingThorax(),
                         vector=vek0_vec)

    board[mech0_pos].set_object(mech0)

    board[vek0_pos].set_object(vek0)

    plans = get_battle_plans(board, size=1, enemy_attacks=[vek0_attack])
    exp_score_0 = 130
    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=Move(),
                            vector=(1, 1)),
                     Attack(attacker=mech0.get_id(), weapon=TitanFist(),
                            vector=(-1, 0))]
    exp_attacks = [exp_attacks_0]

    plan0 = plans[0]
    tc = unittest.TestCase()
    tc.maxDiff = None
    tc.assertEqual(exp_score_0, plan0.get_score())

    attacks = [plan0.get_executed_orders()]

    tc.assertCountEqual(exp_attacks, attacks)


def test_solver_get_best_battle_plans_combat_mech_kill():
    board = Board()
    mech0 = CombatMech()
    mech0_pos = (0, 0)

    vek0 = Firefly()
    vek0_pos = (0, 1)

    mountain0 = Mountain()
    mountain_pos = (0, 2)

    board[mech0_pos].set_object(mech0)
    board[vek0_pos].set_object(vek0)
    board[mountain_pos].set_object(mountain0)

    exp_score = 200
    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=TitanFist(),
                            vector=vek0_pos)]
    exp_attacks = [exp_attacks_0]

    plans = get_battle_plans(board, size=1, enemy_attacks=[])
    plan0 = plans[0]

    tc = unittest.TestCase()
    tc.assertEqual(exp_score, plan0.get_score())

    attacks = [plan0.get_executed_orders()]

    tc.assertCountEqual(exp_attacks, attacks)


def test_solver_get_best_battle_plans_two_combat_mech_cooperation_01():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (0, 0)

    vek0 = Firefly()
    vek0_pos = (0, 2)

    mech1 = CombatMech()
    mech1_pos = (0, 7)

    board[mech0_pos].set_object(mech0)
    board[vek0_pos].set_object(vek0)
    board[mech1_pos].set_object(mech1)

    exp_score = 400

    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=Move(), vector=(0, 1)),
                     Attack(attacker=mech0.get_id(), weapon=TitanFist(), vector=(0, 1)),
                     Attack(attacker=mech1.get_id(), weapon=Move(), vector=(0, 4)),
                     Attack(attacker=mech1.get_id(), weapon=TitanFist(), vector=(0, -1))
                     ]
    exp_attacks = [exp_attacks_0]

    plans = get_battle_plans(board, size=1, enemy_attacks=[])

    tc = unittest.TestCase()
    plan0 = plans[0]
    attacks = [plan0.get_executed_orders()]
    tc.assertCountEqual(exp_attacks, attacks)

    tc.assertEqual(exp_score, plan0.get_score())


def test_solver_get_best_battle_plans_two_combat_mech_cooperation_02():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (1, 0)

    vek0 = Firefly()
    vek0_pos = (0, 2)

    mech1 = CombatMech()
    mech1_pos = (0, 7)

    board[mech0_pos].set_object(mech0)
    board[vek0_pos].set_object(vek0)
    board[mech1_pos].set_object(mech1)

    exp_score = 400

    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=Move(), vector=(0, 1)),
                     Attack(attacker=mech0.get_id(), weapon=TitanFist(), vector=(0, 1)),
                     Attack(attacker=mech1.get_id(), weapon=Move(), vector=(0, 4)),
                     Attack(attacker=mech1.get_id(), weapon=TitanFist(), vector=(0, -1))
                     ]
    exp_attacks = exp_attacks_0

    plans = get_battle_plans(board, size=1, enemy_attacks=[])

    tc = unittest.TestCase()
    plan0 = plans[0]
    attacks = plan0.get_executed_orders()
    tc.assertCountEqual(exp_attacks, attacks)

    tc.assertEqual(exp_score, plan0.get_score())


def test_solver_get_best_battle_plans_three_combat_mech_cooperation_mountain_helpers():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (0, 1)

    mech1 = CombatMech()
    mech1_pos = (1, 1)

    mech2 = CombatMech()
    mech2_pos = (7, 0)

    vek0 = AlphaFirefly()
    vek0_pos = (1, 0)

    board[mech0_pos].set_object(mech0)
    board[mech1_pos].set_object(mech1)
    board[mech2_pos].set_object(mech2)
    board[vek0_pos].set_object(vek0)

    # Use mountains to block things
    mountain0 = Mountain()
    board[(0, 2)].set_object(mountain0)
    mountain1 = Mountain()
    board[(1, 2)].set_object(mountain1)
    mountain2 = Mountain()
    board[(2, 1)].set_object(mountain2)
    mountain3 = Mountain()
    board[(3, 1)].set_object(mountain3)
    mountain4 = Mountain()
    board[(4, 1)].set_object(mountain4)
    mountain5 = Mountain()
    board[(5, 1)].set_object(mountain5)
    mountain6 = Mountain()
    board[(6, 1)].set_object(mountain6)
    mountain7 = Mountain()
    board[(7, 1)].set_object(mountain7)

    exp_score = 600

    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=Move(), vector=(0, 0)),
                     Attack(attacker=mech0.get_id(), weapon=TitanFist(), vector=(1, 0)),
                     Attack(attacker=mech1.get_id(), weapon=Move(), vector=(1, 0)),
                     Attack(attacker=mech1.get_id(), weapon=TitanFist(), vector=(1, 0)),
                     Attack(attacker=mech2.get_id(), weapon=Move(), vector=(4, 0)),
                     Attack(attacker=mech2.get_id(), weapon=TitanFist(), vector=(-1, 0))
                     ]
    exp_attacks = exp_attacks_0

    plans = get_battle_plans(board, size=1, enemy_attacks=[])

    tc = unittest.TestCase()
    plan0 = plans[0]
    attacks = plan0.get_executed_orders()
    tc.maxDiff = None
    tc.assertCountEqual(exp_attacks, attacks)

    tc.assertEqual(exp_score, plan0.get_score())


def test_solver_get_best_battle_plans_three_combat_mech_cooperation():
    board = Board()

    mech0 = CombatMech()
    mech0_pos = (0, 1)

    mech1 = CombatMech()
    mech1_pos = (1, 1)

    mech2 = CombatMech()
    mech2_pos = (7, 0)

    vek0 = AlphaFirefly()
    vek0_pos = (1, 0)

    board[mech0_pos].set_object(mech0)
    board[mech1_pos].set_object(mech1)
    board[mech2_pos].set_object(mech2)
    board[vek0_pos].set_object(vek0)

    exp_score = 600

    exp_attacks_0 = [Attack(attacker=mech0.get_id(), weapon=Move(), vector=(0, 0)),
                     Attack(attacker=mech0.get_id(), weapon=TitanFist(), vector=(1, 0)),
                     Attack(attacker=mech1.get_id(), weapon=Move(), vector=(1, 0)),
                     Attack(attacker=mech1.get_id(), weapon=TitanFist(), vector=(1, 0)),
                     Attack(attacker=mech2.get_id(), weapon=Move(), vector=(4, 0)),
                     Attack(attacker=mech2.get_id(), weapon=TitanFist(), vector=(-1, 0))
                     ]
    exp_attacks = exp_attacks_0

    plans = get_battle_plans(board, size=1, enemy_attacks=[])

    tc = unittest.TestCase()
    plan0 = plans[0]
    attacks = plan0.get_executed_orders()
    tc.assertCountEqual(exp_attacks, attacks)

    tc.assertEqual(exp_score, plan0.get_score())
