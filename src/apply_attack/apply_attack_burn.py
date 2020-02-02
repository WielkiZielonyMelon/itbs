import copy

from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_burn(board, attack):
    pos = attack.get_attacker()
    tile = board[pos]
    obj = tile.get_object()
    ret = {pos: copy.deepcopy(tile)}
    tile.fire_damage()

    update_dict_if_key_not_present(ret, kill_object_if_possible(board, pos, obj))

    return ret
