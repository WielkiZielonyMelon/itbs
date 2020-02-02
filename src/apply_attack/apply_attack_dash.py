import copy


def apply_attack_dash(board, attack, attacker_pos):
    attacker = board[attacker_pos].get_object()

    ret = {attacker_pos: copy.deepcopy(board[attacker_pos])}
    direction = attack.get_vector()
    attack_pos = (attacker_pos[0] + direction[0], attacker_pos[1] + direction[1])

    # TODO: Fix this, ugly
    dict_candidate = None
    while board.in_bounds(attack_pos) and board[attack_pos].get_object() is None:
        # TODO: If object is not massive it should sink
        dict_candidate = copy.deepcopy(board[attack_pos])
        board[attack_pos].set_object(attacker)
        board[attacker_pos].set_object(None)
        board.modify_object_position_cache(attacker.get_id(), attack_pos)
        attacker_pos = attack_pos
        attack_pos = (attack_pos[0] + direction[0], attack_pos[1] + direction[1])

    if dict_candidate is not None:
        ret[attacker_pos] = dict_candidate

    return ret
