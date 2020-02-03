import copy

from src.apply_attack.apply_attack import damage_tile
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_kill(board, attack):
    pos = attack.get_attacker()
    tile = board[pos]
    obj = tile.get_object()
    if obj is None:
        if not is_tile_damageable(tile):
            return {}
        ret = {pos: tile}
        damage_tile(board, pos, tile, None)
        return ret

    ret = {pos: copy.deepcopy(tile)}
    obj._health = 0
    obj.clear_shield()
    damage_tile(board, pos, tile, obj)
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, pos, obj))
    return ret


