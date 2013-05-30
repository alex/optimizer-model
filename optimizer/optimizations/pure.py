import operator

from .base import BaseOptimization
from .utils import OpDispatcher
from .. import Operations


class ConstantFold(BaseOptimization):
    op_map = {
        Operations.INT_ADD: operator.add,
    }

    def handle(self, optimizer, operation):
        if operation.op in self.op_map:
            args = optimizer.getvalues(operation.getarglist())
            if all(arg.is_constant() for arg in args):
                res = self.op_map[operation.op](*(arg.getint() for arg in args))
                optimizer.make_equal_to(operation, optimizer.new_constant_int(res))
                return
        self.prev.handle(optimizer, operation)


class GuardPropagation(BaseOptimization):
    dispatcher = OpDispatcher()

    @dispatcher.register(Operations.GUARD_TRUE)
    def optimize_GUARD_TRUE(self, optimizer, operation):
        self.prev.handle(optimizer, operation)
        optimizer.make_equal_to(operation.getarg(0), optimizer.new_constant_int(1))

    handle = dispatcher.build_handler()
