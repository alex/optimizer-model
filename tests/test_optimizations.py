from optimizer import Optimizer, Operations, Types
from optimizer.optimizations import ConstantFold, IntBounds, GuardPropagation


class TestConstantFold(object):
    def test_addition(self):
        opt = Optimizer([ConstantFold])

        opt.add_operation(Types.INT, Operations.INT_ADD,
            [opt.new_constant_int(1), opt.new_constant_int(0)]
        )
        ops = opt.build_operations()

        assert len(ops) == 0

    def test_subtraction(self):
        opt = Optimizer([ConstantFold])
        opt.add_operation(Types.INT, Operations.INT_SUB,
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


class TestGuardPropogation(object):
    def test_guard_true(self):
        opt = Optimizer([ConstantFold, GuardPropagation])
        i0 = opt.add_input(Types.INT)

        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i0])
        opt.add_operation(Types.INT, Operations.INT_EQ, [i0, opt.new_constant_int(1)])

        ops = opt.build_operations()
        assert len(ops) == 1

        assert opt.getvalue(i0).getint() == 1

    def test_guard_false(self):
        opt = Optimizer([ConstantFold, GuardPropagation])
        i0 = opt.add_input(Types.INT)

        opt.add_operation(Types.VOID, Operations.GUARD_FALSE, [i0])
        opt.add_operation(Types.INT, Operations.INT_EQ, [i0, opt.new_constant_int(1)])

        ops = opt.build_operations()
        assert len(ops) == 1

        assert opt.getvalue(i0).getint() == 0


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

    def test_gt(self):
        opt = Optimizer([IntBounds, GuardPropagation])
        i0 = opt.add_input(Types.INT)

        i1 = opt.add_operation(Types.INT, Operations.INT_GT,
            [i0, opt.new_constant_int(10)]
        )
        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i1])
        opt.add_operation(Types.INT, Operations.INT_GT, [i0, opt.new_constant_int(5)])

        ops = opt.build_operations()
        assert len(ops) == 2
