import copy

from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_move(board, attack, attacker_pos):
    """Move object into another position. If any tiles, objects were affected,
    return their original states along with their positions."""
    attacker = board[attacker_pos].get_object()
    start_pos = attacker_pos
    dst_pos = attack.get_vector()
    if start_pos == dst_pos:
        raise Exception
    if board[dst_pos].has_object():
        raise Exception("Space is occupied")

    start_tile = copy.deepcopy(board[start_pos])
    # Shallow copy possible as there is no object on destination tile
    destination_tile = copy.copy(board[dst_pos])
    ret = {start_pos: start_tile, dst_pos: destination_tile}

    board[dst_pos].set_object(attacker)
    board[start_pos].set_object(None)
    board.modify_object_position_cache(attacker.get_id(), dst_pos)
    convert_tile_if_needed(board, dst_pos)
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, dst_pos, attacker))

    return ret
