from .base import OperationRecorder
from .intbounds import IntBounds
from .pure import ConstantFold, GuardPropagation


ALL_OPTIMIZATIONS = [
    IntBounds,
    GuardPropagation,
    ConstantFold,
]
