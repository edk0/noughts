import clize
import enum


class Tile(enum.Enum):
    EMPTY = ' '
    X = 'x'
    O = 'o'


class Board:
    """
    A game board. This is immutable; .replace() makes a copy.
    """

    def __init__(self, board=None):
        if isinstance(board, tuple):
            self._tiles = board
            return
        self._tiles = ((Tile.EMPTY,) * 3,) * 3
        if isinstance(board, str):
            for i, c in enumerate(board):
                if c not in 'xo':
                    continue
                self._tiles = self._replace(self._tiles, i % 3, i // 3, Tile(c))

    @classmethod
    def _replace(cls, tiles, x, y, value):
        return tuple(
            tuple(value if x_ == x and y_ == y else tiles[y_][x_]
                  for x_ in range(3))
            for y_ in range(3))

    def replace(self, x, y, value):
        return type(self)(self._replace(self._tiles, x, y, value))

    def moves(self, v):
        if v is None:
            v = self.next
        for x in range(3):
            for y in range(3):
                if self[x,y] != Tile.EMPTY:
                    continue
                yield Move(self, x, y, v)

    def unique_moves(self, v):
        move_pool = set(self.moves(v))
        moves = set()
        syms = self.symmetries()
        while move_pool:
            m = move_pool.pop()
            rotations = list(m.rotations())
            rm = set(rotations[i] for i in syms)
            move_pool -= rm
            moves.add(m)
        return moves

    def make_best_move(self):
        movelist = [(negamax(m), m) for m in self.unique_moves(None)]
        if len(movelist) < 1:
            raise ValueError("no moves left")
        movelist.sort(key=lambda x: x[0])
        return movelist[-1][1]

    @property
    def spaces(self):
        return len([True for x in range(3) for y in range(3) if self[x,y] == Tile.EMPTY])

    @property
    def next(self):
        return Tile.X if self.spaces % 2 == 1 else Tile.O

    def __getitem__(self, k):
        x, y = k
        return self._tiles[y][x]

    def _rotate(self):
        return type(self)(tuple(
            tuple(self[2-y, x] for x in range(3))
            for y in range(3)))

    def _mirror(self):
        return type(self)(tuple(
            tuple(self[2-x, y] for x in range(3))
            for y in range(3)))

    def rotations(self):
        x = self
        for _ in range(4):
            yield x
            yield x._mirror()
            x = x._rotate()

    def symmetries(self):
        return [n for n, v in enumerate(self.rotations()) if v == self]

    @property
    def winner(self):
        for v in self.rotations():
            if (v[0,0] == v[1,0] == v[2,0] or
                    v[0,0] == v[1,1] == v[2,2]):
                if v[0,0] is Tile.EMPTY:
                    return None
                return v[0,0]
            if v[0,1] == v[1,1] == v[2,1]:
                if v[0,1] is Tile.EMPTY:
                    return None
                return v[0,1]
        return None

    def __repr__(self):
        return '\n'.join(''.join(e._value_ for e in row) for row in self._tiles)

    def serialize(self):
        return ''.join(''.join(e._value_ for e in row) for row in self._tiles)

    def __eq__(self, other):
        return isinstance(other, Board) and self._tiles == other._tiles

    def __hash__(self):
        return hash(self._tiles)


class Move:
    """
    One move in a game, relative to a certain board. Immutable.
    """

    def __init__(self, board, x, y, value):
        self._board = board
        self._x = x
        self._y = y
        self._value = value

    @property
    def valid(self):
        return self._board[self._x, self._y] == Tile.EMPTY

    @property
    def last(self):
        return self.board.spaces == 0

    @property
    def board(self):
        return self._board.replace(self._x, self._y, self._value)

    @property
    def wins(self):
        return self.board.winner == self._value

    def _rotate(self):
        return type(self)(self._board, 2-self._y, self._x, self._value)

    def _mirror(self):
        return type(self)(self._board, 2-self._x, self._y, self._value)

    def rotations(self):
        x = self
        for _ in range(4):
            yield x
            yield x._mirror()
            x = x._rotate()

    def symmetries(self):
        return [n for n, v in enumerate(self.rotations()) if v == self]

    def __eq__(self, other):
        return (self._x == other._x and
                self._y == other._y and
                self._value == other._value)

    def __hash__(self):
        return hash((self._x, self._y, self._value))

    def __repr__(self):
        return f'Move<{self._value._name_},x={self._x},y={self._y}>'


def negamax(move):
    """
    Find a move that gives the opponent the least room: force a win if we can,
    if not force a draw.
    If you know negamax and this looks the wrong way up, it's because I'm
    starting the search on the child nodes rather than the root. It simplifies
    the problem of knowing which child gave the best answer.
    """
    if move.wins:
        return 1
    if move.last:
        return 0
    v = float("inf")
    for m in move.board.unique_moves(None):
        nv = -negamax(m)
        v = min(v, nv)
        # simple pruning: nothing we do now will make it worse
        if v <= -1:
            break
    return v
