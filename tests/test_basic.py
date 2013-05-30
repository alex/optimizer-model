from optimizer import Optimizer, Operations, Types


class TestBasic(object):
    def test_emit_operation(self):
        opt = Optimizer()
        opt.add_operation(Types.VOID, Operations.RETURN, [])
        ops = opt.build_operations()
        assert len(ops) == 1
        assert ops[0].op == Operations.RETURN
        assert ops[0].getarglist() == []

    def test_inputs(self):
        opt = Optimizer()
        res = opt.add_input(Types.INT)

        opt.add_operation(Types.VOID, Operations.RETURN, [res])
        ops = opt.build_operations()

        assert len(ops) == 1
        assert ops[0].op == Operations.RETURN
        assert ops[0].getarglist() == [res]
