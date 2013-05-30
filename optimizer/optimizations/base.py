class BaseOptimization(object):
    def __init__(self, prev):
        super(BaseOptimization, self).__init__()
        self.prev = prev


# TODO: needs to share a common base class with BaseOptimization
class OperationRecorder(object):
    def __init__(self):
        super(OperationRecorder, self).__init__()
        self.operations = []

    def handle(self, optimizer, operation):
        self.operations.append(operation)

    def get_operations(self):
        return self.operations
