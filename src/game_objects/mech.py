from src.game_objects.object import Object
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


class Mech(Object):
    def __init__(self, health, weapons, moves):
        Object.__init__(self=self, health=health,
                        weapons=weapons, moves=moves)

    def is_player_controlled(self):
        return True

    def is_massive(self):
        return True


class CombatMech(Mech):
    def __init__(self):
        Mech.__init__(self=self, health=3, weapons=[TitanFist(), Repair()], moves=3)


class ArtilleryMech(Mech):
    def __init__(self):
        Mech.__init__(self=self, health=2, weapons=[Artemis(), Repair()], moves=3)


class CannonMech(Mech):
    def __init__(self):
        Mech.__init__(self=self, health=3, weapons=[TaurusCannon(), Repair()], moves=3)


class JetMech(Mech):
    def __init__(self):
        Mech.__init__(self=self, health=2, weapons=[AerialBombs(), Repair()],
                      moves=4)

    def is_flying(self):
        return True


