from optimizer import Optimizer, Operations, Types


class TestBasic(object):
    def test_emit_operation(self):
        opt = Optimizer()
        opt.add_operation(Types.VOID, Operations.FINISH, [])
        ops = opt.build_operations()
        assert len(ops) == 1
        assert ops[0].op == Operations.FINISH
        assert ops[0].getarglist() == []

    def test_inputs(self):
        opt = Optimizer()
        res = opt.add_input(Types.INT)

        opt.add_operation(Types.VOID, Operations.FINISH, [res])
        ops = opt.build_operations()

        assert len(ops) == 1
        assert ops[0].op == Operations.FINISH
        assert ops[0].getarglist() == [res]
