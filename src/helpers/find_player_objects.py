#TODO: Should be part of board

def find_player_objects(board):
    player_controlled_objects = []
    for x in range(0, board.BOARD_MAX_X_SIZE):
        for y in range(0, board.BOARD_MAX_Y_SIZE):
            obj = board[(x, y)].get_object()
            if obj is not None and obj.is_player_controlled():
                player_controlled_objects.append((x, y))

    return player_controlled_objects