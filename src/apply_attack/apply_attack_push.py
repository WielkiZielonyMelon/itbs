import copy

from src.apply_attack.apply_attack_move import apply_attack_move
from src.game_objects.attack import Attack
from src.game_objects.weapons.move import Move
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_push(board, attack):
    push_pos = attack.get_attacker()
    if not board.in_bounds(push_pos):
        return {}
    object_to_push = board[push_pos].get_object()
    # If there is no object, than nothing can be moved
    if object_to_push is None:
        return {}

    # Non pushable objects cannot be pushed
    if not object_to_push.is_pushable():
        # kill_object_if_possible(board, object_to_push)
        return {}

    direction = attack.get_vector()
    new_pos = (push_pos[0] + direction[0], push_pos[1] + direction[1])

    # If out of bounds, do not push object
    if not board.in_bounds(new_pos):
        return {}

    # If not obstructed, push!
    if not board[new_pos].has_object():
        attack = Attack(attacker=object_to_push.get_id(), weapon=Move(), vector=new_pos)
        return apply_attack_move(board, attack)

    # Destination is obstructed
    ret = {new_pos: copy.deepcopy(board[new_pos]), push_pos: copy.deepcopy(board[push_pos])}
    board[new_pos].bump_damage(1)
    board[push_pos].bump_damage(1)

    tile = board[new_pos]
    obj = tile.get_object()
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj))

    tile = board[push_pos]
    obj = tile.get_object()
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, obj))

    return ret
