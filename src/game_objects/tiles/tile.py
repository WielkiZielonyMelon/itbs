import copy


class Tile:

    def __init__(self, _object, smoke=False):
        self._object = _object
        self._smoke = smoke

    def has_smoke(self):
        return self._smoke

    def clear_smoke(self):
        self._smoke = False

    def set_smoke(self):
        self._smoke = True

    def is_liquid(self):
        return False

    def emerge_damage(self, val):
        obj = self.get_object()
        if obj is not None:
            obj.emerge_damage()

    def freeze(self):
        obj = self.get_object()
        if obj is not None:
            obj.freeze()

    def bump_damage(self, val):
        obj = self.get_object()
        if obj is not None:
            obj.bump_damage(val)

    def fire_damage(self):
        obj = self.get_object()
        if obj is not None:
            obj.fire_damage()

    def set_fire(self):
        obj = self.get_object()
        if obj is not None:
            obj.set_fire()

    def repair(self):
        obj = self.get_object()
        if obj is not None:
            obj.repair()

    def set_acid(self):
        obj = self.get_object()
        if obj is not None:
            obj.set_acid()

    def regular_damage(self, val):
        obj = self.get_object()
        if obj is None:
            return
        if obj.is_shielded():
            obj.clear_shield()
        else:
            obj.regular_damage(val)

    def get_object(self):
        return self._object

    def set_object(self, obj):
        self._object = obj

    def has_object(self):
        return self._object is not None

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        for k, v in self.__dict__.items():
            setattr(result, k, copy.copy(v))
        return result


class AcidPool(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def repair(self):
        raise Exception("Repairing AcidPool not possible. Convert to " +
                        "GroundTile and then repair object")


class AcidTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def is_liquid(self):
        return True

    def freeze(self):
        raise Exception("Cannot freeze AcidTile. Convert to FrozenAcidTile " +
                        "and then freeze object")

    def set_fire(self):
        obj = self.get_object()
        if obj is None:
            return

        if obj.is_flying():
            obj.set_fire()


class FrozenAcidTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def set_fire(self):
        raise Exception("Cannot set fire on FrozenAcidTile. Set object on " +
                        "fire and convert tile to AcidTile")


class DamagedFrozenAcidTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def freeze(self):
        raise Exception("Cannot freeze DamagedFrozenAcidTile. Convert to " +
                        "FrozenAcidTile and then freeze object")

    def set_fire(self):
        raise Exception("Cannot set fire on DamagedFrozenAcidTile. Set " +
                        "object on fire and convert tile to AcidTile")


class ChasmTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)


class FireTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def freeze(self):
        raise Exception("Cannot freeze FireTile. Convert to GroundTile and " +
                        "then freeze object")

    def repair(self):
        raise Exception("Repairing FireTile not possible. Repair any object on " +
                        "FireTile and convert tile to GroundTile")


class ForestTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def set_fire(self):
        raise Exception("Cannot set fire on ForestTile. Set object on fire " +
                        "and convert tile to ForestFireTile")


class ForestFireTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def freeze(self):
        raise Exception("Cannot freeze ForestFireTile. Convert to ForestTile " +
                        "and then freeze object")

    def repair(self):
        raise Exception("Repairing ForestFireTile not possible. Convert to " +
                        "ForestTile first and then repair object")


class GroundTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def set_fire(self):
        raise Exception("Cannot set fire on GroundTile. Set object on fire " +
                        "and convert tile to FireTile")


class LavaTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def is_liquid(self):
        return True

    def freeze(self):
        raise Exception("Cannot freeze LavaTile. Convert to FrozenLavaTile " +
                        "and then freeze object")


class FrozenLavaTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def set_fire(self):
        raise Exception("Cannot set fire on FrozenLavaTile. Set object on " +
                        "fire and convert tile to LavaTile")


class DamagedFrozenLavaTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def freeze(self):
        raise Exception("Cannot freeze DamagedFrozenLavaTile. Convert to " +
                        "FrozenLavaTile and then freeze object")

    def set_fire(self):
        raise Exception("Cannot set fire on DamagedFrozenLavaTile. Set " +
                        "object on fire and convert tile to LavaTile")


class SandTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def regular_damage(self, val):
        raise Exception("Not possible to damage SandTile. Convert to " +
                        "SmokeTile and then apply damage")


class SmokeTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)


class IceTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)


class DamagedIceTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)


class WaterTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)

    def is_liquid(self):
        return True

    def freeze(self):
        raise Exception("Cannot freeze WaterTile. Convert to IceTile and then " +
                        "freeze object")


class TimePodTile(Tile):
    def __init__(self, _object):
        Tile.__init__(self=self, _object=_object)
