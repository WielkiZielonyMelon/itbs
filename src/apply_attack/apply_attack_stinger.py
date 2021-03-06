import copy

from src.game_objects.weapons.stinger import LaunchingStinger, SuperStinger
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


# TODO: Rewrite this function, looks a bit ugly
def apply_attack_stinger(board, attack, attacker_pos):
    vector = attack.get_vector()

    attack_pos = [(attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])]
    if not board.in_bounds(attack_pos[0]):
        # Seems object was pushed to a position where it cannot perform attack
        return {}

    if isinstance(attack.get_weapon(), LaunchingStinger):
        proposition = (attack_pos[-1][0] + vector[0], attack_pos[-1][1] + vector[1])
        if board.in_bounds(proposition):
            attack_pos.append(proposition)
    if isinstance(attack.get_weapon(), SuperStinger):
        proposition = (attack_pos[-1][0] + vector[0], attack_pos[-1][1] + vector[1])
        if board.in_bounds(proposition):
            attack_pos.append(proposition)

    ret = {}

    for a_pos in attack_pos:
        tile = board[a_pos]
        # Object present, perform deep copy
        if tile.get_object():
            ret[a_pos] = copy.deepcopy(tile)
        # As there is no object, tile is damageable, it will be replaced in regular_damage
        elif is_tile_damageable(tile):
            ret[a_pos] = tile

        board.regular_damage(a_pos, attack.get_weapon().get_total_damage())
        convert_tile_if_needed(board, a_pos)

    for a_pos in attack_pos:
        obj = board[a_pos].get_object()
        if obj is not None:
            update_dict_if_key_not_present(ret, kill_object_if_possible(board, a_pos, obj))

    return ret
