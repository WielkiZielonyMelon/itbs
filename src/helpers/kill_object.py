import copy

from src.apply_attack.apply_attack import acidify_tile, damage_tile
from src.game_objects.mech import Mech
from src.game_objects.satellite_rocket import SatelliteRocket, ReadySatelliteRocket
from src.game_objects.supply_train import SupplyTrainHead, SupplyTrainTail, SupplyTrainWreck
from src.game_objects.tiles.tile import ForestTile, ChasmTile, ForestFireTile
from src.game_objects.vek import Vek
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def kill_object(board, pos, tile, obj):
    """Kills object. No questions asked"""
    # As an exception do not perform full deepcopy. Object will no longer be referenced, it cannot be changed
    # so a flat copy is appropriate.
    ret = {pos: copy.copy(tile)}
    # As object is dead, we have to remove webs. This of course changes state of object
    # so we need to store that information
    ret.update(board.clear_web_to(pos))
    if not isinstance(obj, (Mech, SatelliteRocket, ReadySatelliteRocket, SupplyTrainHead, SupplyTrainTail,
                            SupplyTrainWreck)) or isinstance(tile, ChasmTile):
        board[pos].set_object(None)
        board.remove_from_object_position_cache(obj.get_id())

    if isinstance(obj, (SupplyTrainHead, SupplyTrainTail)):
        # Train was damaged, replace it with wreck
        wreck = SupplyTrainWreck()
        board[pos].set_object(wreck)
        board.remove_from_object_position_cache(obj.get_id())
        board.modify_object_position_cache(wreck.get_id(), pos)
        for obj_id, position in board.get_object_position_cache().items():
            train = board[position].get_object()
            if isinstance(train, (SupplyTrainHead, SupplyTrainTail)):
                ret[position] = copy.copy(board[position])
                board.remove_from_object_position_cache(obj_id)
                wreck = SupplyTrainWreck()
                board[position].set_object(wreck)
                board.modify_object_position_cache(wreck.get_id(), position)
                break

    # Acid has higher priority than...
    if obj.is_on_acid():
        acidify_tile(board, pos)
    # ... fire
    elif obj.is_on_fire():
        if isinstance(tile, ForestTile):
            board[pos] = ForestFireTile(_object=None)

    if obj.is_exploding() or (isinstance(obj, Vek) and board.is_blast_psion_present()):
        # Damage neighbouring tiles, damage objects and convert tiles if needed
        tiles_pos = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                     (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        affected_tiles_pos = [tile_pos for tile_pos in tiles_pos if board.in_bounds(tile_pos)]

        for affected_tile_pos in affected_tiles_pos:
            tile = board[affected_tile_pos]
            obj = tile.get_object()
            # Will this attack have any effect?
            if obj is None and not is_tile_damageable(tile):
                continue

            ret[affected_tile_pos] = copy.deepcopy(tile)
            damage_tile(board, affected_tile_pos, tile, obj)
            tile.regular_damage(1)
            convert_tile_if_needed(board, affected_tile_pos)

        # It might turn out, we need to kill neighbouring objects
        for affected_tile_pos in affected_tiles_pos:
            obj = board[affected_tile_pos].get_object()
            if obj is not None:
                update_dict_if_key_not_present(ret, kill_object_if_possible(board, affected_tile_pos, obj))

    return ret


def kill_object_if_possible(board, pos, obj):
    """Kill object if it is possible.

    Attempts to remove an object from board, if conditions are met (like health below zero, object is non-flying
    and over chasm, etc.). If object is killed, tiles will also change as a result (for example, object on acid
    killed on a ground tile will leave an AcidPool behind).
    """
    tile = board[pos]

    # If object's health is below zero, we can kill it
    if obj.get_health() <= 0:
        # Remove object already
        return kill_object(board, pos, tile, obj)

    # If object is flying and frozen...
    if obj.is_flying():
        if obj.is_frozen():
            # ... it will always die over chasm tile ...
            if isinstance(tile, ChasmTile):
                return kill_object(board, pos, tile, obj)
            # ... if it's non-massive it will drown in liquid...
            elif not obj.is_massive() and tile.is_liquid():
                return kill_object(board, pos, tile, obj)

        return {}

    # All non-flying objects can be instantly killed over chasm
    if isinstance(tile, ChasmTile):
        # Remove object already
        return kill_object(board, pos, tile, obj)

    # Massive objects cannot be killed over other tiles
    if obj.is_massive():
        return {}

    # We are left with non-massive, non-flying object. They will die in liquid tiles
    if tile.is_liquid():
        return kill_object(board, pos, tile, obj)

    return {}
