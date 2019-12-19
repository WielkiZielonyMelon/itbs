from src.game_objects.weapons.weapon import Weapon


class Stinger(Weapon):
    def __init__(self):
        Weapon.__init__(self=self)

    def get_total_damage(self):
        return 1


class LaunchingStinger(Weapon):
    def __init__(self):
        Weapon.__init__(self=self)

    def get_total_damage(self):
        return 2


class SuperStinger(Weapon):
    def __init__(self):
        Weapon.__init__(self=self)

    def get_total_damage(self):
        return 2
