from src.game_objects.weapons.weapon import Weapon


class Artemis(Weapon):
    def __init__(self, buildings_immune=False, damage_plus_2=False):
        self._base_damage = 1
        self._buildings_immune = buildings_immune
        self._damage_plus_2 = damage_plus_2
        Weapon.__init__(self=self)

    def get_base_damage(self):
        return self._base_damage

    def get_total_damage(self):
        total_damage = self.get_base_damage()
        if self.has_damage_plus_2():
            total_damage += 2
        return total_damage

    def has_damage_plus_2(self):
        return self._damage_plus_2

    def has_buildings_immune(self):
        return self._buildings_immune

    def __repr__(self):
        return "{}(d={} bi={})".format(type(self).__name__, self.has_damage_plus_2(), self.has_buildings_immune())
