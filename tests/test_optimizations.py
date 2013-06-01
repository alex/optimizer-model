from optimizer import Optimizer, Operations, Types
from optimizer.optimizations import (ConstantFold, IntBounds, GuardPropagation,
    Virtualize)


class TestConstantFold(object):
    def test_addition(self):
        opt = Optimizer([ConstantFold])

        res = opt.add_operation(Types.INT, Operations.INT_ADD,
            [opt.new_constant_int(1), opt.new_constant_int(0)]
        )
        ops = opt.build_operations()

        assert len(ops) == 0
        assert opt.getvalue(res).getint() == 1

    def test_subtraction(self):
        opt = Optimizer([ConstantFold])
        res = opt.add_operation(Types.INT, Operations.INT_SUB,
            [opt.new_constant_int(1), opt.new_constant_int(0)]
        )
        ops = opt.build_operations()

        assert len(ops) == 0
        assert opt.getvalue(res).getint() == 1

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

    def test_known_guard_true(self):
        opt = Optimizer([GuardPropagation])
        i0 = opt.add_input(Types.INT)

        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i0])
        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i0])

        ops = opt.build_operations()
        assert len(ops) == 1

        assert opt.getvalue(i0).getint() == 1


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

    def test_lt_reverse(self):
        opt = Optimizer([IntBounds, GuardPropagation])
        i0 = opt.add_input(Types.INT)

        i1 = opt.add_operation(Types.INT, Operations.INT_GT,
            [i0, opt.new_constant_int(5)]
        )
        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i1])
        i2 = opt.add_operation(Types.INT, Operations.INT_LT,
            [i0, opt.new_constant_int(3)]
        )
        opt.add_operation(Types.VOID, Operations.GUARD_FALSE, [i2])

        ops = opt.build_operations()
        assert len(ops) == 2
        assert opt.getvalue(i2).getint() == 0

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

    def test_gt_reverse(self):
        opt = Optimizer([IntBounds, GuardPropagation])
        i0 = opt.add_input(Types.INT)

        i1 = opt.add_operation(Types.INT, Operations.INT_LT,
            [i0, opt.new_constant_int(5)]
        )
        opt.add_operation(Types.VOID, Operations.GUARD_TRUE, [i1])
        i2 = opt.add_operation(Types.INT, Operations.INT_GT,
            [i0, opt.new_constant_int(7)]
        )
        opt.add_operation(Types.VOID, Operations.GUARD_FALSE, [i2])

        ops = opt.build_operations()
        assert len(ops) == 2
        assert opt.getvalue(i2).getint() == 0


class TestVirtualize(object):
    def test_simple_new(self, cpu):
        opt = Optimizer([Virtualize])
        struct_descr = cpu.new_struct()

        opt.add_operation(Types.REF, Operations.NEW, [], descr=struct_descr)

        ops = opt.build_operations()
        assert len(ops) == 0

    def test_simple_new_escapes(self, cpu):
        opt = Optimizer([Virtualize])
        struct_descr = cpu.new_struct()

        p0 = opt.add_operation(Types.REF, Operations.NEW, [], descr=struct_descr)
        opt.add_operation(Types.VOID, Operations.RETURN, [p0])

        ops = opt.build_operations()
        assert len(ops) == 2

    def test_setfield(self, cpu):
        opt = Optimizer([Virtualize])
        i0 = opt.add_input(Types.INT)
        struct_descr = cpu.new_struct()
        field_descr = cpu.new_field(struct_descr)

        p0 = opt.add_operation(Types.REF, Operations.NEW, [], descr=struct_descr)
        opt.add_operation(Types.VOID, Operations.SETFIELD, [p0, i0], descr=field_descr)

        ops = opt.build_operations()
        assert len(ops) == 0

    def test_setfield_escapes(self, cpu):
        opt = Optimizer([Virtualize])
        i0 = opt.add_input(Types.INT)
        struct_descr = cpu.new_struct()
        field_descr = cpu.new_field(struct_descr)

        p0 = opt.add_operation(Types.REF, Operations.NEW, [], descr=struct_descr)
        opt.add_operation(Types.VOID, Operations.SETFIELD, [p0, i0], descr=field_descr)
        opt.add_operation(Types.VOID, Operations.RETURN, [p0])

        ops = opt.build_operations()
        assert len(ops) == 3

    def test_get_setfield(self, cpu):
        opt = Optimizer([Virtualize])
        i0 = opt.add_input(Types.INT)
        struct_descr = cpu.new_struct()
        field_descr = cpu.new_field(struct_descr)

        p0 = opt.add_operation(Types.REF, Operations.NEW, [], descr=struct_descr)
        opt.add_operation(Types.VOID, Operations.SETFIELD, [p0, i0], descr=field_descr)
        i1 = opt.add_operation(Types.INT, Operations.GETFIELD, [p0], descr=field_descr)

        ops = opt.build_operations()
        assert len(ops) == 0

        assert opt.getvalue(i1) is i0

    def test_get_setfield_input(self, cpu):
        opt = Optimizer([Virtualize])
        struct_descr = cpu.new_struct()
        field_descr = cpu.new_field(struct_descr)
        i0 = opt.add_input(Types.INT)
        p0 = opt.add_input(Types.REF)

        opt.add_operation(Types.VOID, Operations.SETFIELD, [p0, i0], descr=field_descr)
        opt.add_operation(Types.INT, Operations.GETFIELD, [p0], descr=field_descr)

        ops = opt.build_operations()
        assert len(ops) == 2

    def test_multiple_setfields(self, cpu):
        opt = Optimizer([Virtualize])
        struct_descr = cpu.new_struct()
        field_descr1 = cpu.new_field(struct_descr)
        field_descr2 = cpu.new_field(struct_descr)
        i0 = opt.add_input(Types.INT)
        i1 = opt.add_input(Types.INT)

        p0 = opt.add_operation(Types.REF, Operations.NEW, [], descr=struct_descr)
        opt.add_operation(Types.VOID, Operations.SETFIELD, [p0, i0], descr=field_descr1)
        opt.add_operation(Types.VOID, Operations.SETFIELD, [p0, i1], descr=field_descr2)
        i2 = opt.add_operation(Types.INT, Operations.GETFIELD, [p0], descr=field_descr1)
        i3 = opt.add_operation(Types.INT, Operations.GETFIELD, [p0], descr=field_descr2)

        ops = opt.build_operations()
        assert len(ops) == 0

        assert opt.getvalue(i2) is i0
        assert opt.getvalue(i3) is i1
