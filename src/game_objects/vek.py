from src.game_objects.object import Object


class Vek(Object):
    def __init__(self, health, weapons, moves):
        Object.__init__(self=self, health=health,
                        weapons=weapons, moves=moves)


class Beetle(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=4, weapons=[],
                     moves=2)


class AlphaBeetle(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=5, weapons=[],
                     moves=2)


class Blobber(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=2)


class AlphaBlobber(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=4)


class Burrower(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=4)


class AlphaBurrower(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=5, weapons=[],
                     moves=4)


class Centipede(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=2)


class AlphaCentipede(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=5)


class Crab(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=3)


class AlphaCrab(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=5, weapons=[],
                     moves=3)


class Digger(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=3)


class AlphaDigger(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=4, weapons=[],
                     moves=3)


class Firefly(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=2)


class AlphaFirefly(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=5, weapons=[],
                     moves=5)


class Hornet(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=5)

    def is_flying(self):
        return True


class AlphaHornet(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=4, weapons=[],
                     moves=5)

    def is_flying(self):
        return True


class Leaper(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=1, weapons=[],
                     moves=4)


class AlphaLeaper(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=4)


class Scarab(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=3)


class AlphaScarab(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=4, weapons=[],
                     moves=3)


class Scorpion(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=3, weapons=[],
                     moves=3)


class AlphaScorpion(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=5, weapons=[],
                     moves=3)


class Spider(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=2)


class AlphaSpider(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=4, weapons=[],
                     moves=2)


class Spiderling(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=1, weapons=[],
                     moves=4)


class BlastPsion(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=2)


class BloodPsion(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=2)


class PsionTyrant(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=2)


class SoldierPsion(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=2)


class ShellPsion(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=2, weapons=[],
                     moves=2)


class Emerged(Vek):
    """Dummy vek, used to calculate points"""
    def __init__(self):
        Vek.__init__(self=self, health=1, weapons=[], moves=0)


class FireflyLeader(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=6, weapons=[], moves=3)

    def is_massive(self):
        return True


class PsionAbomination(Vek):
    def __init__(self):
        Vek.__init__(self=self, health=5, weapons=[], moves=3)

    def is_flying(self):
        return True
