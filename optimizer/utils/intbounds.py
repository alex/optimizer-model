import sys


class IntBounds(object):
    def __init__(self, lower=-sys.maxsize - 1, upper=sys.maxsize):
        super(IntBounds, self).__init__()
        self.lower = lower
        self.upper = upper

    def known_lt(self, other):
        return self.upper < other.lower

    def known_gt(self, other):
        return other.known_lt(self)

    def known_le(self, other):
        return self.upper <= other.lower

    def known_ge(self, other):
        return other.known_le(self)

    def make_lt(self, other):
        if other.upper < self.upper:
            return IntBounds(self.lower, other.upper - 1)
        return self

    def make_le(self, other):
        if other.upper < self.upper:
            return IntBounds(self.lower, other.upper)
        return self

    def make_gt(self, other):
        if other.lower > self.lower:
            return IntBounds(other.lower + 1, self.upper)
        return self

    def make_ge(self, other):
        if other.lower > self.lower:
            return IntBounds(other.lower, self.upper)
        return self
