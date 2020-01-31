import copy
from heapq import heappop, heappush, heapreplace

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.weapons.move import Move
from src.helpers.apply_environment import apply_environment
from src.helpers.get_possible_attacks import get_possible_attacks
from src.helpers.get_possible_moves import get_possible_moves
from src.helpers.get_score_of_board import get_score_of_board
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


class BattlePlans:
    def __init__(self, size, board):
        self._size = size
        self._plans = []
        self._board = board

    def get_size(self):
        return self._size

    def get_board(self):
        return self._board

    def add_plan(self, plan):
        if len(self._plans) < self.get_size():
            heappush(self._plans, plan)
        elif self._plans[0].get_score() < plan.get_score():
            heapreplace(self._plans, plan)

    def get_plans(self):
        plans = []
        while len(self._plans) > 0:
            plans.append(heappop(self._plans))

        return plans


class Plan:
    def __init__(self, score, executed_orders):
        self._executed_orders = copy.copy(executed_orders)
        self._score = score

    def add_order(self, activity):
        self._executed_orders.append(activity)

    def get_score(self):
        return self._score

    def get_executed_orders(self):
        return self._executed_orders

    def __hash__(self):
        # Do not care about the activities, score is the most important
        return hash(self.get_score())

    def __lt__(self, other):
        if self.get_score() < other.get_score():
            return True
        return False

    def __repr__(self):
        return "Plan score {} activities {}".format(self.get_score(), self.get_executed_orders())

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)


class LatestMovesCache:
    """Stores executed attacks/moves with future orders."""
    PRESENT = 0
    ADDED = 1
    DOES_NOT_QUALIFY = 2

    def __init__(self):
        self.movement_sets = set()

    def add(self, orders_executed, attack):
        if not (isinstance(attack.get_weapon(), Move) and len(orders_executed) > 0 and
                isinstance(orders_executed[-1].get_weapon(), Move)):
            return self.DOES_NOT_QUALIFY

        # Get all latest Move executed orders
        latest_moves = []
        before_moves = []
        for p in range(len(orders_executed) - 1, -1, -1):
            if isinstance(orders_executed[p], Move):
                latest_moves.append(orders_executed[p])
            else:
                before_moves = orders_executed[0:p]
                break
        latest_moves.append(attack)
        moves_update = (tuple(before_moves, ), frozenset(latest_moves))
        if moves_update in self.movement_sets:
            return self.PRESENT

        self.movement_sets.add(moves_update)
        return self.ADDED


def execute_attack(board, attacks, battle_plans, latest_moves_cache, orders_executed, orders_left, enemy_attacks,
                   attacker_pos):
    for attack in attacks:
        if LatestMovesCache.PRESENT == latest_moves_cache.add(orders_executed, attack):
            continue
        latest_order_undo = apply_attack(board, attack, attacker_pos)
        if not latest_order_undo:
            # Nothing actually happened, cut this branch
            continue

        # Update executed orders
        orders_executed.append(attack)
        # Apply environment effects
        enemy_attacks_undo = {}
        update_dict_if_key_not_present(enemy_attacks_undo, apply_environment(board))
        # Apply enemy attacks!
        for enemy_attack in enemy_attacks:
            update_dict_if_key_not_present(enemy_attacks_undo, apply_attack(board, enemy_attack))
        # ... now grab the score
        score = get_score_of_board(board)
        # Create a new plan,, with new score and orders left
        new_plan = Plan(score=score, executed_orders=orders_executed)

        # Add to the battle plans
        battle_plans.add_plan(new_plan)
        # Unwind enemy and environment destructive activities
        board.restore_tiles(enemy_attacks_undo)
        # Execute any further plans
        fill_battle_plans(board, battle_plans, latest_moves_cache, orders_executed, orders_left, enemy_attacks)
        # Rewind latest orders
        board.restore_tiles(latest_order_undo)

        # Rewind executed order
        orders_executed.pop()

        # Clear undo tiles
        latest_order_undo.clear()


class Order:
    MOVE = 0,
    ATTACK = 1


def fill_battle_plans(board, battle_plans, latest_moves_cache, orders_executed, orders_left, enemy_attacks):
    """Check possible scenarios and find best battle plan

    This function checks all possible scenarios for all player controlled objects."""
    # Iterate over over all possible orders
    for obj_id, orders in orders_left.items():
        pos = board.find_object_id_position(obj_id)
        if pos is None:
            continue
        obj = board[pos].get_object()
        if Order.MOVE in orders:
            new_orders_left = copy.copy(orders_left)
            new_orders_left[obj_id] = [Order.ATTACK]
            moves = get_possible_moves(board, obj)
            attacks = [Attack(attacker=obj_id, weapon=Move(), vector=move)
                       for move in moves]
            execute_attack(board, attacks, battle_plans, latest_moves_cache,
                           orders_executed, new_orders_left, enemy_attacks, pos)

        if Order.ATTACK in orders:
            new_orders_left = copy.copy(orders_left)
            del new_orders_left[obj_id]
            attacks = get_possible_attacks(board, obj)
            execute_attack(board, attacks, battle_plans, latest_moves_cache,
                           orders_executed, new_orders_left, enemy_attacks, pos)


def get_battle_plans(board, size, enemy_attacks):
    # Initialize empty battle plans, with board as a reference
    battle_plans = BattlePlans(size=size, board=board)

    # Find all player objects
    player_objects_pos = board.find_player_objects()

    if len(player_objects_pos) <= 0:
        # No player objects? We can't do anything then...
        return None

    # For player objects, create possible orders
    orders_left = {}
    for pos in player_objects_pos:
        orders_left[board[pos].get_object().get_id()] = [Order.MOVE, Order.ATTACK]

    # Create moves cache to limit possible moves
    latest_moves_cache = LatestMovesCache()
    executed_orders = []

    fill_battle_plans(board, battle_plans, latest_moves_cache, executed_orders, orders_left, enemy_attacks)
    return battle_plans.get_plans()
