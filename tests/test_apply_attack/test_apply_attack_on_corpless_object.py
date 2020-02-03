import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech, ArtilleryMech, JetMech, CannonMech
from src.game_objects.vek import Firefly, Scarab, Hornet
from src.game_objects.weapons.accelerating_thorax import AcceleratingThorax
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.spitting_glands import SpittingGlands
from src.game_objects.weapons.stinger import Stinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("obj",
                         [Firefly,
                          Hornet,
                          Scarab])
@pytest.mark.parametrize("attacker,         weapon,               vector, obj_pos",
                         [(Firefly(),       AcceleratingThorax(), (0, 1), (1, 3)),
                          (ArtilleryMech(), Artemis(),            (0, 2), (1, 3)),
                          (JetMech(),       AerialBombs(),        (0, 2), (1, 2)),
                          (Scarab(),        SpittingGlands(),     (0, 2), (1, 3)),
                          (Hornet(),        Stinger(),            (0, 1), (1, 2)),
                          (CannonMech(),    TaurusCannon(),       (0, 1), (1, 3)),
                          (CombatMech(),    TitanFist(),          (0, 1), (1, 2))])
def test_weapon_on_corpseless_object(obj, attacker, weapon, vector, obj_pos):
    obj = obj()
    board = Board()

    attacker_pos = (1, 1)
    board[attacker_pos].set_object(attacker)
    attack = Attack(attacker=attacker.get_id(), weapon=weapon,
                    vector=vector)

    obj._health = 1
    board[obj_pos].set_object(obj)

    board.fill_object_position_cache()
    apply_attack(board, attack)
    assert obj.get_health() <= 0
    assert board[obj_pos].get_object() is None
