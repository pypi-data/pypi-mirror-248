"""Contains methods to validate various conditions about 1 or more values."""
from typing import Any

from onecondition import test


class ValidationError(ValueError):
    """A subclass of ValueError, this is raised any time a validation check fails."""
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(message)


def none(value: Any) -> None:
    """Validate that a value is None, and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is not None.

    :rtype: None
    """
    if not test.none(value):
        raise ValidationError(f"Value '{value}' must be None")


def not_none(value: Any) -> None:
    """Validate that a value is not None, and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is None.

    :rtype: None
    """
    if test.none(value):
        raise ValidationError("Value must not be None")


def same_object(first: Any, second: Any) -> None:
    """Validate that two values are the exact same object in memory (NOT `==`), and they aren't, is, raise an exception.

    :param Any first: The value to test.
    :param Any second: The value to test against.

    :raises ValidationError: Raised if the objects aren't exact same the same object (uses `is`).

    :rtype: None
    """
    if not test.same_object(first, second):
        raise ValidationError(f"Value '{first}' must be the same object as {second}")


def not_same_object(first: Any, second: Any) -> None:
    """Validate that two values aren't the exact same object in memory (NOT `!=`), and they are, is, raise an exception.

    :param Any first: The value to test.
    :param Any second: The value to test against.

    :raises ValidationError: Raised if the objects are exact same the same object (uses `is`).

    :rtype: None
    """
    if test.same_object(first, second):
        raise ValidationError(f"Value '{first}' must not be the same object as {second}")


def specific_type(value: Any, value_type: type) -> None:
    """Validate that a value is a specific type (do not consider inheritance), and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the type of the value isn't an exact match.

    :rtype: None
    """
    if not test.specific_type(value, value_type):
        raise ValidationError(f"Value '{value}' must be of type {value_type}, not {type(value)}")


def not_specific_type(value: Any, value_type: type) -> None:
    """Validate that a value is a not specific type (do not consider inheritance), and if it is, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the type of the value is an exact match.

    :rtype: None
    """
    if test.specific_type(value, value_type):
        raise ValidationError(f"Value '{value}' must be not of type {value_type}")


def instance(value: Any, value_type: type) -> None:
    """Validate that a value is an instance (the same as or a subclass) of a specific type, and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the value isn't an instance of the type.

    :rtype: None
    """
    if not test.instance(value, value_type):
        raise ValidationError(f"Value '{value}' must be an instance of {value_type}, not a {type(value)}")


def not_instance(value: Any, value_type: type) -> None:
    """Validate that a value is not an instance (the same as or a subclass) of a specific type, and if it is, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the value is an instance of the type.

    :rtype: None
    """
    if test.instance(value, value_type):
        raise ValidationError(f"Value '{value}' must not be an instance of {value_type}")


def zero(value: int | float) -> None:
    """Validate that a value is exactly equal to 0, and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value isn't exactly equal to zero.

    :rtype: None
    """
    if not test.zero(value):
        raise ValidationError(f"Value '{value}' must be zero")


def not_zero(value: int | float) -> None:
    """Validate that a value is not exactly equal to 0, and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is exactly equal to zero.

    :rtype: None
    """
    if test.zero(value):
        raise ValidationError(f"Value '{value}' must not be zero")


def positive(value: int | float) -> None:
    """Validate that a value is positive (non-zero), and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value isn't positive (non-zero).

    :rtype: None
    """
    if not test.positive(value):
        raise ValidationError(f"Value '{value}' must be positive (non-zero)")


def not_positive(value: int | float) -> None:
    """Validate that a value is not positive (non-zero), and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is positive (non-zero).

    :rtype: None
    """
    if test.positive(value):
        raise ValidationError(f"Value '{value}' must not be positive (non-zero)")


def negative(value: int | float) -> None:
    """Validate that a value is negative (non-zero), and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value isn't negative (non-zero).

    :rtype: None
    """
    if not test.negative(value):
        raise ValidationError(f"Value '{value}' must be negative (non-zero)")


def not_negative(value: int | float) -> None:
    """Validate that a value is not negative (non-zero), and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is negative (non-zero).

    :rtype: None
    """
    if test.negative(value):
        raise ValidationError(f"Value '{value}' must not be negative (non-zero)")


def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is within a specified range (inclusive), and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value isn't within the specified range (inclusive).

    :rtype: None
    """
    if not test.range_inclusive(value, minimum, maximum):
        raise ValidationError(f"Value '{value}' must be between {minimum} and {maximum} (inclusive)")


def not_range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is not within a specified range (inclusive), and if it is, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value is within the specified range (inclusive).

    :rtype: None
    """
    if test.range_inclusive(value, minimum, maximum):
        raise ValidationError(f"Value '{value}' must not be between {minimum} and {maximum} (inclusive)")


def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is within a specified range (non-inclusive), and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value isn't within the specified range (non-inclusive).

    :rtype: None
    """
    if not test.range_non_inclusive(value, minimum, maximum):
        raise ValidationError(f"Value '{value}' must be between {minimum} and {maximum} (non-inclusive)")


def not_range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is not within a specified range (non-inclusive), and if it is, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value is within the specified range (non-inclusive).

    :rtype: None
    """
    if test.range_non_inclusive(value, minimum, maximum):
        raise ValidationError(f"Value '{value}' must not be between {minimum} and {maximum} (non-inclusive)")


def eq(first: int | float, second: int | float) -> None:
    """Validate that a value is exactly equal to a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't exactly equal to a second value.

    :rtype: None
    """
    if not test.eq(first, second):
        raise ValidationError(f"Value '{first}' must be equal to '{second}'")


def neq(first: int | float, second: int | float) -> None:
    """Validate that a value is not exactly equal to a second value, and if it is, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value is exactly equal to a second value.

    :rtype: None
    """
    if test.eq(first, second):
        raise ValidationError(f"Value '{first}' must not be equal to '{second}'")


def gt(first: int | float, second: int | float) -> None:
    """Validate that a value is greater than a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't greater than a second value.

    :rtype: None
    """
    if not test.gt(first, second):
        raise ValidationError(f"Value '{first}' must be greater than '{second}'")


def lte(first: int | float, second: int | float) -> None:
    """Validate that a value is less than or equal to a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't less than or equal to a second value.

    :rtype: None
    """
    if not test.lte(first, second):
        raise ValidationError(f"Value '{first}' must be less than or equal to '{second}'")


def lt(first: int | float, second: int | float) -> None:
    """Validate that a value is less than a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't less than a second value.

    :rtype: None
    """
    if not test.lt(first, second):
        raise ValidationError(f"Value '{first}' must be less than '{second}'")


def gte(first: int | float, second: int | float) -> None:
    """Validate that a value is greater than or equal to a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't greater than or equal to a second value.

    :rtype: None
    """
    if not test.gte(first, second):
        raise ValidationError(f"Value '{first}' must be greater than or equal to '{second}'")
