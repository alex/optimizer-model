from .base import BaseOptimization
from .utils import OpDispatcher
from .. import Operations, Types
from ..optimizer import BaseValue


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
            return self.prev.handle(optimizer, operation)

    @dispatcher.register(Operations.GETFIELD)
    def optimize_GETFIELD(self, optimizer, operation):
        value = optimizer.getvalue(operation.getarg(0))
        if value.is_virtual():
            res = value.getfield(operation.getdescr())
            if res is not None:
                optimizer.make_equal_to(operation, res)
            else:
                optimizer.make_equal_to(operation, optimizer.new_empty_constant(operation.tp))
        else:
            return self.prev.handle(optimizer, operation)

    def optimize_default(self, optimizer, operation):
        for arg in operation.getarglist():
            value = optimizer.getvalue(arg)
            if value.is_virtual():
                value.force(optimizer, self.prev)
        return self.prev.handle(optimizer, operation)

    handle = dispatcher.build_dispatcher(default=optimize_default)


class VirtualValue(BaseValue):
    def __init__(self, original_operation, struct_descr, setfields=None):
        super(VirtualValue, self).__init__()
        self.original_operation = original_operation
        self.struct_descr = struct_descr
        self.setfields = setfields

    def is_virtual(self):
        return True

    def force(self, optimizer, optimization):
        p = optimizer.add_operation(Types.REF, Operations.NEW, [], optimizer=optimization)
        optimizer.make_equal_to(self.original_operation, p)
        seen_descrs = set()
        setfield = self.setfields
        while setfield is not None:
            if setfield.field_descr not in seen_descrs:
                value = optimizer.getvalue(setfield.value)
                optimizer.add_operation(Types.VOID, Operations.SETFIELD, [p, value], descr=setfield.field_descr)
                seen_descrs.add(setfield.field_descr)
            setfield = setfield.prev

    def getfield(self, descr):
        setfield = self.setfields
        while setfield is not None:
            if setfield.field_descr is descr:
                return setfield.value
            setfield = setfield.prev

    def setfield(self, optimizer, field_descr, value):
        new_value = VirtualValue(self.original_operation, self.struct_descr, VirtualSetfield(field_descr, value, self.setfields))
        optimizer.make_equal_to(self.original_operation, new_value)


class VirtualSetfield(object):
    def __init__(self, field_descr, value, prev):
        self.field_descr = field_descr
        self.value = value
        self.prev = prev
