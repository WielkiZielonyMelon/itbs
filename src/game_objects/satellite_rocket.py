from src.game_objects.object import Object


class SatelliteRocket(Object):
    """In game satellite rocket representation."""

    def __init__(self):
        Object.__init__(self=self, health=2,
                        weapons=[], moves=0)

    def is_pushable(self):
        return False
