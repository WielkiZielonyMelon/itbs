import copy

from src.apply_attack.apply_attack import damage_tile
from src.apply_attack.apply_attack_dash import apply_attack_dash
from src.apply_attack.apply_attack_push import apply_attack_push
from src.game_objects.attack import Attack
from src.game_objects.tiles.tile import GroundTile, WaterTile
from src.game_objects.weapons.push import Push
from src.helpers.convert_tile_if_needed import convert_tile_if_needed
from src.helpers.find_object_position import find_object_id_position
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_titan_fist(board, attack):
    # If titan first has dash, move the attacker
    ret = {}
    if attack.get_weapon().has_dash():
        update_dict_if_key_not_present(ret, apply_attack_dash(board, attack))

    attacker = attack.get_attacker()
    attacker_pos = find_object_id_position(board, attacker)
    vector = attack.get_vector()
    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    if not board.in_bounds(attack_pos):
        return {}

    # Will this attack have any effect?
    if not board[attack_pos].has_object() and isinstance(board[attack_pos], (GroundTile, WaterTile)):
        return {}

    update_dict_if_key_not_present(ret, {attack_pos: copy.deepcopy(board[attack_pos])})

    # Damage tile, but do not apply any effects yet, as object might
    # be pushed out of a tile
    damage_tile(board, attack_pos)

    # Damage any present objects
    board[attack_pos].regular_damage(attack.get_weapon().get_total_damage())

    # And finally push
    push_attack = Attack(attacker=attack_pos, weapon=Push(), vector=vector)
    update_dict_if_key_not_present(ret, apply_attack_push(board, push_attack))
    convert_tile_if_needed(board, attack_pos)

    return ret
