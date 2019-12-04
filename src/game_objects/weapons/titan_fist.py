from src.game_objects.weapons.weapon import Weapon


class TitanFist(Weapon):
    def __init__(self, dash=False, damage_plus_2=False):
        self._base_damage = 2
        self._dash = dash
        self._damage_plus_2 = damage_plus_2
        Weapon.__init__(self=self)

    def get_base_damage(self):
        return self._base_damage

    def get_total_damage(self):
        total_damage = self.get_base_damage()
        if self.has_damage_plus_2():
            total_damage += 2
        return total_damage

    def has_dash(self):
        return self._dash

    def has_damage_plus_2(self):
        return self._damage_plus_2

    def __repr__(self):
        return "{}(dh={} dm={})".format(type(self).__name__, self.has_dash(), self.has_damage_plus_2())
