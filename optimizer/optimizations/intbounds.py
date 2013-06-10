from .base import BaseOptimization
from .utils import OpDispatcher
from .. import Operations


class IntBounds(BaseOptimization):
    dispatcher = OpDispatcher()
    bounds_dispatcher = OpDispatcher()

    @dispatcher.register(Operations.INT_LT)
    def optimize_INT_LT(self, optimizer, operation):
        [lhs, rhs] = optimizer.getvalues(operation.getarglist())
        if lhs.getintbound().known_lt(rhs.getintbound()):
            optimizer.make_equal_to(operation, optimizer.new_constant_int(1))
        elif lhs.getintbound().known_ge(rhs.getintbound()) or lhs is rhs:
            optimizer.make_equal_to(operation, optimizer.new_constant_int(0))
        else:
            self.handle_back(optimizer, operation)

    @dispatcher.register(Operations.INT_GT)
    def optimize_INT_GT(self, optimizer, operation):
        [lhs, rhs] = optimizer.getvalues(operation.getarglist())
        if lhs.getintbound().known_gt(rhs.getintbound()):
            optimizer.make_equal_to(operation, optimizer.new_constant_int(1))
        elif lhs.getintbound().known_le(rhs.getintbound()) or lhs is rhs:
            optimizer.make_equal_to(operation, optimizer.new_constant_int(0))
        else:
            self.handle_back(optimizer, operation)

    @dispatcher.register(Operations.GUARD_TRUE)
    def optimize_GUARD_TRUE(self, optimizer, operation):
        self.handle_back(optimizer, operation)
        self.propogate_bounds(optimizer, operation.getarg(0))

    @dispatcher.register(Operations.GUARD_FALSE)
    def optimize_GUARD_FALSE(self, optimizer, operation):
        self.handle_back(optimizer, operation)
        self.propogate_bounds(optimizer, operation.getarg(0))

    @bounds_dispatcher.register(Operations.INT_LT)
    def propogate_bounds_INT_LT(self, optimizer, operation):
        value = optimizer.getvalue(operation)
        if value.is_constant():
            [arg1, arg2] = operation.getarglist()
            if value.getint():
                optimizer.set_bounds(arg1, arg1.getintbound().make_lt(arg2.getintbound()))
                optimizer.set_bounds(arg2, arg2.getintbound().make_ge(arg1.getintbound()))
            else:
                optimizer.set_bounds(arg1, arg1.getintbound().make_ge(arg2.getintbound()))
                optimizer.set_bounds(arg2, arg2.getintbound().make_lt(arg1.getintbound()))

    @bounds_dispatcher.register(Operations.INT_GT)
    def propogate_bounds_INT_GT(self, optimizer, operation):
        value = optimizer.getvalue(operation)
        if value.is_constant():
            [arg1, arg2] = operation.getarglist()
            if value.getint():
                optimizer.set_bounds(arg1, arg1.getintbound().make_gt(arg2.getintbound()))
                optimizer.set_bounds(arg2, arg2.getintbound().make_le(arg1.getintbound()))
            else:
                optimizer.set_bounds(arg1, arg1.getintbound().make_le(arg2.getintbound()))
                optimizer.set_bounds(arg2, arg2.getintbound().make_gt(arg1.getintbound()))

    handle = dispatcher.build_handler()
    propogate_bounds = bounds_dispatcher.build_dispatcher()
