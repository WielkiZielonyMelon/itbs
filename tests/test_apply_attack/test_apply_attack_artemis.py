import copy

import pytest

from src.apply_attack.apply_attack import apply_attack
from src.game_objects.attack import Attack
from src.game_objects.board import Board
from src.game_objects.mech import ArtilleryMech, CombatMech
from src.game_objects.tiles.tile import AcidTile, LavaTile, WaterTile, ChasmTile, IceTile, DamagedFrozenAcidTile
from src.game_objects.vek import Spiderling, BlastPsion, ShellPsion, Firefly
from src.game_objects.weapons.artemis import Artemis


def test_attack_spiderlings():
    board = Board()
    mech = ArtilleryMech()

    mech_pos = (1, 2)
    board[mech_pos].set_object(mech)

    spiderling_pos = [(5, 2), (6, 2), (4, 2), (5, 3), (5, 1)]
    after_attack_pos = [(7, 2), (3, 2), (5, 0), (5, 4)]
    orig_tiles = {}

    for pos in spiderling_pos:
        board[pos].set_object(Spiderling())

    for pos in spiderling_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])
    for pos in after_attack_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])

    attack = Attack(attacker=mech.get_id(), weapon=Artemis(), vector=(4, 0))

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 9
    for key, value in orig_tiles.items():
        assert original_tiles[key] == value

    for pos in spiderling_pos:
        assert not board[pos].has_object()

    for pos in after_attack_pos:
        obj = board[pos].get_object()
        assert isinstance(obj, Spiderling)
        assert obj.get_health() == obj.get_max_health()


def test_attack_spiderlings_with_blast_psion():
    board = Board()
    mech = ArtilleryMech()

    mech_pos = (1, 2)
    board[mech_pos].set_object(mech)

    psion0 = BlastPsion()
    psion0_pos = (7, 7)
    board[psion0_pos].set_object(psion0)
    exp_psion0_health = psion0.get_health()

    spiderling_pos = [(5, 2), (6, 2), (4, 2), (5, 3), (5, 1)]
    after_attack_pos = [(7, 2), (3, 2), (5, 0), (5, 4)]
    orig_tiles = {}

    for pos in spiderling_pos:
        board[pos].set_object(Spiderling())

    for pos in spiderling_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])
    for pos in after_attack_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])

    attack = Attack(attacker=mech.get_id(), weapon=Artemis(), vector=(4, 0))

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 9
    for key, value in orig_tiles.items():
        assert original_tiles[key] == value

    for pos in spiderling_pos:
        assert not board[pos].has_object()

    for pos in after_attack_pos:
        obj = board[pos].get_object()
        assert isinstance(obj, Spiderling)
        assert obj.get_health() == obj.get_max_health()

    assert exp_psion0_health == psion0.get_health()


@pytest.mark.parametrize("tile",
                         [(AcidTile(_object=None)),
                          (LavaTile(_object=None)),
                          (WaterTile(_object=None)),
                          (ChasmTile(_object=None))])
def test_attack_spiderlings_push_to_death_tile(tile):
    board = Board()
    mech = ArtilleryMech()

    mech_pos = (1, 2)
    board[mech_pos].set_object(mech)

    spiderling_pos = [(5, 2), (6, 2), (4, 2), (5, 3), (5, 1)]
    after_attack_pos = [(7, 2), (3, 2), (5, 0), (5, 4)]

    for pos in spiderling_pos:
        board[pos].set_object(Spiderling())

    for pos in after_attack_pos:
        board[pos] = tile

    orig_tiles = {}
    for pos in spiderling_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])
    for pos in after_attack_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])

    attack = Attack(attacker=mech.get_id(), weapon=Artemis(), vector=(4, 0))

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 9
    for key, value in orig_tiles.items():
        assert original_tiles[key] == value

    for pos in spiderling_pos:
        assert not board[pos].has_object()

    for pos in after_attack_pos:
        assert not board[pos].has_object()


@pytest.mark.parametrize("tile",
                         [(AcidTile(_object=None)),
                          (WaterTile(_object=None)),
                          (ChasmTile(_object=None))])
def test_attack_spiderlings_on_acid_push_to_death_tile(tile):
    board = Board()
    mech = ArtilleryMech()

    mech_pos = (1, 2)
    board[mech_pos].set_object(mech)

    spiderling_pos = [(5, 2), (6, 2), (4, 2), (5, 3), (5, 1)]
    after_attack_pos = [(7, 2), (3, 2), (5, 0), (5, 4)]

    for pos in spiderling_pos:
        spiderling = Spiderling()
        spiderling.set_acid()
        board[pos].set_object(spiderling)

    for pos in after_attack_pos:
        board[pos] = copy.copy(tile)

    orig_tiles = {}
    for pos in spiderling_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])
    for pos in after_attack_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])

    attack = Attack(attacker=mech.get_id(), weapon=Artemis(), vector=(4, 0))

    original_tiles = apply_attack(board, attack)
    assert len(original_tiles) == 9
    for key, value in orig_tiles.items():
        assert original_tiles[key] == value

    for pos in spiderling_pos:
        assert not board[pos].has_object()

    for pos in after_attack_pos:
        assert not board[pos].has_object()


@pytest.mark.parametrize("tile",
                         [(AcidTile(_object=None)),
                          (WaterTile(_object=None)),
                          (ChasmTile(_object=None))])
def test_attack_spiderlings_on_acid_blast_psion_push_to_death_tile(tile):
    board = Board()
    mech = ArtilleryMech()

    mech_pos = (1, 2)
    board[mech_pos].set_object(mech)

    psion0 = BlastPsion()
    psion0_pos = (7, 7)
    board[psion0_pos].set_object(psion0)
    exp_psion0_health = psion0.get_health()

    spiderling_pos = [(5, 2), (6, 2), (4, 2), (5, 3), (5, 1)]
    after_attack_pos = [(7, 2), (3, 2), (5, 0), (5, 4)]

    for pos in spiderling_pos:
        spiderling = Spiderling()
        spiderling.set_acid()
        board[pos] = IceTile(_object=spiderling)

    for pos in after_attack_pos:
        board[pos] = copy.copy(tile)

    orig_tiles = {}
    for pos in spiderling_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])
    for pos in after_attack_pos:
        orig_tiles[pos] = copy.deepcopy(board[pos])

    extra_pos = [(2, 2), (3, 1), (3, 3), (4, 4), (5, 5), (6, 4), (4, 0), (6, 0), (7, 1), (7, 3)]
    for pos in extra_pos:
        board[pos] = DamagedFrozenAcidTile(_object=None)
        orig_tiles[pos] = copy.deepcopy(board[pos])

    attack = Attack(attacker=mech.get_id(), weapon=Artemis(), vector=(4, 0))
    original_tiles = apply_attack(board, attack)

    assert len(original_tiles) == 19
    for key, value in orig_tiles.items():
        assert original_tiles[key] == value

    for pos in spiderling_pos:
        assert not board[pos].has_object()

    for pos in after_attack_pos:
        assert not board[pos].has_object()

    assert exp_psion0_health == psion0.get_health()

    for pos in extra_pos:
        assert isinstance(board[pos], AcidTile)

    for pos in spiderling_pos[1:]:
        assert isinstance(board[pos], WaterTile)

    assert isinstance(board[spiderling_pos[0]], DamagedFrozenAcidTile)


def test_artemis_shell_psion():
    board = Board()

    vek0_pos = (1, 1)
    vek0 = Firefly()
    board[vek0_pos].set_object(vek0)

    mech1_pos = (1, 3)
    mech1 = ArtilleryMech()
    board[mech1_pos].set_object(mech1)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -2)
    attack = Attack(attacker=mech1.get_id(), weapon=Artemis(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert vek0.get_health() == vek0.get_max_health()


def test_artemis_shell_psion_on_mech():
    board = Board()

    mech0_pos = (1, 1)
    mech0 = CombatMech()
    board[mech0_pos].set_object(mech0)

    mech1_pos = (1, 3)
    mech1 = ArtilleryMech()
    board[mech1_pos].set_object(mech1)

    shell_psion0_pos = (0, 0)
    shell_psion0 = ShellPsion()
    board[shell_psion0_pos].set_object(shell_psion0)

    attack_vector = (0, -2)
    attack = Attack(attacker=mech1.get_id(), weapon=Artemis(),
                    vector=attack_vector)
    apply_attack(board, attack)

    assert mech0.get_health() == mech0.get_max_health() - 1
