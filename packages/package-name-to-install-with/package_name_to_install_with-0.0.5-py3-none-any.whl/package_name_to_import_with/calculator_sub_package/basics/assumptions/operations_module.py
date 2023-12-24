"""Define functions to add and multiply."""
import pydantic


@pydantic.validate_call(validate_return=True)
def add_numbers(left_addend: float, right_addend: float) -> float:
    """Perform addition of two real numbers.

    Parameters
    ----------
    left_addend : float
        first number to be added
    right_addend : float
        second number to be added

    Returns
    -------
    float
        sum of ``left_addend`` and ``right_addend``

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with.calculator_sub_package import add_numbers
        >>> add_numbers(1, 2)
        3.0
        >>> add_numbers(1, -2)
        -1.0
        >>> add_numbers(-1, 2)
        1.0
        >>> add_numbers(-1, -2)
        -3.0
    """
    sum_of_two_numbers = left_addend + right_addend

    return sum_of_two_numbers


@pydantic.validate_call(validate_return=True)
def multiply_numbers(left_multiplicand: float, right_multiplicand: float) -> float:
    """Perform multiplication of two real numbers.

    Parameters
    ----------
    left_multiplicand : float
        first number to be multiplied
    right_multiplicand : float
        second number to be multiplied

    Returns
    -------
    float
        product of two ``left_multiplicand`` and ``right_multiplicand``

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with.calculator_sub_package import multiply_numbers
        >>> multiply_numbers(1, 2)
        2.0
        >>> multiply_numbers(1, -2)
        -2.0
        >>> multiply_numbers(-1, 2)
        -2.0
        >>> multiply_numbers(-1, -2)
        2.0
    """
    product_of_two_numbers = left_multiplicand * right_multiplicand

    return product_of_two_numbers


__all__ = ["add_numbers", "multiply_numbers"]
