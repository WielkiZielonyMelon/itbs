from src.apply_attack.apply_attack_burn import apply_attack_burn
from src.game_objects.attack import Attack
from src.game_objects.weapons.burn import Burn
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_environment(board):
    """Looks for any fire, storm clouds and regenerating psions and applies their effects"""
    d = {}
    # First, look for fire
    for row in range(0, board.BOARD_X_SIZE):
        for col in range(0, board.BOARD_Y_SIZE):
            obj = board[(row, col)].get_object()
            if obj is None:
                continue
            if obj.is_on_fire():
                attack = Attack(attacker=(row, col), weapon=Burn(), vector=None)
                update_dict_if_key_not_present(d, apply_attack_burn(board, attack))

    # TODO: Add storm clouds damage
    # TODO: Add psion attack
    # TODO: Add psion regeneration

    return d
