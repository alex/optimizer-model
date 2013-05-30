from optimizer.intbounds import IntUnbounded, ConstantIntBounds


class TestIntBounds(object):
    def test_make_gt(self):
        i0 = IntUnbounded()
        i1 = ConstantIntBounds(10)

        i2 = i0.make_gt(i1)

        assert not i2.known_gt(i1)
        assert not i2.known_lt(i1)

        i3 = ConstantIntBounds(9)

        assert i2.known_gt(i3)

    def test_make_lt(self):
        i0 = IntUnbounded()
        i1 = ConstantIntBounds(10)

        i2 = i0.make_lt(i1)

        assert not i2.known_gt(i1)
        assert not i2.known_lt(i1)

        i3 = ConstantIntBounds(11)

        assert i2.known_lt(i3)
