import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, CannonMech
from src.game_objects.vek import Firefly, Hornet, Leaper, AlphaFirefly, AlphaScarab
from src.game_objects.weapons.accelerating_thorax import EnhancedThorax
from src.game_objects.weapons.spitting_glands import AlphaSpittingGlands
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("webbed_obj",
                         [Firefly,
                          Hornet])
@pytest.mark.parametrize("attacker,        weapon,          attack_vector, webber_pos, webbed_pos",
                         [(AlphaFirefly(), EnhancedThorax(),              (0, 1), (0, 3), (1, 3)),
                          (AlphaScarab(),  AlphaSpittingGlands(),         (0, 2), (0, 3), (1, 3)),
                          (CannonMech(),   TaurusCannon(damage_plus_1_upgrade_1=True,
                                                        damage_plus_1_upgrade_2=True),
                                                                          (0, 1), (0, 3), (1, 3)),
                          (CombatMech(),   TitanFist(damage_plus_2=True), (0, 1), (0, 2), (1, 2))])
def test_weapon_kills_webbed(webbed_obj, attacker, weapon, attack_vector, webber_pos, webbed_pos):
    board = Board()

    webber = Leaper()
    board[webber_pos].set_object(webber)
    board.apply_web(webber_pos, webbed_pos)

    attacker_pos = (1, 1)
    board[attacker_pos].set_object(attacker)
    attack = Attack(attacker=attacker.get_id(), weapon=weapon,
                    vector=attack_vector)

    webbed_obj = webbed_obj()
    board[webbed_pos].set_object(webbed_obj)

    board.fill_object_position_cache()

    assert board.is_position_webbed(webbed_pos) is True
    apply_attack(board, attack)
    assert board.is_position_webbed(webbed_pos) is False
    assert board[webbed_pos].get_object() is None

