import copy

from src.apply_attack.apply_attack import fire_tile
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_set_on_fire(board, attack):
    attack_pos = attack.get_attacker()
    ret = {attack_pos: copy.deepcopy(board[attack_pos])}
    fire_tile(board, attack_pos)
    convert_tile_if_needed(board, attack_pos)
    obj = board[attack_pos].get_object()
    if obj is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, attack_pos))
    return ret
