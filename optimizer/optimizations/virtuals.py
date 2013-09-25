from .base import BaseOptimization
from .utils import OpDispatcher
from .. import Operations
from ..optimizer import BaseValue
from ..utils.persistent_dict import PersistentDict


class Virtualize(BaseOptimization):
    dispatcher = OpDispatcher()

    @dispatcher.register(Operations.NEW)
    def optimize_NEW(self, optimizer, operation):
        optimizer.make_equal_to(operation, VirtualValue(operation, operation.getdescr()))

    @dispatcher.register(Operations.SETFIELD)
    def optimize_SETFIELD(self, optimizer, operation):
        value = optimizer.getvalue(operation.getarg(0))
        if value.is_virtual():
            value.setfield(optimizer, operation.getdescr(), optimizer.getvalue(operation.getarg(1)))
        else:
            self.handle_back(optimizer, operation)

    @dispatcher.register(Operations.GETFIELD)
    def optimize_GETFIELD(self, optimizer, operation):
        value = optimizer.getvalue(operation.getarg(0))
        if value.is_virtual():
            res = value.getfield(operation.getdescr())
            if res is not None:
                optimizer.make_equal_to(operation, res)
            else:
                optimizer.make_equal_to(operation, optimizer.new_empty_constant(operation.gettype()))
        else:
            self.handle_back(optimizer, operation)

    def handle_back(self, optimizer, operation):
        for arg in operation.getarglist():
            value = optimizer.getvalue(arg)
            if value.is_virtual():
                value.force(optimizer, self.prev)
        super(Virtualize, self).handle_back(optimizer, operation)

    handle = dispatcher.build_handler()


class VirtualValue(BaseValue):
    def __init__(self, original_operation, struct_descr, setfields=PersistentDict()):
        super(VirtualValue, self).__init__()
        self.original_operation = original_operation
        self.struct_descr = struct_descr
        self.setfields = setfields

    def is_virtual(self):
        return True

    def getvalue(self, optimizer):
        return self

    def force(self, optimizer, optimization):
        p = optimizer.add_operation(Operations.NEW, [], descr=self.struct_descr, optimization=optimization)
        optimizer.make_equal_to(self.original_operation, p)
        for descr, value in self.setfields.iteritems():
            value = optimizer.getvalue(value)
            optimizer.add_operation(Operations.SETFIELD, [p, value], descr=descr)

    def getfield(self, descr):
        return self.setfields.get(descr)

    def setfield(self, optimizer, field_descr, value):
        new_value = VirtualValue(self.original_operation, self.struct_descr, self.setfields.setitem(field_descr, value))
        optimizer.make_equal_to(self.original_operation, new_value)
