from src.game_objects.weapons.weapon import Weapon


class AcceleratingThorax(Weapon):
    def __init__(self):
        Weapon.__init__(self=self)

    def get_total_damage(self):
        return 1


class EnhancedThorax(Weapon):
    def __init__(self):
        Weapon.__init__(self=self)

    def get_total_damage(self):
        return 3
