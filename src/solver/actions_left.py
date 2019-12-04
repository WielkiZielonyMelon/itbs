from src.solver.order import Order


class ActionsLeft:
    """Define actions left for a given object"""
    def __init__(self, _object):
        self._object = _object
        self._move = True
        self._attack = True

    def clear_attack(self):
        self._attack = False

    def clear_move(self):
        self._move = False

    def has_attack(self):
        return self._attack

    def has_move(self):
        return self._move

    def get_object(self):
        return self._object

    def order_attack(self):
        if self._attack is False:
            raise Exception("Cannot get attack as an action")

        self.clear_move()
        self.clear_attack()
        return Order(_object=self.get_object(), _type=Order.ATTACK)

    def order_move(self):
        if self._move is False:
            raise Exception("Cannot get move as an action")

        self.clear_move()
        return Order(_object=self.get_object(), _type=Order.MOVE)

    def __repr__(self):
        s = "ActionsLeft " + str(self.get_object().get_id())
        s += "\nhas_move " + str(self.has_move()) + "\nhas_attack " + \
             str(self.has_attack())

        return s