from optimizer.utils.intbounds import IntBounds


class TestIntBounds(object):
    def test_make_gt(self):
        i0 = IntBounds()

        i1 = i0.make_gt(IntBounds(10, 10))

        assert i1.lower == 11

    def test_make_gt_already_bounded(self):
        i0 = IntBounds()

        i1 = i0.make_gt(IntBounds(10, 10)).make_gt(IntBounds(0, 0))

        assert i1.lower == 11

    def test_make_lt(self):
        i0 = IntBounds()

        i1 = i0.make_lt(IntBounds(10, 10))

        assert i1.upper == 9

    def test_make_lt_already_bounded(self):
        i0 = IntBounds()

        i1 = i0.make_lt(IntBounds(0, 0)).make_lt(IntBounds(10, 10))

        assert i1.upper == -1

    def test_both_bounds(self):
        i0 = IntBounds()

        i1 = i0.make_lt(IntBounds(10, 10)).make_gt(IntBounds(0, 0))

        assert i1.upper == 9
        assert i1.lower == 1

        i2 = i0.make_gt(IntBounds(0, 0)).make_lt(IntBounds(10, 10))

        assert i2.lower == 1
        assert i2.upper == 9

    def test_make_le_already_bounded(self):
        i0 = IntBounds()
        i1 = i0.make_le(IntBounds(0, 0)).make_le(IntBounds(2, 2))

        assert i1.upper == 0

    def test_make_ge_already_bounded(self):
        i0 = IntBounds()
        i1 = i0.make_ge(IntBounds(10, 10)).make_ge(IntBounds(0, 0))

        assert i1.lower == 10
