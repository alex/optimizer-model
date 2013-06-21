from __future__ import absolute_import

from . import Types
from .utils.intbounds import IntBounds


class Optimizer(object):
    def __init__(self, optimization_classes=[]):
        self.recorder = opt = OperationRecorder()
        for cls in reversed(optimization_classes):
            opt = cls(opt)
        self.first_optimization = opt

        self.values = []

    def add_input(self, tp):
        value = InputValue(len(self.values), tp)
        self.values.append(value)
        return value

    def add_operation(self, op, args, descr=None, optimization=None):
        if optimization is None:
            optimization = self.first_optimization
        value = OperationValue(len(self.values), op, args, descr)
        self.values.append(value)
        optimization.handle(self, value)
        return value

    def new_constant_int(self, intvalue):
        return ConstantInt(intvalue)

    def new_constant_float(self, floatvalue):
        return ConstantFloat(floatvalue)

    def new_constant_ref(self, refvalue):
        return ConstantRef(refvalue)

    def new_empty_constant(self, tp):
        if tp == Types.INT:
            return self.new_constant_int(0)
        elif tp == Types.FLOAT:
            return self.new_constant_float(0.0)
        elif tp == Types.REF:
            return self.new_constant_ref(None)
        else:
            raise SystemError

    def build_operations(self):
        return self.recorder.get_operations()

    def getvalues(self, args):
        return [self.getvalue(arg) for arg in args]

    def getvalue(self, arg):
        return arg.getvalue(self)

    def make_equal_to(self, val, newval):
        self.values[val.valuenum] = newval

    def set_bounds(self, val, new_bounds):
        if isinstance(val, AbstractValue):
            self.values[val.valuenum] = val.update_bounds(new_bounds)


class BaseValue(object):
    def is_constant(self):
        return False


class AbstractValue(BaseValue):
    def __init__(self, valuenum, intbounds=None):
        super(AbstractValue, self).__init__()
        self.valuenum = valuenum
        self.intbounds = IntBounds() if intbounds is None else intbounds

    def getvalue(self, optimizer):
        return optimizer.values[self.valuenum]

    def getintbound(self):
        return self.intbounds


class OperationValue(AbstractValue):
    def __init__(self, valuenum, op, args, descr):
        super(OperationValue, self).__init__(valuenum)
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

    def gettype(self):
        if self.getdescr() is not None:
            return self.getdescr().gettype()
        raise NotImplementedError


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
        return IntBounds(self.intvalue, self.intvalue)


class ConstantFloat(BaseConstant):
    def __init__(self, floatvalue):
        super(ConstantFloat, self).__init__()
        self.floatvalue = floatvalue

    def getfloat(self):
        return self.floatvalue


class ConstantRef(BaseConstant):
    def __init__(self, refvalue):
        super(ConstantRef, self).__init__()
        self.refvalue = refvalue

    def getref(self):
        return self.refvalue


# TODO: needs to share a common base class with BaseOptimization
class OperationRecorder(object):
    def __init__(self):
        super(OperationRecorder, self).__init__()
        self.operations = []

    def handle(self, optimizer, operation):
        self.operations.append(operation)

    def get_operations(self):
        return self.operations
