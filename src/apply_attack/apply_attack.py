from src.game_objects.building import Building
from src.game_objects.mountain import Mountain
from src.game_objects.tiles.tile import AcidPool, \
    ForestTile, ForestFireTile, \
    AcidTile, DamagedFrozenAcidTile, FrozenAcidTile, \
    GroundTile, FireTile, \
    LavaTile, FrozenLavaTile, DamagedFrozenLavaTile, \
    WaterTile, IceTile, DamagedIceTile, ChasmTile, SandTile, TimePodTile
from src.game_objects.weapons.accelerating_thorax import EnhancedThorax, AcceleratingThorax
from src.game_objects.weapons.acid import Acid
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.burn import Burn
from src.game_objects.weapons.dash import Dash
from src.game_objects.weapons.drown import Drown
from src.game_objects.weapons.emerging import Emerging
from src.game_objects.weapons.freeze import Freeze
from src.game_objects.weapons.move import Move
from src.game_objects.weapons.push import Push
from src.game_objects.weapons.repair import Repair
from src.game_objects.weapons.set_on_fire import SetOnFire
from src.game_objects.weapons.spitting_glands import SpittingGlands, AlphaSpittingGlands
from src.game_objects.weapons.stinger import Stinger, LaunchingStinger, SuperStinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


def apply_attack(board, attack):
    attacker = attack.get_attacker()
    # If this is an id...
    if not isinstance(attacker, tuple):
        attacker_pos = board.find_object_id_position(attacker)
        if attacker_pos is None:
            return {}
        attacker = board[attacker_pos].get_object()
        # Nothing to do, attacker died
        if attacker.get_health() <= 0:
            return {}

        # Attacker cannot be found, probably removed from board
        if attacker_pos is None:
            return {}
        # If attacker is in liquid tile, there are no possible attacks... except move
        if board[attacker_pos].is_liquid() and not attacker.is_flying() \
                and not isinstance(attack.get_weapon(), Move):
            return {}

        # If attacker is in smoke, there is no possibility to attack
        if board[attacker_pos].has_smoke():
            # TODO: If Camila Vera is piloting, she can still attack
            return {}

    weapon = attack.get_weapon()
    if isinstance(weapon, Move):
        from src.apply_attack.apply_attack_move import apply_attack_move
        return apply_attack_move(board, attack)
    elif isinstance(weapon, TitanFist):
        from src.apply_attack.apply_attack_titan_fist \
            import apply_attack_titan_fist
        return apply_attack_titan_fist(board, attack)
    elif isinstance(weapon, AerialBombs):
        from src.apply_attack.apply_attack_aerial_bombs \
            import apply_attack_aerial_bombs
        apply_attack_aerial_bombs(board, attack)
    elif isinstance(weapon, TaurusCannon):
        from src.apply_attack.apply_attack_projectile_weapon \
            import apply_attack_projectile_weapon
        return apply_attack_projectile_weapon(board, attack, push=True)
    elif isinstance(weapon, (Artemis, SpittingGlands, AlphaSpittingGlands)):
        from src.apply_attack.apply_artillery_attack import apply_attack_artillery
        return apply_attack_artillery(board, attack)
    elif isinstance(weapon, (AcceleratingThorax, EnhancedThorax)):
        from src.apply_attack.apply_attack_projectile_weapon \
            import apply_attack_projectile_weapon
        return apply_attack_projectile_weapon(board, attack)
    elif isinstance(weapon, (Stinger, LaunchingStinger, SuperStinger)):
        from src.apply_attack.apply_attack_stinger import apply_attack_stinger
        return apply_attack_stinger(board, attack)
    elif isinstance(weapon, Push):
        from src.apply_attack.apply_attack_push import apply_attack_push
        return apply_attack_push(board, attack)
    elif isinstance(weapon, Dash):
        from src.apply_attack.apply_attack_dash import apply_attack_dash
        return apply_attack_dash(board, attack)
    elif isinstance(weapon, Drown):
        from src.apply_attack.apply_attack_drown import apply_attack_drown
        return apply_attack_drown(board, attack)
    elif isinstance(weapon, Emerging):
        from src.apply_attack.apply_attack_emerging import apply_attack_emerging
        return apply_attack_emerging(board, attack)
    elif isinstance(weapon, Burn):
        from src.apply_attack.apply_attack_burn import apply_attack_burn
        return apply_attack_burn(board, attack)
    elif isinstance(weapon, SetOnFire):
        from src.apply_attack.apply_attack_set_on_fire \
            import apply_attack_set_on_fire
        return apply_attack_set_on_fire(board, attack)
    elif isinstance(weapon, Freeze):
        from src.apply_attack.apply_attack_freeze import apply_attack_freeze
        apply_attack_freeze(board, attack)
    elif isinstance(weapon, Acid):
        from src.apply_attack.apply_attack_acid import apply_attack_acid
        apply_attack_acid(board, attack)
    elif isinstance(weapon, Repair):
        from src.apply_attack.apply_attack_repair import apply_attack_repair
        return apply_attack_repair(board, attack)
    else:
        raise Exception("Do not know weapon = " + str(weapon) + "!")


def acidify_tile(board, pos):
    """Converts the tile as if A.C.I.D. was applied to it."""

    # If object is frozen, do not care, continue applying acid
    obj = board[pos].get_object()
    has_smoke = board[pos].has_smoke()
    if obj is not None:
        if isinstance(obj, Mountain):
            # Acid cannot be applied to mountain tiles
            return
        elif isinstance(obj, Building):
            # AcidPool appears under building
            board[pos] = AcidPool(_object=obj)
            if has_smoke:
                board[pos].set_smoke()
            return
        # All other objects receive acid, nothing should happen to tile
        obj.set_acid()
        return

    tile = board[pos]
    if isinstance(tile, AcidTile) or isinstance(tile, FrozenAcidTile) \
            or isinstance(tile, DamagedFrozenAcidTile):
        # Nothing has to be done, this tile is already acided
        pass
    # Chasm tiles cannot be acided
    elif isinstance(tile, ChasmTile):
        pass
    elif isinstance(tile, WaterTile):
        board[pos] = AcidTile(_object=None)
    elif isinstance(tile, IceTile):
        board[pos] = FrozenAcidTile(_object=None)
    elif isinstance(tile, DamagedIceTile):
        board[pos] = DamagedFrozenAcidTile(_object=None)
    elif isinstance(tile, LavaTile):
        # TODO: Not sure about this, needs verification
        board[pos] = AcidTile(_object=None)
    elif isinstance(tile, DamagedFrozenLavaTile):
        # TODO: Not sure about this, needs verification
        board[pos] = DamagedFrozenAcidTile(_object=None)
    elif isinstance(tile, LavaTile):
        # TODO: Not sure about this, needs verification
        board[pos] = AcidTile(_object=None)
    else:
        board[pos] = AcidPool(_object=None)

    if has_smoke:
        board[pos].set_smoke()


def fire_tile(board, pos):
    obj = board[pos].get_object()
    tile = board[pos]
    if isinstance(tile, (FrozenAcidTile, DamagedFrozenAcidTile)):
        board[pos] = AcidTile(_object=obj)
    elif isinstance(tile, (FrozenLavaTile, DamagedFrozenLavaTile)):
        board[pos] = LavaTile(_object=obj)
    elif isinstance(tile, (IceTile, DamagedIceTile)):
        board[pos] = WaterTile(_object=obj)
    elif isinstance(tile, GroundTile):
        board[pos] = FireTile(_object=obj)
    elif isinstance(tile, ForestTile):
        board[pos] = ForestFireTile(_object=obj)

    board[pos].set_fire()


def freeze_tile(board, pos):
    obj = board[pos].get_object()
    tile = board[pos]
    if isinstance(tile, DamagedFrozenAcidTile):
        board[pos] = FrozenAcidTile(_object=obj)
    elif isinstance(tile, AcidTile):
        board[pos] = FrozenAcidTile(_object=obj)
    elif isinstance(tile, ForestFireTile):
        board[pos] = ForestTile(_object=obj)
    elif isinstance(tile, FireTile):
        board[pos] = GroundTile(_object=obj)
    elif isinstance(tile, LavaTile) or \
            isinstance(tile, DamagedFrozenLavaTile):
        board[pos] = FrozenLavaTile(_object=obj)


def damage_tile(board, pos):
    obj = board[pos].get_object()
    tile = board[pos]
    if isinstance(tile, IceTile):
        board[pos] = DamagedIceTile(_object=obj)
    elif isinstance(tile, DamagedIceTile):
        board[pos] = WaterTile(_object=obj)
    elif isinstance(tile, FrozenAcidTile):
        board[pos] = DamagedFrozenAcidTile(_object=obj)
    elif isinstance(tile, DamagedFrozenAcidTile):
        board[pos] = AcidTile(_object=obj)
    elif isinstance(tile, FrozenLavaTile):
        board[pos] = DamagedFrozenLavaTile(_object=obj)
    elif isinstance(tile, DamagedFrozenLavaTile):
        board[pos] = LavaTile(_object=obj)
    elif isinstance(tile, ForestTile):
        board[pos] = ForestFireTile(_object=obj)
    elif isinstance(tile, SandTile):
        board[pos] = GroundTile(_object=obj)
        board[pos].set_smoke()
    elif isinstance(tile, TimePodTile):
        board[pos] = GroundTile(_object=obj)
        board.set_time_pod_destroyed()


def repair_tile(board, pos):
    obj = board[pos].get_object()
    tile = board[pos]
    if isinstance(tile, FireTile):
        board[pos] = GroundTile(_object=obj)
    elif isinstance(tile, ForestFireTile):
        board[pos] = ForestTile(_object=obj)


def smoke_tile(board, pos):
    # TODO: Smoking a tile repairs it?
    repair_tile(board, pos)
    board[pos].set_smoke()
