import unittest

from src.game_objects.board import Board
from src.solver.battle_plans import BattlePlans, Plan


def test_battle_plans():
    board = Board()
    plan0 = Plan(score=950, executed_orders=[], orders_left=None)
    plan1 = Plan(score=800, executed_orders=[], orders_left=None)
    plan2 = Plan(score=1600, executed_orders=[], orders_left=None)
    plan3 = Plan(score=1200, executed_orders=[], orders_left=None)
    plan4 = Plan(score=900, executed_orders=[], orders_left=None)
    plan5 = Plan(score=1000, executed_orders=[], orders_left=None)

    battle_plans = BattlePlans(size=3, board=None)
    battle_plans.add_plan(plan0)
    battle_plans.add_plan(plan1)
    battle_plans.add_plan(plan2)
    battle_plans.add_plan(plan3)
    battle_plans.add_plan(plan4)
    battle_plans.add_plan(plan5)

    ret_plans = battle_plans.get_plans()
    exp_plans = [plan2, plan3, plan5]

    unittest.TestCase().assertCountEqual(ret_plans, exp_plans)
