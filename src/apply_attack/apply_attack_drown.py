import copy

from src.game_objects.tiles.tile import WaterTile
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_drown(board, attack):
    attack_pos = attack.get_attacker()

    # If obj is None, then shallow copy is sufficient
    obj = board[attack_pos].get_object()
    if obj is None:
        ret = {attack_pos: copy.copy(board[attack_pos])}
    else:
        ret = {attack_pos: copy.deepcopy(board[attack_pos])}

    board[attack_pos] = WaterTile(_object=obj)
    convert_tile_if_needed(board, attack_pos)
    if obj is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, attack_pos, obj))

    return ret
