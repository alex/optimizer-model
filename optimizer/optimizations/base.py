class BaseOptimization(object):
    def __init__(self, prev):
        super(BaseOptimization, self).__init__()
        self.prev = prev

    def handle_back(self, optimizer, operation):
        self.prev.handle(optimizer, operation)
