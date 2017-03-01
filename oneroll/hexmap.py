
class Hex:
    def __init__(self, q, r,):
        self.q = q
        self.r = r
        self.s = -q -r
        assert self.q + self.r + self.s == 0

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r)

    def distance(self, other):
        _ = self - other
        return sum([abs(x) for x in [_.q, _.r, _.s]]) // 2

    def neighbor(self, direction):
        assert type(direction) == int, "Choose an integer between 0 and 5."
        _dirs = (Hex(1, 0), Hex(1, -1), Hex(0, -1),
                 Hex(-1, 0), Hex(-1, 1), Hex(0, 1))
        return self + _dirs[direction % 6]

    def __hash__(self):
        return hash((self.q, self.r))


if __name__ == "__main__":
    foo = Hex(0, 0)
    bar = Hex(-3, 3)

    print(foo.distance(bar))
    print(foo.neighbor(-6))