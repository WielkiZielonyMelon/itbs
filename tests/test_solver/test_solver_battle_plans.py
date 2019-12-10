import unittest

from src.solver.battle_plans import BattlePlans, Plan


def test_battle_plans():
    plan0 = Plan(score=950, executed_orders=[])
    plan1 = Plan(score=800, executed_orders=[])
    plan2 = Plan(score=1600, executed_orders=[])
    plan3 = Plan(score=1200, executed_orders=[])
    plan4 = Plan(score=900, executed_orders=[])
    plan5 = Plan(score=1000, executed_orders=[])

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
