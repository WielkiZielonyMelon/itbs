import copy

from src.apply_attack.apply_attack_move import apply_attack_move
from src.game_objects.attack import Attack
from src.game_objects.weapons.move import Move
from src.helpers.kill_object import kill_object_if_possible
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_push(board, attack):
    push_from = attack.get_attacker()
    if not board.in_bounds(push_from):
        return {}
    push_from_tile = board[push_from]
    object_to_push = push_from_tile.get_object()
    # If there is no object, than nothing can be moved
    if object_to_push is None:
        return {}

    # Non pushable objects cannot be pushed
    if not object_to_push.is_pushable():
        # kill_object_if_possible(board, object_to_push)
        return {}

    direction = attack.get_vector()
    push_to = (push_from[0] + direction[0], push_from[1] + direction[1])

    # If out of bounds, do not push object
    if not board.in_bounds(push_to):
        return {}

    # If not obstructed, push!
    push_to_tile = board[push_to]
    blocker = push_to_tile.get_object()
    if blocker is None:
        attack = Attack(attacker=object_to_push.get_id(), weapon=Move(), vector=push_to)
        return apply_attack_move(board, attack, push_from)

    # Destination is obstructed
    ret = {push_to: copy.deepcopy(push_to_tile), push_from: copy.deepcopy(push_from_tile)}
    board[push_to].bump_damage(1)
    board[push_from].bump_damage(1)

    update_dict_if_key_not_present(ret, kill_object_if_possible(board, push_to, blocker))
    update_dict_if_key_not_present(ret, kill_object_if_possible(board, push_from, object_to_push))

    return ret
