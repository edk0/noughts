from noughts import *

def test_rotation():
    b1 = Board('xxx------')
    b2 = Board('--x--x--x')
    rotations = set(b1.rotations())
    assert b2 in rotations

def test_symmetry():
    b1 = Board('-x-xxx-x-')
    assert len(list(b1.symmetries())) == 8

def test_winners():
    b1 = Board('xxx------')
    assert b1.winner == Tile.X
    b2 = Board('o---o---o')
    assert b2.winner == Tile.O
    b3 = Board('x--------')
    assert b3.winner is None

def test_uniqueness():
    b1 = Board('x-x------')
    b1_um = b1.unique_moves(Tile.O)
    assert len(b1_um) == len(set(b1_um)), "elements not unique"
    m1 = Move(b1, 0, 1, Tile.O)
    m2 = Move(b1, 2, 1, Tile.O)
    assert (m1 in b1_um) ^ (m2 in b1_um), "there should be exactly one of these equivalent moves"

def test_gameplay():
    b1 = Board('xx--o----')
    b2 = b1.make_best_move().board
    assert b2 == Board('xxo-o----')

    # the AI should always force a draw against itself
    b3 = Board('')
    while b3.spaces:
        b3 = b3.make_best_move().board
    assert b3.spaces == 0 and b3.winner == None
