class BaseBox(object):
    pass


class BoxInt(BaseBox):
    def __init__(self, intval):
        super(BoxInt, self).__init__()
        self.intval = intval

    def getint(self):
        return self.intval
