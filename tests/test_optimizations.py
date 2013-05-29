from optimizer import Optimizer, Operations, Types, boxes
from optimizer.optimizations import ConstantFold


class TestConstantFold(object):
    def test_plus_zero(self):
        opt = Optimizer([ConstantFold])

        i0 = opt.add_input(Types.INT)

        opt.add_operation(Operations.INT_ADD,
            [i0, opt.new_constant(boxes.BoxInt(0))]
        )
        ops = opt.build_operations()

        assert len(ops) == 0

    def test_cant_fold(self):
        opt = Optimizer([ConstantFold])
        i0 = opt.add_input(Types.INT)

        opt.add_operation(Operations.INT_ADD,
            [i0, opt.new_constant(boxes.BoxInt(1))]
        )
        ops = opt.build_operations()
        assert len(ops) == 1
