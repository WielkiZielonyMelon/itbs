from src.game_objects.attack import Attack
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


def get_possible_attacks(board, obj):
    """Return a list of possible attacks."""
    # Can't get any possible attacks if there is no object
    if obj is None:
        return []

    # I will not list attacks for an object that is not player controlled
    if not obj.is_player_controlled():
        return []

    # No weapons? This is straightforward
    if not obj.get_weapons():
        return []

    # This object is probably dead
    if obj.get_health() <= 0:
        return []

    # Get attackers position, that still might be removed from the board
    attacker_pos = board.find_object_position(obj)
    if attacker_pos is None:
        # Whoopsie, someone died
        return []

    # If attacker is in liquid tile, there are no possible attacks
    if board[attacker_pos].is_liquid() and not obj.is_flying():
        return []

    # If attacker is in smoke, there is no possibility to attack
    if board[attacker_pos].has_smoke():
        # TODO: If Camila Vera is piloting, she can still attack
        return []

    # Right, now create a list of possible attacks
    possible_attacks = []
    for weapon in obj.get_weapons():
        if isinstance(weapon, Repair):
            possible_attacks.extend(get_possible_attacks_repair(board, weapon, attacker_pos))
        elif isinstance(weapon, TitanFist):
            possible_attacks.extend(get_possible_attacks_titan_fist(board, weapon, attacker_pos))
        elif isinstance(weapon, AerialBombs):
            possible_attacks.extend(get_possible_attacks_aerial_bombs(board, weapon, attacker_pos))
        elif isinstance(weapon, Artemis):
            possible_attacks.extend(get_possible_attacks_artemis(board, weapon, attacker_pos))
        elif isinstance(weapon, TaurusCannon):
            possible_attacks.extend(get_possible_attacks_taurus_cannon(board, weapon, attacker_pos))
        else:
            raise Exception("Do not know this type of weapon!")

    return possible_attacks


def get_possible_attacks_repair(board, weapon, attacker_pos):
    """Returns all possible repair attacks"""
    return [Attack(attacker=board[attacker_pos].get_object().get_id(),
                   weapon=weapon, vector=None)]


def get_directional_attack_vectors(board, weapon, attacker_pos):
    possible_attacks = []
    # This is a list of relative positions that can be pushed
    for vector in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        attacked_pos = (attacker_pos[0] + vector[0], attacker_pos[1] + vector[1])
        if not board.in_bounds(attacked_pos):
            continue

        new_attack = Attack(attacker=board[attacker_pos].get_object().get_id(),
                            weapon=weapon, vector=vector)
        possible_attacks.append(new_attack)

    return possible_attacks


def get_possible_attacks_titan_fist(board, weapon, attacker_pos):
    return get_directional_attack_vectors(board, weapon, attacker_pos)


def get_possible_attacks_aerial_bombs(board, weapon, attacker_pos):
    possible_attacks = []
    attacker = board[attacker_pos].get_object()

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

        new_attack = Attack(attacker=attacker.get_id(), weapon=weapon, vector=vector)
        possible_attacks.append(new_attack)

    return possible_attacks


def get_possible_attacks_artemis(board, weapon, attacker_pos):
    possible_attacks = []
    attacker = board[attacker_pos].get_object()
    vectors = []

    candidate = set((attacker_pos[0], y) for y in range(0, board.BOARD_MAX_Y_SIZE))
    # Remove object position itself and nearest tiles
    candidate.discard(attacker_pos)
    candidate.discard((attacker_pos[0], attacker_pos[1] + 1))
    candidate.discard((attacker_pos[0], attacker_pos[1] - 1))
    vectors.extend(candidate)

    candidate = set((x, attacker_pos[1]) for x in range(0, board.BOARD_MAX_X_SIZE))
    # Remove object position itself and nearest tiles
    candidate.discard(attacker_pos)
    candidate.discard((attacker_pos[0] + 1, attacker_pos[1]))
    candidate.discard((attacker_pos[0] - 1, attacker_pos[1]))
    vectors.extend(candidate)

    for vector in vectors:
        possible_attacks.append(Attack(attacker=attacker.get_id(), weapon=weapon,
                                       vector=(vector[0] - attacker_pos[0], vector[1] - attacker_pos[1])))

    return possible_attacks


def get_possible_attacks_taurus_cannon(board, weapon, attacker_pos):
    return get_directional_attack_vectors(board, weapon, attacker_pos)
