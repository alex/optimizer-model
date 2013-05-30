from .base import BaseOptimization
from .utils import OpDispatcher
from .. import Operations, Types
from ..optimizer import BaseValue


class Virtualize(BaseOptimization):
    dispatcher = OpDispatcher()

    @dispatcher.register(Operations.NEW)
    def optimize_NEW(self, optimizer, operation):
        optimizer.make_equal_to(operation, VirtualValue(operation))

    def optimize_default(self, optimizer, operation):
        for arg in operation.getarglist():
            value = optimizer.getvalue(arg)
            if value.is_virtual():
                value.force(optimizer, self.prev)
        return self.prev.handle(optimizer, operation)

    handle = dispatcher.build_dispatcher(default=optimize_default)


class VirtualValue(BaseValue):
    def __init__(self, original_operation):
        super(VirtualValue, self).__init__()
        self.original_operation = original_operation

    def is_virtual(self):
        return True

    def force(self, optimizer, optimization):
        p = optimizer.add_operation_at_optimizer(Types.REF, Operations.NEW, [], optimization)
        optimizer.make_equal_to(self.original_operation, p)
