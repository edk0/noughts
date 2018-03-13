import enum


class Tile(enum.Enum):
    EMPTY = ' '
    X = 'x'
    O = 'o'


class Board:
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
        for x in range(3):
            for y in range(3):
                if self[x,y] != Tile.EMPTY:
                    continue
                yield Move(self, x, y, v)

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
        return None

    def __repr__(self):
        return '\n'.join(''.join(e._value_ for e in row) for row in self._tiles)

    def __eq__(self, other):
        return isinstance(other, Board) and self._tiles == other._tiles

    def __hash__(self):
        return hash(self._tiles)


class Move:
    def __init__(self, board, x, y, value):
        self._board = board
        self._x = x
        self._y = y
        self._value = value

    @property
    def valid(self):
        return self._board[self._x, self._y] == Tile.EMPTY

    @property
    def board(self):
        return self._board.replace(self._x, self._y, self._value)

    @property
    def wins(self):
        return self._board.winner == self._value


def negamax(move):
    if check_win(move):
        return 1
    if move.last:
        return 0
    v = float("-inf")
    for m in move.board.moves:
        v = max(v, -negamax(m))
    return v
