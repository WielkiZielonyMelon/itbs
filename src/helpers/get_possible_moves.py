from queue import Queue


def get_possible_moves(board, pos):
    """Returns all possible moves for a player controlled object
    at given position.

    If provided obj is None, exception will be risen"""

    obj = board[pos].get_object()
    if board[pos].get_web() is not None:
        return []
    # Holder for visited moves
    possible_moves = []
    # Holder for position that were visited (however not possible to move there)
    visited = []
    # Queue hold a tuple, current player controlled object position
    # and how many moves are left from that position
    q = Queue()
    moves_left = obj.get_moves()
    q.put((pos, moves_left))

    while not q.empty():
        it = q.get()

        moves_left = it[1]
        if moves_left <= 0:
            continue
        moves_left -= 1

        pos_x = it[0][0]
        pos_y = it[0][1]

        #              West     East    South    North
        for vector in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (pos_x + vector[0], pos_y + vector[1])
            if board.in_bounds(new_pos) and new_pos not in possible_moves:
                obj = board[new_pos].get_object()
                if obj is None:
                    possible_moves.append(new_pos)
                    q.put((new_pos, moves_left))
                elif new_pos not in visited and obj.is_player_controlled():
                    visited.append(new_pos)
                    q.put((new_pos, moves_left))

    return possible_moves
