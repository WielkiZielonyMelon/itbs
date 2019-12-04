import copy
from queue import Queue


class Order:
    """Order for a given object

    It tells an object to either move or attack but does not specify
    where an object should move or what attack it should do.
    """
    MOVE = 0
    ATTACK = 1

    def __init__(self, _object, _type):
        self._object = _object
        self._type = _type

    def get_object(self):
        return self._object

    def get_type(self):
        return self._type

    def get_type_str(self):
        t = self.get_type()
        if t is Order.MOVE:
            return "Move({})".format(t)
        elif t is Order.ATTACK:
            return "Attack({})".format(t)
        else:
            raise Exception("Unknown order of type {} for object {}"
                            .format(t, self.get_object()))

    def __hash__(self):
        return self.get_type() + 2 * self.get_object().get_id()

    def __repr__(self):
        s = "Order for id({}) is {}"\
            .format(self.get_object().get_id(), self.get_type_str())
        return s

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)


def create_orders(board):
    """Return list of orders for player controlled objects

    Arguments:
        board - Board - gameplay arena

    Returns:
        List of all possible orders for player controlled objects
    """
    orders = []
    player_objects = board.find_player_objects()
    if len(player_objects) <= 0:
        return orders

    from src.solver.actions_left import ActionsLeft
    actions_left = [ActionsLeft(_object=board[pos].get_object()) for pos in player_objects]

    q = Queue()
    current_orders = []
    q.put((current_orders, actions_left))

    counter = 0
    while q.empty() is not True:
        counter += 1
        it = q.get()
        current_orders = it[0]
        actions_left = it[1]

        for i in range(0, len(actions_left)):
            action_left = actions_left[i]
            if action_left.has_move():
                new_actions_left = copy.deepcopy(actions_left)
                new_order = new_actions_left[i].order_move()
                q.put((current_orders + [new_order], new_actions_left))
            if action_left.has_attack():
                new_actions_left = copy.deepcopy(actions_left)
                new_order = new_actions_left[i].order_attack()
                del new_actions_left[i]
                if len(new_actions_left) <= 0:
                    orders.append(current_orders + [new_order])
                    continue
                else:
                    q.put((current_orders + [new_order], new_actions_left))

    return orders
