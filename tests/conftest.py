import pytest


class FakeCPU(object):
    def new_struct(self):
        return FakeStructDescr()

    def new_field(self, struct_descr):
        return FakeFieldDescr(struct_descr)


class BaseFakeDescr(object):
    pass


class FakeStructDescr(BaseFakeDescr):
    pass


class FakeFieldDescr(BaseFakeDescr):
    def __init__(self, struct_descr):
        self.struct_descr = struct_descr


@pytest.fixture
def cpu():
    return FakeCPU()
