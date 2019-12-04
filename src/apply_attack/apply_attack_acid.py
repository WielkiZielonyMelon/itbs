from src.apply_attack.apply_attack import acidify_tile


def apply_attack_acid(board, attack):
    acidify_tile(board, attack.get_attacker())
