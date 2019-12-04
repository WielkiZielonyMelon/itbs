class Attack:
    """Defines attack that associated object wants to do"""
    def __init__(self, attacker, weapon, vector=None):
        """Standard initialization

        Arguments:
            _object - Object() or (int, int) - id of attacker or position to perform attack
            weapon - Weapon() - weapon that object wants to use
            vector - (int, int) - vector of the attack
        """
        self._attacker = attacker
        self._weapon = weapon
        self._vector = vector

    def get_attacker(self):
        return self._attacker

    def get_weapon(self):
        return self._weapon

    def get_vector(self):
        return self._vector

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        s = "Attack(attacker={}, weapon={}, vector={})" \
            .format(str(self.get_attacker()), str(self.get_weapon()), str(self.get_vector()))
        return s

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Attack):
            return False

        if self.get_attacker() != other.get_attacker():
            return False

        if self.get_weapon() != other.get_weapon():
            return False

        if self.get_vector() != other.get_vector():
            return False

        return True
