import operator

from . import Operations


class BaseOptimization(object):
    def __init__(self, prev):
        super(BaseOptimization, self).__init__()
        self.prev = prev


class OpDispatcher(object):
    def __init__(self):
        self.dispatch_table = {}

    def register(self, op):
        def inner(func):
            self.dispatch_table[op] = func
            return func
        return inner

    def build_dispatcher(self, default=None):
        dispatch_table = self.dispatch_table

        def dispatch(self, optimizer, operation):
            if operation.op in dispatch_table:
                return dispatch_table[operation.op](self, optimizer, operation)
            if default is not None:
                return default(self, optimizer, operation)
        return dispatch

    def build_handler(self):
        def handler_default(self, optimizer, operation):
            return self.prev.handle(optimizer, operation)
        return self.build_dispatcher(default=handler_default)


# TODO: needs to share a common base class with BaseOptimization
class OperationRecorder(object):
    def __init__(self):
        super(OperationRecorder, self).__init__()
        self.operations = []

    def handle(self, optimizer, operation):
        self.operations.append(operation)

    def get_operations(self):
        return self.operations


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
            self.prev.handle(optimizer, operation)

    @dispatcher.register(Operations.GUARD_TRUE)
    def optimize_GUARD_TRUE(self, optimizer, operation):
        self.prev.handle(optimizer, operation)
        self.propogate_bounds(optimizer, operation.getarg(0))

    @bounds_dispatcher.register(Operations.INT_LT)
    def propogate_bounds_INT_LT(self, optimizer, operation):
        value = optimizer.getvalue(operation)
        if value.is_constant():
            if value.getint():
                [arg1, arg2] = operation.getarglist()
                optimizer.set_bounds(arg1, arg1.getintbound().make_lt(arg2.getintbound()))
            else:
                raise NotImplementedError("handle the reverse")

    handle = dispatcher.build_handler()
    propogate_bounds = bounds_dispatcher.build_dispatcher()


class GuardPropagation(BaseOptimization):
    dispatcher = OpDispatcher()

    @dispatcher.register(Operations.GUARD_TRUE)
    def optimize_GUARD_TRUE(self, optimizer, operation):
        self.prev.handle(optimizer, operation)
        optimizer.make_equal_to(operation.getarg(0), optimizer.new_constant_int(1))

    handle = dispatcher.build_handler()
