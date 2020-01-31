from queue import Queue


def get_possible_moves(board, obj):
    """Returns all possible moves for a player controlled object
    at given position.

    If provided obj is None, exception will be risen"""

    # Check if object is still present on board, if not, return empty array of possible moves
    pos = board.find_object_position(obj)
    possible_moves = []
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
            if board.in_bounds(new_pos) and not board[new_pos].has_object() and new_pos not in possible_moves:
                possible_moves.append(new_pos)
                q.put((new_pos, moves_left))

    return possible_moves
