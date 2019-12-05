import copy

from src.apply_attack.apply_attack_push import apply_attack_push
from src.apply_attack.apply_attack import damage_tile
from src.game_objects.attack import Attack
from src.game_objects.building import Building
from src.game_objects.weapons.push import Push
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_artemis(board, attack):
    attacker = attack.get_attacker()
    attacker_pos = board.find_object_id_position(attacker)
    vector = attack.get_vector()
    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])

    # If attack position is not in bounds (possible, object might have been moved), cancel attack
    if not board.in_bounds(attack_pos):
        return {}

    ret = {}
    weapon = attack.get_weapon()
    attacked_obj = board[attack_pos].get_object()
    if attacked_obj is None and not is_tile_damageable(board[attack_pos]):
        pass
    else:
        ret[attack_pos] = copy.deepcopy(board[attack_pos])

    # Do not damage buildings, if we have proper power-up
    if weapon.has_buildings_immune() and isinstance(attacked_obj, Building):
        pass
    # Damage the tile and object
    else:
        damage_tile(board, attack_pos)
        board[attack_pos].regular_damage(weapon.get_total_damage())

    # Push all the tiles around the attack. Modify attacked, so Push will understand
    for x in [-1, 1]:
        attack = Attack(attacker=(attack_pos[0] + x, attack_pos[1]), weapon=Push(), vector=(x, 0))
        update_dict_if_key_not_present(ret, apply_attack_push(board, attack))

    for y in [-1, 1]:
        attack = Attack(attacker=(attack_pos[0], attack_pos[1] + y), weapon=Push(), vector=(0, y))
        update_dict_if_key_not_present(ret, apply_attack_push(board, attack))

    convert_tile_if_needed(board, attack_pos)

    obj_to_kill = board[attack_pos].get_object()
    if obj_to_kill is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj_to_kill))

    return ret
