import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import AcidPool, GroundTile
from src.game_objects.vek import Firefly, Hornet
from src.game_objects.weapons.push import Push


@pytest.mark.parametrize("obj",
                         [(CombatMech()),
                          (JetMech()),
                          (Firefly()),
                          (Hornet())])
def test_acid_mech_non_flying(obj):
    board = Board()
    pool_pos = (0, 0)
    obj_pos = (1, 0)
    direction = (-1, 0)
    board[obj_pos].set_object(obj)
    board[pool_pos] = AcidPool(_object=None)

    attack = Attack(attacker=obj_pos, weapon=Push(), vector=direction)
    apply_attack(board, attack)

    tile = board[pool_pos]
    obj = tile.get_object()
    assert obj.is_on_acid() is True
    assert isinstance(tile, GroundTile)


def test_acid_pool_exceptions():
    board = Board()
    pool_pos = (0, 0)

    obj = CombatMech()
    board[pool_pos] = AcidPool(_object=obj)

    with pytest.raises(Exception) as context:
        board[pool_pos].repair()

    assert "Repairing AcidPool not possible. Convert to GroundTile and then repair object" \
           in str(context.value)
