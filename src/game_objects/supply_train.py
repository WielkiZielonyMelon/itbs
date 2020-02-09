from src.game_objects.object import Object


class SupplyTrainHead(Object):
    def __init__(self):
        Object.__init__(self=self, health=1,
                        weapons=[], moves=0)

    def is_pushable(self):
        return False

    def fire_damage(self):
        pass


class SupplyTrainTail(Object):
    def __init__(self):
        Object.__init__(self=self, health=1,
                        weapons=[], moves=0)

    def is_pushable(self):
        return False

    def fire_damage(self):
        pass


class SupplyTrainWreck(Object):
    def __init__(self):
        Object.__init__(self=self, health=1,
                        weapons=[], moves=0)

    def is_pushable(self):
        return False

    def fire_damage(self):
        pass

