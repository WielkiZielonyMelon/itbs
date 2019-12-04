from src.game_objects.weapons.weapon import Weapon


class AerialBombs(Weapon):
    def __init__(self, damage_plus_1=False, range_plus_1=False):
        self._base_damage = 1
        self._base_range = 2
        self._damage_plus_1 = damage_plus_1
        self._range_plus_1 = range_plus_1
        Weapon.__init__(self=self)

    def get_base_damage(self):
        return self._base_damage

    def get_total_damage(self):
        total_damage = self.get_base_damage()
        if self.has_damage_plus_1():
            total_damage += 1
        return total_damage

    def has_damage_plus_1(self):
        return self._damage_plus_1

    def get_base_range(self):
        return self._base_range

    def get_full_range(self):
        r = [self.get_base_range()]
        if self.has_range_plus_1():
            r.append(self.get_base_range() + 1)
        return r

    def has_range_plus_1(self):
        return self._range_plus_1
