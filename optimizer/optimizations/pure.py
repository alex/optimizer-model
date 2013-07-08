import operator

from .base import BaseOptimization
from .utils import OpDispatcher
from .. import Operations


class ConstantFold(BaseOptimization):
    dispatcher = OpDispatcher()

    def make_optimize_operation(func):
        def optimize_operation(self, optimizer, operation):
            args = optimizer.getvalues(operation.getarglist())
            if all(arg.is_constant() for arg in args):
                res = func(*(arg.getint() for arg in args))
                optimizer.make_equal_to(operation, optimizer.new_constant_int(res))
                return
            self.handle_back(optimizer, operation)
        return optimize_operation

    for op, func in [
        (Operations.INT_ADD, operator.add),
        (Operations.INT_SUB, operator.sub),

        (Operations.INT_EQ, operator.eq),
        (Operations.INT_LT, operator.lt),
        (Operations.INT_GT, operator.gt),
        (Operations.INT_GE, operator.ge),
    ]:
        dispatcher.register(op)(make_optimize_operation(func))

    handle = dispatcher.build_handler()


class GuardPropagation(BaseOptimization):
    dispatcher = OpDispatcher()

    @dispatcher.register(Operations.GUARD_TRUE)
    def optimize_GUARD_TRUE(self, optimizer, operation):
        arg = optimizer.getvalue(operation.getarg(0))
        if arg.is_constant():
            assert arg.getint()
        else:
            self.handle_back(optimizer, operation)
            optimizer.make_equal_to(operation.getarg(0), optimizer.new_constant_int(1))

    @dispatcher.register(Operations.GUARD_FALSE)
    def optimize_GUARD_FALSE(self, optimizer, operation):
        arg = optimizer.getvalue(operation.getarg(0))
        if arg.is_constant():
            assert not arg.getint()
        else:
            self.handle_back(optimizer, operation)
            optimizer.make_equal_to(operation.getarg(0), optimizer.new_constant_int(0))

    @dispatcher.register(Operations.GUARD_VALUE)
    def optimize_GUARD_VALUE(self, optimizer, operation):
        [arg, known] = optimizer.getvalues(operation.getarglist())
        assert known.is_constant()
        self.handle_back(optimizer, operation)
        optimizer.make_equal_to(arg, known)

    handle = dispatcher.build_handler()
