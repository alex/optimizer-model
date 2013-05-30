class BaseIntBounds(object):
    def known_lt(self, other):
        return self.has_upper() and other.has_lower() and self.get_upper() < other.get_lower()

    def known_gt(self, other):
        return other.known_lt(self)

    def known_le(self, other):
        return self.has_upper() and other.has_lower() and self.get_upper() <= other.get_lower()

    def known_ge(self, other):
        return other.known_le(self)

    def make_lt(self, other):
        if other.has_upper() and (not self.has_upper() or other.get_upper() < self.get_upper()):
            return self.replace(upper=other.get_upper())
        return self

    def make_gt(self, other):
        if other.has_lower() and (not self.has_lower() or other.get_lower() > self.get_lower()):
            return self.replace(lower=other.get_lower())
        return self


class IntUnbounded(BaseIntBounds):
    def replace(self, lower=None, upper=None):
        if upper is not None and lower is not None:
            raise NotImplementedError
        elif lower is not None:
            return IntLowerBound(lower)
        elif upper is not None:
            return IntUpperBound(upper)
        else:
            raise NotImplementedError

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


class IntLowerBound(BaseIntBounds):
    def __init__(self, lower):
        super(IntLowerBound, self).__init__()
        self.lower = lower

    def has_lower(self):
        return True

    def has_upper(self):
        return False

    def get_lower(self):
        return self.lower


class IntUpperBound(BaseIntBounds):
    def __init__(self, upper):
        super(IntUpperBound, self).__init__()
        self.upper = upper

    def has_lower(self):
        return False

    def has_upper(self):
        return True

    def get_upper(self):
        return self.upper
