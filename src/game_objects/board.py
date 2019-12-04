from src.game_objects.tiles.tile import GroundTile
from src.game_objects.vek import BlastPsion, PsionAbomination


class Board:
    """Board where game tiles are placed"""
    BOARD_MAX_X_SIZE = 8
    BOARD_MAX_Y_SIZE = 8

    def __init__(self):
        """Initializes board with empty tiles"""
        self._tiles = [[GroundTile(_object=None)
                       for x in range(self.BOARD_MAX_X_SIZE)]
                       for y in range(self.BOARD_MAX_Y_SIZE)]

    def is_explosive_psion_present(self):
        for x in range(0, self.BOARD_MAX_X_SIZE):
            for y in range(0, self.BOARD_MAX_Y_SIZE):
                obj = self[(x, y)].get_object()
                if obj is not None and isinstance(obj, (BlastPsion, PsionAbomination)):
                    return True

        return False

    def in_bounds(self, pos):
        if pos[0] < 0:
            return False
        if pos[0] >= self.BOARD_MAX_X_SIZE:
            return False
        if pos[1] < 0:
            return False
        if pos[1] >= self.BOARD_MAX_Y_SIZE:
            return False

        return True

    def are_tiles_the_same(self, other):
        """Compare tiles, not objects"""
        for x in range(0, self.BOARD_MAX_X_SIZE):
            for y in range(0, self.BOARD_MAX_Y_SIZE):
                if type(self) != type(other):
                    return False

        return True

    # TODO: Refactor, this is ugly
    def print_board(self):
        width = 25
        s = ""
        for y in range(0, self.BOARD_MAX_Y_SIZE):
            s += "Description".ljust(width)
            for x in range(0, self.BOARD_MAX_X_SIZE):
                s += type(self[(x, y)]).__name__.ljust(width)

            s += "\n"
            s += "Smoke".ljust(width)
            for x in range(0, self.BOARD_MAX_X_SIZE):
                s += str(self[(x, y)].has_smoke()).ljust(width)

            s+= "\n"
            s += "Object".ljust(width)
            for x in range(0, self.BOARD_MAX_X_SIZE):
                obj = self[(x, y)].get_object()
                if obj is None:
                    s += "non".ljust(width)
                else:
                    s += type(obj).__name__.ljust(width - 5)
                    s += str(obj.get_health()).ljust(5)
            s += "\n\n"

        return s

    def __getitem__(self, key):
        return self._tiles[key[0]][key[1]]

    def __setitem__(self, key, val):
        self._tiles[key[0]][key[1]] = val

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)
