from src.apply_attack.apply_attack import damage_tile
from src.game_objects.mech import Mech
from src.game_objects.supply_train import SupplyTrainWreck
from src.game_objects.tiles.tile import GroundTile, TimePodTile
from src.game_objects.vek import BlastPsion, PsionAbomination, ShellPsion, Vek, Psion, BloodPsion, SoldierPsion, \
    PsionTyrant, Emerged


class Board:
    """Board where game tiles are placed"""
    BOARD_X_SIZE = 8
    BOARD_Y_SIZE = 8

    def __init__(self):
        """Initializes board with empty tiles"""
        self._tiles = [[GroundTile(_object=None)
                       for _ in range(self.BOARD_X_SIZE)]
                       for _ in range(self.BOARD_Y_SIZE)]

        self._is_time_pod_destroyed = False
        self._is_time_pod_picked_up = False
        self._object_position_cache = {}

    def apply_web(self, from_pos, to_pos):
        direction = (to_pos[0] - from_pos[0], to_pos[1] - from_pos[1])
        self[from_pos].get_object().set_web_direction(direction)

    def clear_web(self, to_pos):
        self[to_pos].get_object().clear_web_direction()

    def is_position_webbed(self, pos):
        for vector in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            potential_webber_pos = (pos[0] + vector[0], pos[1] + vector[1])
            if not self.in_bounds(potential_webber_pos):
                continue
            potential_webber = self[potential_webber_pos].get_object()
            if potential_webber is None:
                continue

            web_direction = potential_webber.get_web_direction()
            if web_direction is None:
                continue

            web_end = (potential_webber_pos[0] + web_direction[0], potential_webber_pos[1] + web_direction[1])
            if web_end == pos:
                return True

        return False

    def fill_object_position_cache(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None:
                    self._object_position_cache[obj.get_id()] = (x, y)

    def get_object_position_cache(self):
        return self._object_position_cache

    def remove_from_object_position_cache(self, _id):
        del(self._object_position_cache[_id])

    def modify_object_position_cache(self, k, v):
        self._object_position_cache[k] = v

    def restore_tiles(self, tiles):
        for position, tile in tiles.items():
            # Cleanup any emerged left-overs
            obj = self[position].get_object()
            if isinstance(obj, Emerged):
                self.remove_from_object_position_cache(obj.get_id())
            if isinstance(obj, SupplyTrainWreck):
                self.remove_from_object_position_cache(obj.get_id())
            if isinstance(tile, TimePodTile):
                self.clear_time_pod_destroyed()
                self.clear_time_pod_picked_up()

            obj = tile.get_object()
            if obj is not None:
                self.modify_object_position_cache(obj.get_id(), position)

            self[position] = tile

    def regular_damage(self, pos, damage):
        tile = self[pos]
        obj = tile.get_object()
        damage_tile(self, pos, tile, obj)
        if obj is not None:
            if isinstance(obj, Vek) and self.is_shell_psion_present() and not isinstance(obj, Psion):
                damage -= 1

            self[pos].regular_damage(damage)

    # TODO: In the long run, those function will take a lot time to process.
    # Consider having a some sort of cache to store information if psion is present.
    # Something similar in function restore_tiles and how time pods are restored
    def is_blast_psion_present(self):
        for _, v in self._object_position_cache.items():
            if isinstance(self[v].get_object(), (BlastPsion, PsionAbomination)):
                return True

        return False

    def is_blood_psion_present(self):
        for _, v in self._object_position_cache.items():
            if isinstance(self[v].get_object(), (BloodPsion, PsionAbomination)):
                return True

        return False

    def is_psion_tyrant_present(self):
        for _, v in self._object_position_cache.items():
            if isinstance(self[v].get_object(), PsionTyrant):
                return True

        return False

    def is_soldier_psion_present(self):
        for _, v in self._object_position_cache.items():
            if isinstance(self[v].get_object(), (SoldierPsion, PsionAbomination)):
                return True

        return False

    def is_shell_psion_present(self):
        for _, v in self._object_position_cache.items():
            if isinstance(self[v].get_object(), ShellPsion):
                return True

        return False

    def in_bounds(self, pos):
        if not (0 <= pos[0] < self.BOARD_X_SIZE) or not (0 <= pos[1] < self.BOARD_Y_SIZE):
            return False

        return True

    def find_object_position(self, _object):
        _id = _object.get_id()
        return self.find_object_id_position(_id)

    def find_object_id_position(self, _id):
        return None if _id not in self._object_position_cache else self._object_position_cache[_id]

    def find_player_objects(self):
        player_controlled_objects = []
        for _, v in self._object_position_cache.items():
            if isinstance(self[v].get_object(), Mech):
                player_controlled_objects.append(v)

        return player_controlled_objects

    def set_time_pod_destroyed(self):
        self._is_time_pod_destroyed = True

    def set_time_pod_picked_up(self):
        self._is_time_pod_picked_up = True

    def clear_time_pod_destroyed(self):
        self._is_time_pod_destroyed = False

    def clear_time_pod_picked_up(self):
        self._is_time_pod_picked_up = False

    def is_time_pod_destroyed(self):
        return self._is_time_pod_destroyed

    def is_time_pod_picked_up(self):
        return self._is_time_pod_picked_up

    def __getitem__(self, key):
        return self._tiles[key[0]][key[1]]

    def __setitem__(self, key, val):
        self._tiles[key[0]][key[1]] = val

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)
