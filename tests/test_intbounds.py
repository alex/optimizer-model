from optimizer.intbounds import IntUnbounded, ConstantIntBounds


class TestIntBounds(object):
    def test_make_gt(self):
        i0 = IntUnbounded()

        i1 = i0.make_gt(ConstantIntBounds(10))

        assert i1.has_lower()
        assert not i1.has_upper()
        assert i1.get_lower() == 11

    def test_make_gt_already_bounded(self):
        i0 = IntUnbounded()

        i1 = i0.make_gt(ConstantIntBounds(10)).make_gt(ConstantIntBounds(0))

        assert i1.has_lower()
        assert not i1.has_upper()
        assert i1.get_lower() == 11

    def test_make_lt(self):
        i0 = IntUnbounded()

        i1 = i0.make_lt(ConstantIntBounds(10))

        assert i1.has_upper()
        assert not i1.has_lower()
        assert i1.get_upper() == 9

    def test_make_lt_already_bounded(self):
        i0 = IntUnbounded()

        i1 = i0.make_lt(ConstantIntBounds(0)).make_lt(ConstantIntBounds(10))

        assert i1.has_upper()
        assert not i1.has_lower()
        assert i1.get_upper() == -1

    def test_both_bounds(self):
        i0 = IntUnbounded()

        i1 = i0.make_lt(ConstantIntBounds(10)).make_gt(ConstantIntBounds(0))

        assert i1.has_upper()
        assert i1.has_lower()
        assert i1.get_upper() == 9
        assert i1.get_lower() == 1

        i2 = i0.make_gt(ConstantIntBounds(0)).make_lt(ConstantIntBounds(10))

        assert i2.has_upper()
        assert i2.has_lower()
        assert i2.get_upper() == 9
        assert i2.get_lower() == 1

    def test_make_le_already_bounded(self):
        i0 = IntUnbounded()
        i1 = i0.make_le(ConstantIntBounds(0)).make_le(ConstantIntBounds(2))

        assert i1.has_upper()
        assert not i1.has_lower()
        assert i1.get_upper() == 0

    def test_make_ge_already_bounded(self):
        i0 = IntUnbounded()
        i1 = i0.make_ge(ConstantIntBounds(10)).make_ge(ConstantIntBounds(0))

        assert i1.has_lower()
        assert not i1.has_upper()
        assert i1.get_lower() == 10
