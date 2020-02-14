import copy

from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_fangs(board, attack, attacker_pos):
    vector = attack.get_vector()

    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    if not board.in_bounds(attack_pos):
        # Seems object was pushed to a position where it cannot perform attack
        return {}

    tile = board[attack_pos]
    obj = tile.get_object()
    if obj is None:
        if is_tile_damageable(tile) is False:
            return {}
        ret = {attack_pos: tile}
        board.regular_damage(attack_pos, 1)

        return ret

    ret = {attack_pos: copy.deepcopy(tile)}
    board.regular_damage(attack_pos, attack.get_weapon().get_total_damage())

    update_dict_if_key_not_present(ret, kill_object_if_possible(board, attack_pos, obj))

    return ret
