import copy

from src.apply_attack.apply_attack_burn import apply_attack_burn
from src.game_objects.attack import Attack
from src.game_objects.vek import Vek, Psion
from src.game_objects.weapons.burn import Burn
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_environment(board):
    """Looks for any fire, storm clouds and regenerating psions and applies their effects"""
    d = {}
    # First, look for fire
    for _, pos in copy.copy(board.get_object_position_cache()).items():
        obj = board[pos].get_object()
        # TODO: Is this needed?
        if obj is None:
            continue
        if obj.is_on_fire():
            attack = Attack(attacker=pos, weapon=Burn(), vector=None)
            update_dict_if_key_not_present(d, apply_attack_burn(board, attack))

    # Second, look for anyone who can regenerate veks
    # TODO: Check behaviour in solver!
    if board.is_blood_psion_present():
        for _, pos in board.get_object_position_cache().items():
            obj = board[pos].get_object()
            if isinstance(obj, Vek) and not isinstance(obj, Psion):
                if obj.get_health() < obj.get_max_health():
                    # TODO: Yeah, add a heal function
                    obj._health += 1

    # TODO: Add storm clouds damage
    # TODO: Add psion attack

    return d
