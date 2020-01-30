from src.game_objects.tiles.tile import GroundTile, WaterTile, AcidTile, LavaTile, ForestFireTile, FireTile


def is_tile_damageable(tile):
    if isinstance(tile, (GroundTile, WaterTile, AcidTile, LavaTile, ForestFireTile, FireTile)):
        return False
    else:
        return True
