import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import CombatMech, JetMech
from src.game_objects.tiles.tile import GroundTile, WaterTile, ForestTile, FrozenAcidTile, IceTile, \
    DamagedFrozenAcidTile, DamagedIceTile, AcidTile
from src.game_objects.vek import Firefly, Hornet, Spiderling, BlastPsion, ShellPsion, Scarab
from src.game_objects.weapons.drown import Drown


@pytest.mark.parametrize("obj",
                         [None,
                          (CombatMech()),
                          (JetMech()),
                          (Hornet())])
def test_drown_object(obj):
    board = Board()

    drown_pos = (0, 0)

    board[drown_pos] = GroundTile(_object=obj)
    orig_tile = copy.deepcopy(board[drown_pos])

    attack = Attack(attacker=drown_pos, weapon=Drown(), vector=None)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[drown_pos]

    tile = board[drown_pos]
    assert isinstance(tile, WaterTile)
    assert board[drown_pos].get_object() == obj


def test_drown_firefly():
    board = Board()
    hornet = Firefly()

    drown_pos = (0, 0)

    board[drown_pos] = GroundTile(_object=hornet)
    orig_tile = copy.deepcopy(board[drown_pos])

    board.fill_object_position_cache()
    attack = Attack(attacker=drown_pos, weapon=Drown(), vector=None)
    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 1
    assert orig_tile == original_tiles[drown_pos]

    tile = board[drown_pos]
    assert isinstance(tile, WaterTile)
    assert board[drown_pos].get_object() is None


def test_drown_exploding_vek_chain_reaction():
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
    vek0_attack = Attack(attacker=spiderling0_pos, weapon=Drown(),
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
    assert isinstance(board[spiderling0_pos], WaterTile)
    assert isinstance(board[(3, 1)], DamagedFrozenAcidTile)
    assert isinstance(board[spiderling1_pos], WaterTile)
    assert isinstance(board[(4, 1)], AcidTile)
    assert isinstance(board[spiderling2_pos], AcidTile)
    assert isinstance(board[(5, 1)], DamagedIceTile)
    assert isinstance(board[spiderling3_pos], WaterTile)
    assert isinstance(board[(6, 1)], WaterTile)


@pytest.mark.parametrize("obj",
                         [(Firefly()),
                          (Scarab())])
def test_drown_on_sinkable_object_with_shell_psion_present(obj):
    board = Board()

    obj_pos = (1, 1)
    board[obj_pos].set_object(obj)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    board.fill_object_position_cache()
    attack = Attack(attacker=obj_pos, weapon=Drown(),
                    vector=None)
    apply_attack(board, attack)

    obj = board[obj_pos].get_object()
    assert obj is None


@pytest.mark.parametrize("obj",
                         [(Hornet()),
                          (CombatMech())])
def test_drown_on_non_sinkable_object_with_shell_psion_present(obj):
    board = Board()

    obj_pos = (1, 1)
    board[obj_pos].set_object(obj)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack = Attack(attacker=obj_pos, weapon=Drown(),
                    vector=None)
    apply_attack(board, attack)

    obj = board[obj_pos].get_object()
    assert obj.get_health() == obj.get_max_health()


@pytest.mark.parametrize("obj",
                         [(ShellPsion()),
                          (BlastPsion())])
def test_drown_on_psion(obj):
    board = Board()

    shell_psion0_pos = (0, 0)
    board[shell_psion0_pos].set_object(obj)

    attack = Attack(attacker=shell_psion0_pos, weapon=Drown(),
                    vector=None)
    apply_attack(board, attack)

    obj = board[shell_psion0_pos].get_object()
    assert obj.get_health() == obj.get_max_health()
