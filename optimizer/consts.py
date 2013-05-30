from flufl.enum import Enum


class Operations(Enum):
    RETURN = 0

    GUARD_TRUE = 1
    GUARD_FALSE = 2

    INT_ADD = 3
    INT_SUB = 4

    INT_EQ = 5
    INT_LT = 6
    INT_GT = 7


class Types(Enum):
    VOID = 0
    INT = 1
