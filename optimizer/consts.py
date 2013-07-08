from flufl.enum import Enum


class Operations(Enum):
    LABEL = 0
    JUMP = 1
    FINISH = 2

    GUARD_TRUE = 3
    GUARD_FALSE = 4

    INT_ADD = 5
    INT_SUB = 6

    INT_EQ = 7
    INT_NE = 8
    INT_LT = 9
    INT_LE = 10
    INT_GT = 11
    INT_GE = 12

    NEW = 13

    GETFIELD = 14
    SETFIELD = 15


class Types(Enum):
    VOID = 0
    INT = 1
    FLOAT = 2
    REF = 3
