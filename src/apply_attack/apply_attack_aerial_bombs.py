from src.apply_attack.apply_attack import smoke_tile
from src.helpers.kill_object import kill_object_if_possible


def apply_attack_aerial_bombs(board, attack, attacker_pos):
    attacker = board[attacker_pos].get_object()
    vector = attack.get_vector()
    attack_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    # Check if attack can still be applied
    if not board.in_bounds(attack_pos):
        return

    # TODO: Ugly, consider rewrite
    points_to_smoke = []
    if vector[1] != 0:
        if attacker_pos[1] > attack_pos[1]:
            for y in range(attack_pos[1] + 1, attacker_pos[1]):
                points_to_smoke.append((attack_pos[0], y))
        else:
            for y in range(attacker_pos[1] + 1, attack_pos[1]):
                points_to_smoke.append((attack_pos[0], y))
    else:
        if attacker_pos[0] > attack_pos[0]:
            for x in range(attack_pos[0] + 1, attacker_pos[0]):
                points_to_smoke.append((x, attack_pos[1]))
        else:
            for x in range(attacker_pos[0] + 1, attack_pos[0]):
                points_to_smoke.append((x, attack_pos[1]))

    # Move object to a new tile
    board[attack_pos].set_object(attacker)
    board[attacker_pos].set_object(None)
    # Apply tile effect, object may die, be lit on fire
    board[attack_pos].apply_tile_effects()

    # Kill object if it landed on something dangerous
    kill_object_if_possible(board, attacker)

    # Now damage and smoke all tiles along the way
    dmg = attack.get_weapon().get_total_damage()
    for point in points_to_smoke:
        board.regular_damage(point, dmg)
        smoke_tile(board, point)
        obj = board[point].get_object()
        if obj is not None:
            kill_object_if_possible(board, obj)
