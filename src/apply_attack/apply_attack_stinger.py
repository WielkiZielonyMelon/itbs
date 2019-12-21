import copy

from src.apply_attack.apply_attack import damage_tile
from src.game_objects.weapons.stinger import LaunchingStinger, SuperStinger
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_stinger(board, attack):
    if isinstance(attack.get_weapon(), (LaunchingStinger, SuperStinger)):
        raise Exception("Not implemented yet!")
    attacker = attack.get_attacker()
    attacker_pos = board.find_object_id_position(attacker)
    vector = attack.get_vector()

    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    if not board.in_bounds(attack_pos):
        # Seems object was pushed to a position where it cannot perform attack
        return {}

    # Will this attack have any effect?
    if not board[attack_pos].has_object() and not is_tile_damageable(board[attack_pos]):
        return {}

    ret = {}
    update_dict_if_key_not_present(ret, {attack_pos: copy.deepcopy(board[attack_pos])})

    # Damage tile, but do not apply any effects yet, as object might
    # be pushed out of a tile
    damage_tile(board, attack_pos)

    # Damage any present objects
    board.regular_damage(attack_pos, attack.get_weapon().get_total_damage())

    convert_tile_if_needed(board, attack_pos)

    obj = board[attack_pos].get_object()
    if obj is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj))

    return ret
