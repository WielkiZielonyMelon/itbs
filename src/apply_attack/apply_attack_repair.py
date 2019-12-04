import copy

from src.apply_attack.apply_attack import repair_tile
from src.game_objects.tiles.tile import ForestFireTile, FireTile


def apply_attack_repair(board, attack):
    attacker = attack.get_attacker()
    attack_pos = board.find_object_id_position(attacker)
    attacker = board[attack_pos].get_object()
    if attacker.get_health() == attacker.get_max_health() and \
            not isinstance(board[attack_pos], (ForestFireTile, FireTile)) and \
            not attacker.is_on_fire() and not attacker.is_on_acid():
        return {}
    ret = {attack_pos: copy.deepcopy(board[attack_pos])}
    # Convert tile
    repair_tile(board, attack_pos)
    # Repair any objects
    board[attack_pos].repair()

    return ret
