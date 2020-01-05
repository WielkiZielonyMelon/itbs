from src.apply_attack.apply_attack import damage_tile
from src.game_objects.tiles.tile import GroundTile, TimePodTile
from src.game_objects.vek import BlastPsion, PsionAbomination, ShellPsion, Vek, Psion, BloodPsion, SoldierPsion, \
    PsionTyrant


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

    def restore_tiles(self, tiles):
        for position, tile in tiles.items():
            if isinstance(tile, TimePodTile):
                self.clear_time_pod_destroyed()
                self.clear_time_pod_picked_up()

            self[position] = tile

    def regular_damage(self, pos, damage):
        damage_tile(self, pos)
        obj = self[pos].get_object()
        if obj is not None:
            if self.is_shell_psion_present() and isinstance(obj, Vek) and not isinstance(obj, Psion):
                damage -= 1

            self[pos].regular_damage(damage)

    # TODO: In the long run, those function will take a lot time to process.
    # Consider having a some sort of cache to store information if psion is present.
    # Something similar in function restore_tiles and how time pods are restored
    def is_blast_psion_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, (BlastPsion, PsionAbomination)):
                    return True

        return False

    def is_blood_psion_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, (BloodPsion, PsionAbomination)):
                    return True

        return False

    def is_psion_tyrant_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, PsionTyrant):
                    return True

        return False

    def is_soldier_psion_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, (SoldierPsion, PsionAbomination)):
                    return True

        return False

    def is_shell_psion_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, ShellPsion):
                    return True

        return False

    def in_bounds(self, pos):
        if pos[0] < 0:
            return False
        if pos[0] >= self.BOARD_X_SIZE:
            return False
        if pos[1] < 0:
            return False
        if pos[1] >= self.BOARD_Y_SIZE:
            return False

        return True

    def find_object_position(self, _object):
        _id = _object.get_id()
        return self.find_object_id_position(_id)

    def find_object_id_position(self, _id):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and _id == obj.get_id():
                    return x, y

        return None

    def find_player_objects(self):
        player_controlled_objects = []
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and obj.is_player_controlled():
                    player_controlled_objects.append((x, y))

        return player_controlled_objects

    def set_time_pod_destroyed(self):
        self._is_time_pod_destroyed = True

    def set_time_pod_picked_up(self):
        self._is_time_pod_picked_up = True

    def clear_time_pod_destroyed(self):
        self._is_time_pod_destroyed = False

    def clear_time_pod_picked_up(self):
        self._is_time_pod_picked_up = False

    def is_time_pod_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                if isinstance(self[(x, y)], TimePodTile):
                    return True

        return False

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
