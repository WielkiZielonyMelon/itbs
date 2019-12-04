from src.game_objects.object import Object


class Building(Object):
    """In game building representation.

    Building ranges from civilian building, factories, bars,
    clinics, coal plants. It does not include terraformers"""

    def __init__(self, health):
        Object.__init__(self=self, health=health,
                        weapons=[], moves=0)

    def is_pushable(self):
        return False

    def fire_damage(self):
        # Buildings do not get damaged by fire
        pass


class CivilianBuilding(Building):
    def __init__(self, health):
        Building.__init__(self=self, health=health)


class SpecialBuilding(Building):
    def __init__(self, health):
        Building.__init__(self=self, health=health)


class PowerGenerator(SpecialBuilding):
    def __init__(self):
        SpecialBuilding.__init__(self=self, health=1)
