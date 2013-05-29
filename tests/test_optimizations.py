from optimizer import Optimizer, Operations, Types
from optimizer.optimizations import ConstantFold


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
