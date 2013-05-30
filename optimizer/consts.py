from flufl.enum import Enum


class Operations(Enum):
    RETURN = 0

    GUARD_TRUE = 1

    INT_ADD = 2
    INT_LT = 3


class Types(Enum):
    VOID = 0
    INT = 1
