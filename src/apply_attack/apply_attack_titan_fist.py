import copy

from src.apply_attack.apply_attack_dash import apply_attack_dash
from src.apply_attack.apply_attack_push import apply_attack_push
from src.game_objects.attack import Attack
from src.game_objects.weapons.push import Push
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_titan_fist(board, attack, attacker_pos):
    # If titan first has dash, move the attacker
    ret = {}
    if attack.get_weapon().has_dash():
        update_dict_if_key_not_present(ret, apply_attack_dash(board, attack, attacker_pos))
        attacker = attack.get_attacker()
        attacker_pos = board.find_object_id_position(attacker)

    vector = attack.get_vector()
    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    if not board.in_bounds(attack_pos):
        return ret

    # Will this attack have any effect?
    if not board[attack_pos].has_object() and not is_tile_damageable(board[attack_pos]):
        return ret

    update_dict_if_key_not_present(ret, {attack_pos: copy.deepcopy(board[attack_pos])})

    # Damage tile and any present objects
    board.regular_damage(attack_pos, attack.get_weapon().get_total_damage())

    # And finally push
    push_attack = Attack(attacker=attack_pos, weapon=Push(), vector=vector)
    update_dict_if_key_not_present(ret, apply_attack_push(board, push_attack))
    convert_tile_if_needed(board, attack_pos)

    tile = board[attack_pos]
    obj = tile.get_object()
    if obj is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, attack_pos, obj))

    return ret
