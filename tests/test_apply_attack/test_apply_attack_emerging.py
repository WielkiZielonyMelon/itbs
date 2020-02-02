import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech
from src.game_objects.tiles.tile import ForestTile, FrozenAcidTile, IceTile, DamagedFrozenAcidTile, DamagedIceTile, \
    AcidTile, WaterTile
from src.game_objects.vek import Emerged, Firefly, Spiderling, BlastPsion, ShellPsion
from src.game_objects.weapons.emerging import Emerging


def test_apply_attack_emerging():
    board = Board()

    emerge_pos = (1, 1)
    orig_tile = copy.deepcopy(board[emerge_pos])
    attack = Attack(attacker=emerge_pos, weapon=Emerging(), vector=None)

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[emerge_pos]
    obj = board[emerge_pos].get_object()
    assert isinstance(obj, Emerged)


def test_apply_attack_emerging_on_mech():
    board = Board()
    obj = CombatMech()

    emerge_pos = (1, 1)
    board[emerge_pos].set_object(obj)
    orig_tile = copy.deepcopy(board[emerge_pos])
    exp_obj_health = obj.get_health() - 1
    attack = Attack(attacker=emerge_pos, weapon=Emerging(), vector=None)

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[emerge_pos]
    obj = board[emerge_pos].get_object()
    assert obj.get_health() == exp_obj_health


def test_emerging_attack_exploding_vek_chain_reaction():
    board = Board()

    vek0 = Firefly()
    vek0_pos = (2, 0)
    board[vek0_pos] = ForestTile(_object=vek0)

    spiderling0 = Spiderling()
    spiderling0_pos = (3, 0)
    board[spiderling0_pos] = FrozenAcidTile(_object=spiderling0)
    board[(3, 1)] = FrozenAcidTile(_object=None)

    spiderling1 = Spiderling()
    spiderling1_pos = (4, 0)
    board[spiderling1_pos] = IceTile(_object=spiderling1)
    board[(4, 1)] = DamagedFrozenAcidTile(_object=None)

    spiderling2 = Spiderling()
    spiderling2_pos = (5, 0)
    board[spiderling2_pos] = DamagedFrozenAcidTile(_object=spiderling2)
    board[(5, 1)] = IceTile(_object=None)

    spiderling3 = Spiderling()
    spiderling3_pos = (6, 0)
    board[spiderling3_pos] = DamagedIceTile(_object=spiderling3)
    board[(6, 1)] = DamagedIceTile(_object=None)

    psion1 = BlastPsion()
    psion1_pos = (1, 0)
    board[psion1_pos].set_object(psion1)

    exp_vek0_health = vek0.get_health() - 1

    orig_tile20 = copy.deepcopy(board[vek0_pos])
    orig_tile30 = copy.deepcopy(board[spiderling0_pos])
    orig_tile31 = copy.deepcopy(board[(3, 1)])
    orig_tile40 = copy.deepcopy(board[spiderling1_pos])
    orig_tile41 = copy.deepcopy(board[(4, 1)])
    orig_tile50 = copy.deepcopy(board[spiderling2_pos])
    orig_tile51 = copy.deepcopy(board[(5, 1)])
    orig_tile60 = copy.deepcopy(board[spiderling3_pos])
    orig_tile61 = copy.deepcopy(board[(6, 1)])

    board.fill_object_position_cache()
    vek0_attack = Attack(attacker=spiderling0_pos, weapon=Emerging(),
                         vector=None)

    original_tiles = apply_attack(board, vek0_attack)
    assert len(original_tiles) == 9

    assert orig_tile20 == original_tiles[vek0_pos]
    assert orig_tile30 == original_tiles[spiderling0_pos]
    assert orig_tile31 == original_tiles[(3, 1)]
    assert orig_tile40 == original_tiles[spiderling1_pos]
    assert orig_tile41 == original_tiles[(4, 1)]
    assert orig_tile50 == original_tiles[spiderling2_pos]
    assert orig_tile51 == original_tiles[(5, 1)]
    assert orig_tile60 == original_tiles[spiderling3_pos]
    assert orig_tile61 == original_tiles[(6, 1)]

    assert board[spiderling0_pos].get_object() is None
    assert board[psion1_pos].get_object() == psion1
    assert board[vek0_pos].get_object() == vek0
    assert exp_vek0_health == vek0.get_health()
    assert isinstance(board[spiderling0_pos], DamagedFrozenAcidTile)
    assert isinstance(board[(3, 1)], DamagedFrozenAcidTile)
    assert isinstance(board[spiderling1_pos], WaterTile)
    assert isinstance(board[(4, 1)], AcidTile)
    assert isinstance(board[spiderling2_pos], AcidTile)
    assert isinstance(board[(5, 1)], DamagedIceTile)
    assert isinstance(board[spiderling3_pos], WaterTile)
    assert isinstance(board[(6, 1)], WaterTile)


def test_emerging_shell_psion_on_psion():
    board = Board()

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack = Attack(attacker=shell_psion0_pos, weapon=Emerging(),
                    vector=None)
    apply_attack(board, attack)

    assert shell_psion0.get_health() == shell_psion0.get_max_health() - 1


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (CombatMech())])
def test_emerging_on_object_with_shell_psion_present(obj):
    board = Board()

    psion0_pos = (0, 0)
    psion0 = ShellPsion()
    board[psion0_pos].set_object(psion0)

    obj0_pos = (1, 3)
    obj0 = obj
    board[obj0_pos].set_object(obj0)

    attack = Attack(attacker=obj0_pos, weapon=Emerging(),
                    vector=None)

    apply_attack(board, attack)
    assert obj0.get_health() + 1 == obj0.get_max_health()


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (CombatMech())])
def test_emerging_on_shielded_object(obj):
    board = Board()

    obj0_pos = (1, 3)
    obj0 = obj
    obj0.set_shield()
    board[obj0_pos].set_object(obj0)

    attack = Attack(attacker=obj0_pos, weapon=Emerging(),
                    vector=None)

    apply_attack(board, attack)
    assert obj0.get_health() == obj0.get_max_health()
    assert not obj0.is_shielded()
