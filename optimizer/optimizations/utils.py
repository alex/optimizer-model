from .. import Operations


class OpDispatcher(object):
    def __init__(self):
        self.dispatch_table = [None] * len(Operations._enums)

    def register(self, op):
        def inner(func):
            self.dispatch_table[op.value] = func
            return func
        return inner

    def build_dispatcher(self, default=None):
        dispatch_table = self.dispatch_table

        def dispatch(self, optimizer, operation):
            if dispatch_table[operation.op.value] is not None:
                return dispatch_table[operation.op.value](self, optimizer, operation)
            if default is not None:
                return default(self, optimizer, operation)
        return dispatch

    def build_handler(self):
        def handler_default(self, optimizer, operation):
            return self.handle_back(optimizer, operation)
        return self.build_dispatcher(default=handler_default)
