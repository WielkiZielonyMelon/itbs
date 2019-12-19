from queue import Queue


def get_possible_moves(board, obj):
    """Returns all possible moves for a player controlled object
    at given position"""
    if obj is None:
        return []

    if not obj.is_player_controlled():
        return []

    if obj.get_moves() == 0:
        return []

    possible_moves = []
    pos = board.find_object_position(obj)
    if pos is None:
        # Whooopsie, seems someone has died
        return []

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

        # Go north
        north = it[0][1] - 1
        new_pos = (it[0][0], north)
        if north >= 0 and new_pos not in possible_moves and \
                not board[new_pos].has_object():
            possible_moves.append(new_pos)
            q.put((new_pos, moves_left))
        # Go east
        east = it[0][0] + 1
        new_pos = (east, it[0][1])
        if east < board.BOARD_X_SIZE and new_pos not in possible_moves and \
                not board[new_pos].has_object():
            possible_moves.append(new_pos)
            q.put((new_pos, moves_left))
        # Go south
        south = it[0][1] + 1
        new_pos = (it[0][0], south)
        if south < board.BOARD_Y_SIZE and new_pos not in possible_moves and \
                not board[new_pos].has_object():
            possible_moves.append(new_pos)
            q.put((new_pos, moves_left))
        # Go west
        west = it[0][0] - 1
        new_pos = (west, it[0][1])
        if west >= 0 and new_pos not in possible_moves and \
                not board[new_pos].has_object():
            possible_moves.append(new_pos)
            q.put((new_pos, moves_left))

    return possible_moves
