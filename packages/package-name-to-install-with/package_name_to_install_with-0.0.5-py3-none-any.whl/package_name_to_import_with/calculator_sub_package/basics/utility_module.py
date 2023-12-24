"""Define functions to subtract and divide."""
import pydantic

from .assumptions import add_numbers, get_negative, get_reciprocal, multiply_numbers


@pydantic.validate_call(validate_return=True)
def subtract_numbers(minuend: float, subtrahend: float) -> float:
    """Perform subtraction of two real numbers.

    Parameters
    ----------
    minuend : float
        number which is subtracted from
    subtrahend : float
        number which is subtracted

    Returns
    -------
    float
        difference of ``minuend`` from ``subtrahend``

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with.calculator_sub_package import subtract_numbers
        >>> subtract_numbers(1, 2)
        -1.0
        >>> subtract_numbers(1, -2)
        3.0
        >>> subtract_numbers(-1, 2)
        -3.0
        >>> subtract_numbers(-1, -2)
        1.0
    """
    difference_of_two_numbers = add_numbers(minuend, get_negative(subtrahend))

    return difference_of_two_numbers


@pydantic.validate_call(validate_return=True)
def divide_numbers(dividend: float, divisor: float) -> float:
    """Perform division of two real numbers.

    Parameters
    ----------
    dividend : float
        number which is divided
    divisor : float
        number which divides

    Returns
    -------
    float
        quotient of ``dividend`` by ``divisor``

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with.calculator_sub_package import divide_numbers
        >>> divide_numbers(1, 2)
        0.5
        >>> divide_numbers(1, -2)
        -0.5
        >>> divide_numbers(-1, 2)
        -0.5
        >>> divide_numbers(-1, -2)
        0.5
    """
    quotient_of_two_numbers = multiply_numbers(dividend, get_reciprocal(divisor))

    return quotient_of_two_numbers


__all__ = ["divide_numbers", "subtract_numbers"]
