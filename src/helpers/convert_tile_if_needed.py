from src.game_objects.tiles.tile import AcidPool, GroundTile, AcidTile, WaterTile, ForestFireTile, FireTile, LavaTile, \
    ForestTile


def convert_tile_if_needed(board, pos):
    """Convert tile, but do not kill an object.

    Converts tile depending on the state of an object and apply various state to object.
    For example, if object is on fire, it will convert ForestTile to ForestFireTile. IT WILL NOT KILL AN OBJECT.
    To kill an object call kill_object_if_possible"""
    obj = board[pos].get_object()
    if obj is None:
        return

    tile = board[pos]
    has_smoke = tile.has_smoke()

    if isinstance(tile, AcidPool):
        obj.set_acid()
        board[pos] = GroundTile(_object=obj)
    elif isinstance(tile, AcidTile) and not obj.is_flying():
        obj.set_acid()
    elif obj.is_on_acid():
        if isinstance(tile, WaterTile):
            board[pos] = AcidTile(_object=obj)
    elif obj.is_on_fire():
        if isinstance(tile, (WaterTile, AcidTile)) and not obj.is_flying():
            obj.clear_fire()
        elif isinstance(tile, ForestTile):
            board[pos] = ForestFireTile(_object=obj)
    elif obj.is_frozen():
        if isinstance(tile, WaterTile) and obj.is_massive():
            obj.thaw()
        elif isinstance(board, (ForestFireTile, FireTile)):
            obj.thaw()
            obj.set_fire()
        elif isinstance(tile, LavaTile) and obj.is_massive():
            obj.thaw()
            obj.set_fire()
    elif not obj.is_flying() and isinstance(tile, (ForestFireTile, FireTile, LavaTile)):
        obj.set_fire()

    if has_smoke:
        board[pos].set_smoke()
