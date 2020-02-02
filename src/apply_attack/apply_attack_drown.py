import copy

from src.game_objects.tiles.tile import WaterTile
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_drown(board, attack):
    attack_pos = attack.get_attacker()
    tile = board[attack_pos]
    obj = tile.get_object()

    # If there is no object, just add tile to dictionary, as it will not be referenced
    if obj is None:
        ret = {attack_pos: tile}
        board[attack_pos] = WaterTile(_object=None)
        return ret

    # Object exists. Deep copy is a must, tile conversion (as object might be on acid) and it might be killed
    ret = {attack_pos: copy.deepcopy(board[attack_pos])}
    board[attack_pos] = WaterTile(_object=obj)
    convert_tile_if_needed(board, attack_pos)
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, attack_pos, obj))

    return ret
