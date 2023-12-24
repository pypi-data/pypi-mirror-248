"""Expose selected package contents."""
from .calculator_sub_package import BinaryArithmeticOperator, calculate_results
from .data_using_module import METADATA
from .garbage_collection_module import define_garbage_collection_decorator
from .simplify import solve_simplification

__all__ = [
    "BinaryArithmeticOperator",
    "calculate_results",
    "define_garbage_collection_decorator",
    "solve_simplification",
]
__version__: str = METADATA.Version
