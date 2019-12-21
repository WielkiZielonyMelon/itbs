from src.game_objects.tiles.tile import GroundTile, TimePodTile
from src.game_objects.vek import BlastPsion, PsionAbomination, ShellPsion, Vek


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
        obj = self[pos].get_object()
        if obj is not None:
            if self.is_shell_psion_present() and isinstance(obj, Vek):
                damage -= 1

            self[pos].regular_damage(damage)

    def is_shell_psion_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, ShellPsion):
                    return True

        return False

    def is_explosive_psion_present(self):
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, (BlastPsion, PsionAbomination)):
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

    def are_tiles_the_same(self, other):
        """Compare tiles, not objects"""
        for x in range(0, self.BOARD_X_SIZE):
            for y in range(0, self.BOARD_Y_SIZE):
                if type(self) != type(other):
                    return False

        return True

    # TODO: Refactor, this is ugly
    def print_board(self):
        width = 25
        s = ""
        for y in range(0, self.BOARD_Y_SIZE):
            s += "Description".ljust(width)
            for x in range(0, self.BOARD_X_SIZE):
                s += type(self[(x, y)]).__name__.ljust(width)

            s += "\n"
            s += "Smoke".ljust(width)
            for x in range(0, self.BOARD_X_SIZE):
                s += str(self[(x, y)].has_smoke()).ljust(width)

            s += "\n"
            s += "Object".ljust(width)
            for x in range(0, self.BOARD_X_SIZE):
                obj = self[(x, y)].get_object()
                if obj is None:
                    s += "non".ljust(width)
                else:
                    s += type(obj).__name__.ljust(width - 5)
                    s += str(obj.get_health()).ljust(5)
            s += "\n\n"

        return s

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
