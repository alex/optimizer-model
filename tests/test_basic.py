from optimizer import Optimizer, Operations, Types, boxes


class TestBasic(object):
    def test_emit_operation(self):
        opt = Optimizer()
        opt.add_operation(Operations.RETURN, [])
        ops = opt.build_operations()
        assert len(ops) == 1
        assert ops[0].op == Operations.RETURN
        assert ops[0].arguments == []

    def test_inputs(self):
        opt = Optimizer()
        res = opt.add_input(Types.INT)

        opt.add_operation(Operations.RETURN, [res])
        ops = opt.build_operations()

        assert len(ops) == 1
        assert ops[0].op == Operations.RETURN
        assert ops[0].arguments == [res]
