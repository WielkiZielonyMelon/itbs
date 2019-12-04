import copy

from src.apply_attack.apply_attack import acidify_tile, damage_tile
from src.game_objects.tiles.tile import ForestTile, ChasmTile, ForestFireTile
from src.game_objects.vek import Vek
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def kill_object(board, obj):
    """Kills object. No questions asked"""
    pos = board.find_object_position(obj)
    tile = board[pos]
    ret = {pos: copy.deepcopy(tile)}
    board[pos].set_object(None)

    # Acid has higher priority than...
    if obj.is_on_acid():
        acidify_tile(board, pos)
    # ... fire
    elif obj.is_on_fire():
        if isinstance(tile, ForestTile):
            board[pos] = ForestFireTile(_object=None)

    if obj.is_exploding() or (isinstance(obj, Vek) and board.is_explosive_psion_present()):
        # Damage neighbouring tiles, damage objects and convert tiles if needed
        tiles_pos = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                     (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        affected_tiles_pos = []
        for tile_pos in tiles_pos:
            if not board.in_bounds(tile_pos):
                continue
            affected_tiles_pos.append(tile_pos)

        for affected_tile_pos in affected_tiles_pos:
            ret[affected_tile_pos] = copy.deepcopy(board[affected_tile_pos])
            damage_tile(board, affected_tile_pos)
            board[affected_tile_pos].regular_damage(1)
            convert_tile_if_needed(board, affected_tile_pos)

        # It might turn out, we need to kill neighbouring objects
        for affected_tile_pos in affected_tiles_pos:
            obj = board[affected_tile_pos].get_object()
            if obj is not None:
                update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj))

    return ret


def kill_object_if_possible(board, obj):
    """Kill object if it is possible.

    Attempts to remove an object from board, if conditions are met (like health below zero, object is non-flying
    and over chasm, etc.). If object is killed, tiles will also change as a result (for example, object on acid
    killed on a ground tile will leave an AcidPool behind).
    """
    # Does this object still exist?
    pos = board.find_object_position(obj)
    if pos is None:
        return {}

    tile = board[pos]
    # If object's health is below zero, we can kill it
    if obj.get_health() <= 0:
        # Remove object already
        return kill_object(board, obj)

    # If object is flying and frozen...
    if obj.is_flying():
        if obj.is_frozen():
            # ... it will always die over chasm tile ...
            if isinstance(tile, ChasmTile):
                return kill_object(board, obj)
            # ... if it's non-massive it will drown in liquid...
            elif not obj.is_massive() and tile.is_liquid():
                return kill_object(board, obj)

        return {}

    # All non-flying objects can be instantly killed over chasm
    if isinstance(tile, ChasmTile):
        # Remove object already
        return kill_object(board, obj)

    # Massive objects cannot be killed over other tiles
    if obj.is_massive():
        return {}

    # We are left with non-massive, non-flying object. They will die in liquid tiles
    if tile.is_liquid():
        return kill_object(board, obj)

    return {}
