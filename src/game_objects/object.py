import copy
import itertools


class Object:
    """Representation of game object.

    Objects can be anything, ranging from buildings, rocks, mountains,
    vek, mechs or power pylons. Most of the time it is something that
    can be damaged"""
    id_iter = itertools.count()

    def __init__(self, health, weapons, moves):
        self._id = next(Object.id_iter)
        self._max_health = health
        self._health = health
        self._weapons = weapons
        self._moves = moves
        self._on_fire = False
        self._on_acid = False
        self._is_frozen = False
        self._is_shielded = False
        self._web_directions = []

    def clear_web_direction(self, direction):
        self._web_directions.remove(direction)

    def clear_web_directions(self):
        self._web_directions = []

    def add_web_direction(self, direction):
        self._web_directions.append(direction)

    def get_web_directions(self):
        return self._web_directions

    def get_id(self):
        return self._id

    def get_max_health(self):
        return self._max_health

    def get_health(self):
        return self._health

    def get_weapons(self):
        return self._weapons

    def get_moves(self):
        return self._moves

    def is_on_fire(self):
        return self._on_fire

    def set_fire(self):
        self._on_fire = True

    def clear_fire(self):
        self._on_fire = False

    def is_on_acid(self):
        return self._on_acid

    def set_acid(self):
        self._on_acid = True

    def clear_acid(self):
        self._on_acid = False

    def is_frozen(self):
        return self._is_frozen

    def freeze(self):
        self._is_frozen = True
        self.clear_fire()

    def thaw(self):
        self._is_frozen = False

    def is_shielded(self):
        return self._is_shielded

    def set_shield(self):
        self._is_shielded = True

    def clear_shield(self):
        self._is_shielded = False

    def is_player_controlled(self):
        return False

    def is_massive(self):
        return False

    def is_pushable(self):
        return True

    def is_flying(self):
        return False

    def is_exploding(self):
        return False

    def repair(self):
        if self.get_health() < self.get_max_health():
            self._health += 1

        self.clear_acid()
        self.clear_fire()
        self.thaw()
        
    def fire_damage(self):
        self._health -= 1
        if self._health <= 0:
            self._health = 0

    def emerge_damage(self):
        if self.is_shielded():
            self.clear_shield()
            return

        self._health -= 1
        if self._health <= 0:
            self._health = 0

    def bump_damage(self, val):
        self._health -= val
        if self._health <= 0:
            self._health = 0

    def regular_damage(self, val):
        if self.is_on_acid() is True:
            self._health -= 2 * val
        else:
            self._health -= val

        if self._health < 0:
            self._health = 0

    def __hash__(self):
        return self.get_id()

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)

    def get_flags_str(self):
        return "id={} mh={} h={} w={} m={} fi={} a={} fr={} pc={} m={} ph={} fl={} e={}" \
            .format(self.get_id(), self.get_max_health(), self.get_health(), self.get_weapons(), self.get_moves(),
                    self.is_on_fire(), self.is_on_acid(), self.is_frozen(), self.is_player_controlled(),
                    self.is_massive(), self.is_pushable(), self.is_flying(), self.is_exploding())

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.get_flags_str())

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        for k, v in self.__dict__.items():
            setattr(result, k, copy.copy(v))

        return result
