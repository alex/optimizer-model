from .intbounds import IntBounds
from .pure import ConstantFold, GuardPropagation
from .virtuals import Virtualize


ALL_OPTIMIZATIONS = [
    IntBounds,
    GuardPropagation,
    ConstantFold,
    Virtualize,
]
