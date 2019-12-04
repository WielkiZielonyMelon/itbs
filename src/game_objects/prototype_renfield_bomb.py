from src.game_objects.object import Object


class PrototypeRenfieldBomb(Object):
    def __init__(self):
        Object.__init__(self=self, health=1,
                        weapons=[], moves=0)

    def is_exploding(self):
        return True

