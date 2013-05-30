from optimizer.intbounds import IntUnbounded, ConstantIntBounds


class TestIntBounds(object):
    def test_make_gt(self):
        i0 = IntUnbounded()
        i1 = ConstantIntBounds(10)

        i2 = i0.make_gt(i1)

        assert i2.has_lower()
        assert not i2.has_upper()
        assert i2.get_lower() == 11

    def test_make_lt(self):
        i0 = IntUnbounded()
        i1 = ConstantIntBounds(10)

        i2 = i0.make_lt(i1)

        assert i2.has_upper()
        assert not i2.has_lower()
        assert i2.get_upper() == 9
