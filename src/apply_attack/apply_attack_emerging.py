import copy

from src.game_objects.vek import Emerged
from src.game_objects.tiles.tile import ChasmTile
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

    ret = {pos: copy.deepcopy(board[pos])}
    # If there is no object present on tile, spawn dummy vek
    obj = tile.get_object()
    if obj is None:
        tile.set_object(Emerged())
        return ret

    # There is an object present. Damage it and kill if possible
    tile.emerge_damage(1)
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj))
    return ret


