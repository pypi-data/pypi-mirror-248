"""Contains methods to test various conditions about 1 or more values."""
from typing import Any


def none(value: Any) -> bool:
    """Test if a value is None.

    :param Any value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return value is None


def same_object(first: Any, second: Any) -> bool:
    """Test if two values are the exact same object in memory (NOT `==`).

    :param Any first: The value to test.
    :param Any second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return first is second


def specific_type(value: Any, value_type: type) -> bool:
    """Test if a value is a specific type (do not consider inheritance).

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return type(value) is value_type


def instance(value: Any, value_type: type) -> bool:
    """Test if a value is an instance (the same as or a subclass) of a specific type.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return isinstance(value, value_type)


def zero(value: int | float) -> bool:
    """Test if a value is exactly equal to 0.

    :param int | float value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return value == 0


def positive(value: int | float) -> bool:
    """Test if a value is positive (non-zero).

    :param int | float value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return value > 0


def negative(value: int | float) -> bool:
    """Test if a value is negative (non-zero).

    :param int | float value: The value to test.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return value < 0


def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> bool:
    """Test if a value is within a specified range (inclusive).

    :param int | float value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return minimum <= value <= maximum


def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> bool:
    """Test if a value is within a specified range (non-inclusive).

    :param int | float value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return minimum < value < maximum


def eq(first: int | float, second: int | float) -> bool:
    """Test if a value is exactly equal to a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return first == second


def gt(first: int | float, second: int | float) -> bool:
    """Test if a value is greater than a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return first > second


def lte(first: int | float, second: int | float) -> bool:
    """Test if a value is less than or equal to a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return first <= second


def lt(first: int | float, second: int | float) -> bool:
    """Test if a value is less than a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return first < second


def gte(first: int | float, second: int | float) -> bool:
    """Test if a value is greater than or equal to a second value.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :return: The result of the evaluation.
    :rtype: bool
    """
    return first >= second
