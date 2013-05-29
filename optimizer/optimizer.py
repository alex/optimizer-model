from __future__ import absolute_import

from .optimizations import OperationRecorder


class Optimizer(object):
    def __init__(self, optimization_classes=[]):
        self.recorder = opt = OperationRecorder()
        for cls in optimization_classes:
            opt = cls(opt)
        self.first_optimizer = opt

        self.values = []

    def add_input(self, tp):
        value = InputValue(len(self.values), tp)
        self.values.append(value)
        return value

    def add_operation(self, tp, op, arguments):
        value = OperationValue(len(self.values), tp, op, arguments)
        self.values.append(value)
        self.first_optimizer.handle(self, value)
        return value

    def new_constant(self, box):
        return Constant(box)

    def build_operations(self):
        return self.recorder.get_operations()

    def getvalues(self, args):
        return [self.getvalue(arg) for arg in args]

    def getvalue(self, arg):
        return arg.getvalue(self)

    def make_equal_to(self, val, newval):
        self.values[val.valuenum] = newval


class BaseValue(object):
    def is_constant(self):
        return False


class NumberedValue(BaseValue):
    def __init__(self, valuenum):
        super(NumberedValue, self).__init__()
        self.valuenum = valuenum

    def getvalue(self, optimizer):
        return optimizer.values[self.valuenum]


class OperationValue(NumberedValue):
    def __init__(self, valuenum, tp, op, arguments):
        super(OperationValue, self).__init__(valuenum)
        self.tp = tp
        self.op = op
        self.arguments = arguments


class InputValue(NumberedValue):
    def __init__(self, valuenum, tp):
        super(InputValue, self).__init__(valuenum)
        self.tp = tp


class Constant(BaseValue):
    def __init__(self, box):
        super(Constant, self).__init__()
        self.box = box

    def is_constant(self):
        return True

    def getvalue(self, optimizer):
        return self

    def getint(self):
        return self.box.getint()
