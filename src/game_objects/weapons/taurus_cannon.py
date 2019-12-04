from src.game_objects.weapons.weapon import Weapon


class TaurusCannon(Weapon):
    def __init__(self, damage_plus_1_upgrade_1=False, damage_plus_1_upgrade_2=False):
        self._base_damage = 2
        self._damage_plus_1_upgrade_1 = damage_plus_1_upgrade_1
        self._damage_plus_1_upgrade_2 = damage_plus_1_upgrade_2
        Weapon.__init__(self=self)

    def get_base_damage(self):
        return self._base_damage

    def get_total_damage(self):
        total_damage = self.get_base_damage()
        if self.has_damage_plus_1_upgrade_1():
            total_damage += 1
        if self.has_damage_plus_1_upgrade_2():
            total_damage += 1

        return total_damage

    def has_damage_plus_1_upgrade_1(self):
        return self._damage_plus_1_upgrade_1

    def has_damage_plus_1_upgrade_2(self):
        return self._damage_plus_1_upgrade_2

    def __repr__(self):
        return "{}(d1={} d2={})".format(type(self).__name__,
                                        self.has_damage_plus_1_upgrade_1(), self.has_damage_plus_1_upgrade_2())
