# TODO: Should be part of Board

def find_object_position(board, _object):
    _id = _object.get_id()
    return find_object_id_position(board, _id)


def find_object_id_position(board, _id):
    for x in range(0, board.BOARD_MAX_X_SIZE):
        for y in range(0, board.BOARD_MAX_Y_SIZE):
            obj = board[(x, y)].get_object()
            if obj is not None and _id == obj.get_id():
                return x, y

    return None
