import copy

from src.apply_attack.apply_attack_kill import apply_attack_kill
from src.game_objects.attack import Attack
from src.game_objects.weapons.kill import Kill
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_launch(board, attack):
    pos = attack.get_attacker()
    tile = board[pos]
    ret = {pos: copy.deepcopy(tile)}

    # Remove object from board completely
    obj = tile.get_object()
    tile.set_object(None)
    board.remove_from_object_position_cache(obj.get_id())

    for x in [-1, 1]:
        attack = Attack(attacker=(pos[0] + x, pos[1]), weapon=Kill(), vector=(x, 0))
        update_dict_if_key_not_present(ret, apply_attack_kill(board, attack))

    for y in [-1, 1]:
        attack = Attack(attacker=(pos[0], pos[1] + y), weapon=Kill(), vector=(0, y))
        update_dict_if_key_not_present(ret, apply_attack_kill(board, attack))
    return ret
