import copy

from src.apply_attack.apply_attack_kill import apply_attack_kill
from src.apply_attack.apply_attack_move import apply_attack_move
from src.game_objects.attack import Attack
from src.game_objects.supply_train import SupplyTrainWreck
from src.game_objects.weapons.kill import Kill
from src.game_objects.weapons.move import Move
from src.helpers.update_dict_if_key_not_present import update_dict_if_key_not_present


def apply_attack_choo_choo(board, attack, attacker_pos):
    # Train is frozen? Quit...
    train_head = board[attacker_pos].get_object()
    if train_head.is_frozen():
        return {}

    # Train wreck? Can't move that
    if isinstance(train_head, SupplyTrainWreck):
        return {}

    vector = attack.get_vector()
    attack_pos_0 = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
    attack_pos_1 = (attack_pos_0[0] + vector[0], attack_pos_0[1] + vector[1])
    tail_pos = (attacker_pos[0] - vector[0], attacker_pos[1] - vector[1])

    # If train is not blocked, this is obvious
    obj_0 = board[attack_pos_0].get_object()
    obj_1 = board[attack_pos_1].get_object()

    ret = {attacker_pos: copy.deepcopy(board[attacker_pos]), tail_pos: copy.deepcopy(board[tail_pos])}
    if obj_0 is None and obj_1 is None:
        # Do not update dictionary, nothing will happen with this move. Unless someone is trying to drive
        # train into lava...
        attack = Attack(attacker=attacker_pos, weapon=Move(), vector=attack_pos_1)
        apply_attack_move(board, attack, attacker_pos)
        attack = Attack(attacker=tail_pos, weapon=Move(), vector=attack_pos_0)
        apply_attack_move(board, attack, attacker_pos)
        return ret

    if obj_0 is not None:
        for pos in [attacker_pos, tail_pos]:
            wreck = SupplyTrainWreck()
            board[pos].set_object(wreck)
            board.modify_object_position_cache(wreck.get_id(), pos)

        attack = Attack(attacker=attack_pos_0, weapon=Kill(), vector=None)
        update_dict_if_key_not_present(ret, apply_attack_kill(board, attack))
    else:
        tail = board[tail_pos].get_object()
        board[tail_pos].set_object(None)
        board.remove_from_object_position_cache(tail.get_id())
        for pos in [attacker_pos, attack_pos_0]:
            wreck = SupplyTrainWreck()
            board[pos].set_object(wreck)
            board.modify_object_position_cache(wreck.get_id(), pos)

        attack = Attack(attacker=attack_pos_0, weapon=Kill(), vector=None)
        update_dict_if_key_not_present(ret, apply_attack_kill(board, attack))

    return ret
