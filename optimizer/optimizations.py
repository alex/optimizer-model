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
    def __init__(self, prev):
        self.prev = prev

    def handle(self, optimizer, operation):
        if operation.op == Operations.INT_ADD:
            [lhs, rhs] = optimizer.getvalues(operation.arguments)
            if rhs.is_constant() and rhs.getint() == 0:
                optimizer.make_equal_to(lhs, rhs)
                return
        self.prev.handle(optimizer, operation)
