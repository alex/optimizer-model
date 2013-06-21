import pytest


class FakeCPU(object):
    def new_struct(self):
        return FakeStructDescr()

    def new_field(self, struct_descr, tp):
        return FakeFieldDescr(struct_descr, tp)


class BaseFakeDescr(object):
    pass


class FakeStructDescr(BaseFakeDescr):
    pass


class FakeFieldDescr(BaseFakeDescr):
    def __init__(self, struct_descr, tp):
        self.struct_descr = struct_descr
        self.tp = tp

    def gettype(self):
        return self.tp


@pytest.fixture
def cpu():
    return FakeCPU()
