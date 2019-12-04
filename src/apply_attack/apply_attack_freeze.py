from src.apply_attack.apply_attack import freeze_tile


def apply_attack_freeze(board, attack):
    attack_pos = attack.get_attacker()
    # Convert tile
    freeze_tile(board, attack_pos)
    # Freeze any objects
    board[attack_pos].freeze()
