from src.game_objects.object import Object


class Mountain(Object):
    def __init__(self):
        Object.__init__(self=self, health=2,
                        weapons=[], moves=0)

    def is_pushable(self):
        return False

    def regular_damage(self, val):
        """Mountains can get their health decreased only by one"""
        self._health -= 1
