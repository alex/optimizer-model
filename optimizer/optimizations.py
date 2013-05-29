import operator

from . import Operations


class BaseOptimization(object):
    pass


class OperationRecorder(BaseOptimization):
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

    def __init__(self, prev):
        self.prev = prev

    def handle(self, optimizer, operation):
        if operation.op in self.op_map:
            args = optimizer.getvalues(operation.arguments)
            if all(arg.is_constant() for arg in args):
                res = self.op_map[operation.op](*(arg.getint() for arg in args))
                optimizer.make_equal_to(operation, optimizer.new_constant_int(res))
                return
        self.prev.handle(optimizer, operation)
