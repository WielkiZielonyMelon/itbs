import itertools

from src.game_objects.attack import Attack
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


def get_possible_attacks(board, attacker_pos):
    """Return a list of possible attacks for object in provided position"""
    tile = board[attacker_pos]
    attacker = tile.get_object()
    # Non-flying object in water can't attack
    if tile.is_liquid() and not attacker.is_flying():
        return []

    # If attacker is in smoke, there is no possibility to attack
    if tile.has_smoke():
        # TODO: If Camila Vera is piloting, she can still attack
        return []

    # Right, now create a list of possible attacks
    possible_attacks = []
    for weapon in attacker.get_weapons():
        if isinstance(weapon, Repair):
            possible_attacks.extend(get_possible_attacks_repair(board, weapon, attacker, attacker_pos))
        elif isinstance(weapon, TitanFist):
            possible_attacks.extend(get_possible_attacks_titan_fist(board, weapon, attacker, attacker_pos))
        elif isinstance(weapon, AerialBombs):
            possible_attacks.extend(get_possible_attacks_aerial_bombs(board, weapon, attacker, attacker_pos))
        elif isinstance(weapon, Artemis):
            possible_attacks.extend(get_possible_attacks_artemis(board, weapon, attacker, attacker_pos))
        elif isinstance(weapon, TaurusCannon):
            possible_attacks.extend(get_possible_attacks_taurus_cannon(board, weapon, attacker, attacker_pos))
        else:
            raise Exception("Do not know this type of weapon!")

    return possible_attacks


def get_possible_attacks_repair(board, weapon, attacker, attacker_pos):
    """Returns all possible repair attacks"""
    return [Attack(attacker=attacker.get_id(), weapon=weapon, vector=None)]


def get_directional_attack_vectors(board, weapon, attacker, attacker_pos):
    possible_attacks = []
    attacker_id = attacker.get_id()
    # This is a list of relative positions that can be pushed
    for vector in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        attacked_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
        if not board.in_bounds(attacked_pos):
            continue

        new_attack = Attack(attacker=attacker_id, weapon=weapon, vector=vector)
        possible_attacks.append(new_attack)

    return possible_attacks


def get_possible_attacks_titan_fist(board, weapon, attacker, attacker_pos):
    return get_directional_attack_vectors(board, weapon, attacker, attacker_pos)


def get_possible_attacks_aerial_bombs(board, weapon, attacker, attacker_pos):
    possible_attacks = []
    attacker_id = attacker.get_id()

    rnge = weapon.get_full_range()
    vectors = []
    for r in rnge:
        vectors.extend([(r, 0), (-r, 0), (0, r), (0, -r)])

    for vector in vectors:
        landing_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
        if not board.in_bounds(landing_pos):
            continue

        if board[landing_pos].has_object():
            continue

        new_attack = Attack(attacker=attacker_id, weapon=weapon, vector=vector)
        possible_attacks.append(new_attack)

    return possible_attacks


def get_possible_attacks_artemis(board, weapon, attacker, attacker_pos):
    possible_attacks = []
    attacker_pos_x = attacker_pos[0]
    attacker_pos_y = attacker_pos[1]

    vectors = [(attacker_pos_x, y) for y in itertools.chain(range(0, attacker_pos_y - 1),
                                                            range(attacker_pos_y + 2, board.BOARD_Y_SIZE))]

    vectors.extend([(x, attacker_pos_y) for x in itertools.chain(range(0, attacker_pos_x - 1),
                                                                 range(attacker_pos_x + 2, board.BOARD_X_SIZE))])

    attacker_id = attacker.get_id()
    for vector in vectors:
        possible_attacks.append(Attack(attacker=attacker_id, weapon=weapon,
                                       vector=(vector[0] - attacker_pos_x, vector[1] - attacker_pos_y)))

    return possible_attacks


def get_possible_attacks_taurus_cannon(board, weapon, attacker, attacker_pos):
    return get_directional_attack_vectors(board, weapon, attacker, attacker_pos)
