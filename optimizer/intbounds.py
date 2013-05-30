class BaseIntBounds(object):
    def known_lt(self, other):
        return self.has_upper() and other.has_lower() and self.get_upper() < other.get_lower()

    def known_le(self, other):
        return self.has_upper() and other.has_lower() and self.get_upper() <= other.get_lower()

    def known_ge(self, other):
        return other.known_le(self)

    def make_lt(self, other):
        if other.has_upper() and (not self.has_upper() or other.get_upper() < self.get_upper()):
            return self.replace(upper=other.get_upper())
        return self


class IntUnbounded(BaseIntBounds):
    def replace(self, upper):
        return IntUpperBound(upper)

    def has_lower(self):
        return False

    def has_upper(self):
        return False


class ConstantIntBounds(BaseIntBounds):
    def __init__(self, intvalue):
        super(ConstantIntBounds, self).__init__()
        self.intvalue = intvalue

    def has_lower(self):
        return True

    def has_upper(self):
        return True

    def get_lower(self):
        return self.intvalue

    def get_upper(self):
        return self.intvalue


class IntUpperBound(BaseIntBounds):
    def __init__(self, upper):
        super(IntUpperBound, self).__init__()
        self.upper = upper

    def has_upper(self):
        return True

    def get_upper(self):
        return self.upper
