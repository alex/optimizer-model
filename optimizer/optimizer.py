from __future__ import absolute_import

from . import Types
from .utils.intbounds import IntUnbounded, ConstantIntBounds


class Optimizer(object):
    def __init__(self, optimization_classes=[]):
        self.recorder = opt = OperationRecorder()
        for cls in reversed(optimization_classes):
            opt = cls(opt)
        self.first_optimizer = opt

        self.values = []

    def add_input(self, tp):
        value = InputValue(len(self.values), tp)
        self.values.append(value)
        return value

    def add_operation(self, tp, op, args, descr=None, optimizer=None):
        if optimizer is None:
            optimizer = self.first_optimizer
        value = OperationValue(len(self.values), tp, op, args, descr)
        self.values.append(value)
        optimizer.handle(self, value)
        return value

    def new_constant_int(self, intvalue):
        return ConstantInt(intvalue)

    def new_empty_constant(self, tp):
        assert tp == Types.INT
        return self.new_constant_int(0)

    def build_operations(self):
        return self.recorder.get_operations()

    def getvalues(self, args):
        return [self.getvalue(arg) for arg in args]

    def getvalue(self, arg):
        return arg.getvalue(self)

    def make_equal_to(self, val, newval):
        self.values[val.valuenum] = newval

    def set_bounds(self, val, new_bounds):
        self.values[val.valuenum] = val.update_bounds(new_bounds)


class BaseValue(object):
    def is_constant(self):
        return False


class AbstractValue(BaseValue):
    def __init__(self, valuenum, intbounds=None):
        super(AbstractValue, self).__init__()
        self.valuenum = valuenum
        self.intbounds = IntUnbounded() if intbounds is None else intbounds

    def getvalue(self, optimizer):
        return optimizer.values[self.valuenum]

    def getintbound(self):
        return self.intbounds


class OperationValue(AbstractValue):
    def __init__(self, valuenum, tp, op, args, descr):
        super(OperationValue, self).__init__(valuenum)
        self.tp = tp
        self.op = op
        self.args = args
        self.descr = descr

    def is_virtual(self):
        return False

    def getarg(self, n):
        return self.args[n]

    def getarglist(self):
        return self.args

    def getdescr(self):
        return self.descr


class InputValue(AbstractValue):
    def __init__(self, valuenum, tp, intbounds=None):
        super(InputValue, self).__init__(valuenum, intbounds)
        self.tp = tp

    def is_virtual(self):
        return False

    def update_bounds(self, bounds):
        return InputValue(self.valuenum, self.tp, bounds)


class BaseConstant(BaseValue):
    def is_constant(self):
        return True

    def getvalue(self, optimizer):
        return self


class ConstantInt(BaseConstant):
    def __init__(self, intvalue):
        super(ConstantInt, self).__init__()
        self.intvalue = intvalue

    def getint(self):
        return self.intvalue

    def getintbound(self):
        return ConstantIntBounds(self.intvalue)


# TODO: needs to share a common base class with BaseOptimization
class OperationRecorder(object):
    def __init__(self):
        super(OperationRecorder, self).__init__()
        self.operations = []

    def handle(self, optimizer, operation):
        self.operations.append(operation)

    def get_operations(self):
        return self.operations
