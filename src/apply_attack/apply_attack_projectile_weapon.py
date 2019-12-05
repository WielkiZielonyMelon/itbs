import copy

from src.apply_attack.apply_attack import damage_tile
from src.apply_attack.apply_attack_push import apply_attack_push
from src.game_objects.attack import Attack
from src.game_objects.weapons.push import Push
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_projectile_weapon(board, attack, push=False):
    attacker = attack.get_attacker()
    attacker_pos = board.find_object_id_position(attacker)
    vector = attack.get_vector()

    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    if not board.in_bounds(attack_pos):
        # Seems object was pushed to a position where it cannot perform attack
        return {}

    while True:
        obj = board[attack_pos].get_object()
        if obj is not None:
            break

        new_attack_pos = (attack_pos[0] + vector[0], attack_pos[1] + vector[1])
        if not board.in_bounds(new_attack_pos):
            break

        attack_pos = new_attack_pos

    if not board[attack_pos].has_object() and not is_tile_damageable(board[attack_pos]):
        return {}

    # Store original tile
    ret = {attack_pos: copy.deepcopy(board[attack_pos])}
    # Damage tile
    damage_tile(board, attack_pos)
    # Damage object
    dmg = attack.get_weapon().get_total_damage()
    board[attack_pos].regular_damage(dmg)
    # Store object for later reference
    obj = board[attack_pos].get_object()
    if push is True:
        attack = Attack(attacker=attack_pos, weapon=Push(), vector=vector)
        update_dict_if_key_not_present(ret, apply_attack_push(board, attack))

    # Convert the tile (for example, object might have been on acid and it's sinking
    # in WaterTile(convert to AcidTile) or it was on acid and was killed convert to (AcidPool)
    convert_tile_if_needed(board, attack_pos)
    if obj is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj))

    return ret
