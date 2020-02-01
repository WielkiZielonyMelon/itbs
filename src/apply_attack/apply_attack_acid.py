import copy

from src.apply_attack.apply_attack import acidify_tile


def apply_attack_acid(board, attack):
    pos = attack.get_attacker()
    ret = {pos: copy.deepcopy(board[pos])}
    acidify_tile(board, attack.get_attacker())

    return ret
