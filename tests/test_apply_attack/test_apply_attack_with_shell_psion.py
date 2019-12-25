import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.building import CivilianBuilding
from src.game_objects.mech import CombatMech, ArtilleryMech, JetMech, CannonMech
from src.game_objects.vek import Firefly, Scarab, Hornet, ShellPsion
from src.game_objects.weapons.accelerating_thorax import AcceleratingThorax
from src.game_objects.weapons.aerial_bombs import AerialBombs
from src.game_objects.weapons.artemis import Artemis
from src.game_objects.weapons.spitting_glands import SpittingGlands
from src.game_objects.weapons.stinger import Stinger
from src.game_objects.weapons.taurus_cannon import TaurusCannon
from src.game_objects.weapons.titan_fist import TitanFist


@pytest.mark.parametrize("obj",
                         [Firefly])
@pytest.mark.parametrize("attacker,         weapon,               vector, obj_pos, exp_dmg",
                         [(Firefly(),       AcceleratingThorax(), (0, 1), (1, 3),  0),
                          (ArtilleryMech(), Artemis(),            (0, 2), (1, 3),  0),
                          (JetMech(),       AerialBombs(),        (0, 2), (1, 2),  0),
                          (Scarab(),        SpittingGlands(),     (0, 2), (1, 3),  0),
                          (Hornet(),        Stinger(),            (0, 1), (1, 2),  0),
                          (CannonMech(),    TaurusCannon(),       (0, 1), (1, 3),  0),
                          (CombatMech(),    TitanFist(),          (0, 1), (1, 2),  1)])
def test_weapon_on_vek_with_shell_psion_present(obj, attacker, weapon, vector, obj_pos, exp_dmg):
    obj = obj()
    board = Board()

    attacker_pos = (1, 1)
    board[attacker_pos].set_object(attacker)
    attack = Attack(attacker=attacker.get_id(), weapon=weapon,
                    vector=vector)

    board[obj_pos].set_object(obj)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    apply_attack(board, attack)
    assert obj.get_health() + exp_dmg == obj.get_max_health()


@pytest.mark.parametrize("obj",
                         [CombatMech])
@pytest.mark.parametrize("attacker,         weapon,               vector, obj_pos, exp_dmg",
                         [(Firefly(),       AcceleratingThorax(), (0, 1), (1, 3),  1),
                          (ArtilleryMech(), Artemis(),            (0, 2), (1, 3),  1),
                          (JetMech(),       AerialBombs(),        (0, 2), (1, 2),  1),
                          (Scarab(),        SpittingGlands(),     (0, 2), (1, 3),  1),
                          (Hornet(),        Stinger(),            (0, 1), (1, 2),  1),
                          (CannonMech(),    TaurusCannon(),       (0, 1), (1, 3),  1),
                          (CombatMech(),    TitanFist(),          (0, 1), (1, 2),  2)])
def test_weapon_on_mech_with_shell_psion_present(obj, attacker, weapon, vector, obj_pos, exp_dmg):
    obj = obj()
    board = Board()

    attacker_pos = (1, 1)
    board[attacker_pos].set_object(attacker)
    attack = Attack(attacker=attacker.get_id(), weapon=weapon,
                    vector=vector)

    board[obj_pos].set_object(obj)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    apply_attack(board, attack)
    assert obj.get_health() + exp_dmg == obj.get_max_health()


@pytest.mark.parametrize("obj",
                         [CivilianBuilding])
@pytest.mark.parametrize("attacker,         weapon,               vector, obj_pos, exp_dmg",
                         [(Firefly(),       AcceleratingThorax(), (0, 1), (1, 3),  1),
                          (ArtilleryMech(), Artemis(),            (0, 2), (1, 3),  1),
                          (JetMech(),       AerialBombs(),        (0, 2), (1, 2),  1),
                          (Scarab(),        SpittingGlands(),     (0, 2), (1, 3),  1),
                          (Hornet(),        Stinger(),            (0, 1), (1, 2),  1),
                          (CannonMech(),    TaurusCannon(),       (0, 1), (1, 3),  1),
                          (CombatMech(),    TitanFist(),          (0, 1), (1, 2),  2)])
def test_weapon_on_building_with_shell_psion_present(obj, attacker, weapon, vector, obj_pos, exp_dmg):
    obj = obj(health=3)
    board = Board()

    attacker_pos = (1, 1)
    board[attacker_pos].set_object(attacker)
    attack = Attack(attacker=attacker.get_id(), weapon=weapon,
                    vector=vector)

    board[obj_pos].set_object(obj)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    apply_attack(board, attack)
    assert obj.get_health() + exp_dmg == obj.get_max_health()


@pytest.mark.parametrize("attacker,         weapon,               vector, obj_pos, exp_dmg",
                         [(Firefly(),       AcceleratingThorax(), (0, 1), (1, 3),  1),
                          (ArtilleryMech(), Artemis(),            (0, 2), (1, 3),  1),
                          (JetMech(),       AerialBombs(),        (0, 2), (1, 2),  1),
                          (Scarab(),        SpittingGlands(),     (0, 2), (1, 3),  1),
                          (Hornet(),        Stinger(),            (0, 1), (1, 2),  1),
                          (CannonMech(),    TaurusCannon(),       (0, 1), (1, 3),  1),
                          (CombatMech(),    TitanFist(),          (0, 1), (1, 2),  2)])
def test_weapon_on_shell_psion(attacker, weapon, vector, obj_pos, exp_dmg):
    board = Board()

    attacker_pos = (1, 1)
    board[attacker_pos].set_object(attacker)
    attack = Attack(attacker=attacker.get_id(), weapon=weapon,
                    vector=vector)

    obj = ShellPsion()
    board[obj_pos].set_object(obj)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    apply_attack(board, attack)
    assert obj.get_health() + exp_dmg == obj.get_max_health()
