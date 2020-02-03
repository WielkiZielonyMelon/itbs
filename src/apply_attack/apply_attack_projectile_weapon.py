import copy

from src.apply_attack.apply_attack import damage_tile
from src.apply_attack.apply_attack_push import apply_attack_push
from src.game_objects.attack import Attack
from src.game_objects.weapons.push import Push
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.is_tile_damagable import is_tile_damageable
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_projectile_weapon(board, attack, attacker_pos, push=False):
    # Grab direction of attack
    vector = attack.get_vector()

    # Grab first position that the projectile will fly through
    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])

    # If position is no longer in range, than object must have been pushed to an edge of board
    if not board.in_bounds(attack_pos):
        return {}

    tile = board[attack_pos]
    obj = tile.get_object()
    # Keep pushing projectile until we find an object or we reach edge of board
    while obj is None:
        new_attack_pos = (attack_pos[0] + vector[0], attack_pos[1] + vector[1])
        if not board.in_bounds(new_attack_pos):
            # We have reached edge of the board. We know there is no object, so if tile is not damageable,
            # then this projectile will not change the state of board
            if not is_tile_damageable(tile):
                return {}
            break

        attack_pos = new_attack_pos
        tile = board[attack_pos]
        obj = tile.get_object()

    # If object is None at this point, we know that the tile is damageable. Do not perform copy
    # as tile will be overwritten in damage procedure
    if obj is None:
        ret = {attack_pos: tile}
        # In this case we can damage the tile directly.
        damage_tile(board, attack_pos)
        return ret

    # Store original tile
    ret = {attack_pos: copy.deepcopy(tile)}
    # Damage tile and object
    dmg = attack.get_weapon().get_total_damage()
    board.regular_damage(attack_pos, dmg)
    if push is True:
        attack = Attack(attacker=attack_pos, weapon=Push(), vector=vector)
        update_dict_if_key_not_present(ret, apply_attack_push(board, attack))

    # Convert the tile (for example, object might have been on acid and it's sinking
    # in WaterTile(convert to AcidTile) or it was on acid and was killed convert to (AcidPool)
    convert_tile_if_needed(board, attack_pos)

    # If object still exist and wasn't killed by push function, it still might be killed here.
    obj = board[attack_pos].get_object()
    if obj is not None:
        update_dict_if_key_not_present(ret, kill_object_if_possible(board, attack_pos, obj))

    return ret
