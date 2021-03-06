import copy

from src.game_objects.tiles.tile import ChasmTile
from src.game_objects.vek import Emerged
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_emerging(board, attack):
    pos = attack.get_attacker()
    tile = board[pos]
    # If tile is liquid, emerging was cancelled
    if tile.is_liquid():
        return {}

    # If tile is a chasm, emerging was cancelled
    if isinstance(tile, ChasmTile):
        return {}

    # If there is no object present on tile, spawn dummy vek
    # Also, return a shallow copy
    obj = tile.get_object()
    if obj is None:
        ret = {pos: copy.copy(tile)}
        emerged = Emerged()
        tile.set_object(emerged)
        board.modify_object_position_cache(emerged.get_id(), pos)
        return ret

    ret = {pos: copy.deepcopy(tile)}
    # There is an object present. Damage it and kill if possible
    tile.emerge_damage(1)
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, pos, obj))
    return ret


