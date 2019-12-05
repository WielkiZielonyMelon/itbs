from src.game_objects.tiles.tile import GroundTile, WaterTile, AcidTile, LavaTile, ForestFireTile


def is_tile_damageable(tile):
    if isinstance(tile, (GroundTile, WaterTile, AcidTile, LavaTile, ForestFireTile)):
        return False
    else:
        return True
