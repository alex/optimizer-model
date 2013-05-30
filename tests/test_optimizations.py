from optimizer import Optimizer, Operations, Types
from optimizer.optimizations import ConstantFold, IntBounds, GuardPropagation


class TestConstantFold(object):
    def test_plus_zero(self):
        opt = Optimizer([ConstantFold])

        opt.add_operation(Types.INT, Operations.INT_ADD,
            [opt.new_constant_int(1), opt.new_constant_int(0)]
        )
        ops = opt.build_operations()

        assert len(ops) == 0

    def test_cant_fold(self):
        opt = Optimizer([ConstantFold])
        i0 = opt.add_input(Types.INT)

        opt.add_operation(Types.INT, Operations.INT_ADD,
            [i0, opt.new_constant_int(1)]
        )
        ops = opt.build_operations()
        assert len(ops) == 1


class TestIntBounds(object):
    def test_lt(self):
        opt = Optimizer([IntBounds, GuardPropagation])
        i0 = opt.add_input(Types.INT)

        i1 = opt.add_operation(Types.INT, Operations.INT_LT,
            [i0, opt.new_constant_int(10)],
        )
        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i1])
        opt.add_operation(Types.INT, Operations.INT_LT, [i0, opt.new_constant_int(15)])

        ops = opt.build_operations()
        assert len(ops) == 2
