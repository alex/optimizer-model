from flufl.enum import Enum


class Operations(Enum):
    LABEL = 0
    JUMP = 1
    FINISH = 2

    GUARD_TRUE = 3
    GUARD_FALSE = 4
    GUARD_VALUE = 5

    INT_ADD = 6
    INT_SUB = 7

    INT_EQ = 8
    INT_NE = 9
    INT_LT = 10
    INT_LE = 11
    INT_GT = 12
    INT_GE = 13

    NEW = 14

    GETFIELD = 15
    SETFIELD = 16


class Types(Enum):
    VOID = 0
    INT = 1
    FLOAT = 2
    REF = 3
