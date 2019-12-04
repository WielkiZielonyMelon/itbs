import copy
from heapq import heappop, heappush, heapreplace
from queue import Queue

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.weapons.move import Move
from src.helpers.get_possible_attacks import get_possible_attacks
from src.helpers.get_possible_moves import get_possible_moves
from src.helpers.get_score_of_board import get_score_of_board
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present
from src.solver.order import Order, create_orders


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
    def __init__(self, score, executed_orders, orders_left):
        self._executed_orders = copy.copy(executed_orders)
        self._score = score
        self._orders_left = orders_left

    def add_order(self, activity):
        self._executed_orders.append(activity)

    def get_score(self):
        return self._score

    def get_executed_orders(self):
        return self._executed_orders

    def has_orders_left(self):
        return len(self.get_orders_left()) > 0

    def pop_first_order(self):
        order = self.get_orders_left()[0]
        self._orders_left = self._orders_left[1:]
        return order

    def get_orders_left(self):
        return self._orders_left

    def __hash__(self):
        # Do not care about the activities, score is the most important
        return hash(self.get_score())

    def __lt__(self, other):
        if self.get_score() < other.get_score():
            return True
        return False

    def __repr__(self):
        s = "Plan score " + str(self.get_score()) + " "
        s += "activities " + str(self.get_executed_orders()) + " "
        s += "orders left " + str(self.get_orders_left())

        return s

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)


def get_battle_plans(board, size, enemy_attacks):
    # Initialize empty battle plans, with board as a reference
    battle_plans = BattlePlans(size=size, board=board)

    # Create empty queue
    q = Queue()

    # Grab the score
    score = get_score_of_board(board)

    # Grab orders left
    orders_left = create_orders(board)

    # This might happen if there are no player objects
    if len(orders_left) <= 0:
        return battle_plans

    # And fill it with all possible orders that can be executed
    for orders in orders_left:
        # Create a plan with no orders executed yet and
        new_plan = Plan(score=score, executed_orders=[], orders_left=orders)

        # Finally put the plan to queue so it will be executed later
        # if it has orders left that is
        q.put(new_plan)

    counter = [0, 0, 0, 0, 0, 0, 0]
    total_branches = [0, 0, 0, 0, 0, 0, 0]
    loop_counter = 0
    cut_in_moves = [0, 0, 0, 0, 0, 0, 0]
    # TODO: This should be a class
    movement_sets = set()

    while q.empty() is not True:
        loop_counter += 1
        # Retrieve plan, that has some orders already executed and some orders to do
        plan = q.get()

        # Check next order to be executed, either MOVE or ATTACK
        # This also removes the order from the orders_left list
        next_order = plan.pop_first_order()

        # Get a list of orders executed yet
        orders_executed = plan.get_executed_orders()

        # Dictionary that will restore original board
        undo_tiles = {}

        # Execute orders to get latest board state
        for order in orders_executed:
            update_dict_if_key_not_present(undo_tiles, apply_attack(board, order))

        # For what object is this order for?
        obj = next_order.get_object()

        # Board is updated, check next order
        if next_order.get_type() is Order.MOVE:
            # As the next order is move, get all possible moves
            moves = get_possible_moves(board, obj)
            # Convert those moves to attacks
            attacks = []
            for move in moves:
                # Create a new order to be executed...
                attacks.append(Attack(attacker=obj.get_id(), weapon=Move(), vector=move))

        elif next_order.get_type() is Order.ATTACK:
            # Attack time! Get all possible attacks
            attacks = get_possible_attacks(board, obj)
        else:
            raise Exception("Unknown order {}".format(next_order))

        for attack in attacks:
            total_branches[len(orders_executed) + 1] += 1
            # Before applying enemy attack, check if it was a move. If it was a move and also last executed order
            # was a move, check if we have something like this before. If so, terminate
            if isinstance(attack.get_weapon(), Move) and len(orders_executed) > 0 and \
                    isinstance(orders_executed[-1].get_weapon(), Move):
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
                moves_update = (tuple(before_moves, ), frozenset(latest_moves), tuple(plan.get_orders_left()))
                if moves_update in movement_sets:
                    cut_in_moves[len(orders_executed) + 1] += 1
                    continue
                movement_sets.add(moves_update)

            # Apply new attack!
            latest_order = apply_attack(board, attack)
            if not latest_order:
                # Nothing actually happened, cut this branch
                counter[len(orders_executed) + 1] += 1
                continue

            # Apply enemy attacks!
            for enemy_attack in enemy_attacks:
                update_dict_if_key_not_present(latest_order, apply_attack(board, enemy_attack))

            # ... now grab the score
            score = get_score_of_board(board)

            # Create a new plan,, with new score and orders left
            new_plan = Plan(score=score, executed_orders=plan.get_executed_orders(),
                            orders_left=plan.get_orders_left())
            # We still have to add information that order was executed
            new_plan.add_order(attack)
            # Add to the battle plans
            battle_plans.add_plan(new_plan)

            # Rewind latest orders
            for position, tile in latest_order.items():
                board[position] = tile

            latest_order.clear()

            # Add to queue if there are any orders left
            if new_plan.has_orders_left():
                q.put(new_plan)

        # And rewind original attacks
        for position, tile in undo_tiles.items():
            board[position] = tile

    print("")
    print("Total branches {}".format(total_branches))
    print("Terminated branches {}".format(counter))
    print("Cut in moves {}".format(cut_in_moves))
    print("Total loops {}".format(loop_counter))
    return battle_plans.get_plans()
