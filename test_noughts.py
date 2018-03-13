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
