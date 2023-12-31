"""Contains methods to validate various conditions about 1 or more values.

>>> none(None)
>>> not_none("")

>>> class TestError(ValueError):
...     def __init__(self, message):
...         super().__init__(message)
>>> test_error = TestError("Test")
>>> specific_type(test_error, TestError)
>>> instance(test_error, ValueError)
>>> not_specific_type(test_error, ValueError)
>>> not_instance(test_error, TypeError)

>>> zero(0)
>>> not_zero(42)
>>> positive(42)
>>> not_positive(0)
>>> negative(-123.45)
>>> not_negative(0)

>>> range_inclusive(0, 0, 1)
>>> not_range_inclusive(2, 0, 1)
>>> range_non_inclusive(0.5, 0, 1)
>>> not_range_non_inclusive(0, 0, 1)

>>> eq(42, 42)
>>> neq(42, -123.45)
>>> gt(42, -123.45)
>>> lt(-123.45, 42)
>>> gte(0, 0)
>>> lte(0, 0)
"""
from onecondition import ValidationError, test

from typing import Any


def none(value: Any) -> None:
    """Validate that a value is None, and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is not None.

    :rtype: None

    >>> none(None)
    >>> none("")
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `''` must be None
    """
    if not test.none(value):
        raise ValidationError(value, "be None")


def not_none(value: Any) -> None:
    """Validate that a value is not None, and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is None.

    :rtype: None

    >>> not_none("")
    >>> not_none(None)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `None` must not be None
    """
    if test.none(value):
        raise ValidationError(value, "not be None")


def specific_type(value: Any, value_type: type) -> None:
    """Validate that a value is a specific type (do not consider inheritance), and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the type of the value isn't an exact match.

    :rtype: None

    >>> class TestError(ValueError):
    ...     def __init__(self, message):
    ...         super().__init__(message)
    >>> test_error = TestError("Test")
    >>> specific_type(test_error, TestError)
    >>> specific_type(test_error, ValueError)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `TestError('Test')` must be of type <class 'ValueError'>, not <class 'onecondition.validate.TestError'>
    """
    if not test.specific_type(value, value_type):
        raise ValidationError(value, f"be of type {value_type}, not {type(value)}")


def not_specific_type(value: Any, value_type: type) -> None:
    """Validate that a value is a not specific type (do not consider inheritance), and if it is, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the type of the value is an exact match.

    :rtype: None

    >>> class TestError(ValueError):
    ...     def __init__(self, message):
    ...         super().__init__(message)
    >>> test_error = TestError("Test")
    >>> not_specific_type(test_error, ValueError)
    >>> not_specific_type(test_error, TestError)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `TestError('Test')` must be not of type <class 'onecondition.validate.TestError'>
    """
    if test.specific_type(value, value_type):
        raise ValidationError(value, f"be not of type {value_type}")


def instance(value: Any, value_type: type) -> None:
    """Validate that a value is an instance (the same as or a subclass) of a specific type, and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the value isn't an instance of the type.

    :rtype: None

    >>> class TestError(ValueError):
    ...     def __init__(self, message):
    ...         super().__init__(message)
    >>> test_error = TestError("Test")
    >>> instance(test_error, ValueError)
    >>> instance(test_error, TypeError)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `TestError('Test')` must be an instance of <class 'TypeError'>, not a <class 'onecondition.validate.TestError'>
    """
    if not test.instance(value, value_type):
        raise ValidationError(value, f"be an instance of {value_type}, not a {type(value)}")


def not_instance(value: Any, value_type: type) -> None:
    """Validate that a value is not an instance (the same as or a subclass) of a specific type, and if it is, raise an exception.

    :param Any value: The value to test.
    :param type value_type: The type to test the value against.

    :raises ValidationError: Raised if the value is an instance of the type.

    :rtype: None

    >>> class TestError(ValueError):
    ...     def __init__(self, message):
    ...         super().__init__(message)
    >>> test_error = TestError("Test")
    >>> not_instance(test_error, TypeError)
    >>> not_instance(test_error, ValueError)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `TestError('Test')` must not be an instance of <class 'ValueError'>
    """
    if test.instance(value, value_type):
        raise ValidationError(value, f"not be an instance of {value_type}")


def zero(value: int | float) -> None:
    """Validate that a value is exactly equal to 0, and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value isn't exactly equal to zero.

    :rtype: None

    >>> zero(0)
    >>> zero(42)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be zero
    """
    if not test.zero(value):
        raise ValidationError(value, "be zero")


def not_zero(value: int | float) -> None:
    """Validate that a value is not exactly equal to 0, and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is exactly equal to zero.

    :rtype: None

    >>> not_zero(42)
    >>> not_zero(0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must not be zero
    """
    if test.zero(value):
        raise ValidationError(value, "not be zero")


def positive(value: int | float) -> None:
    """Validate that a value is positive (non-zero), and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value isn't positive (non-zero).

    :rtype: None

    >>> positive(42)
    >>> positive(0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must be positive (non-zero)
    >>> positive(-123.45)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `-123.45` must be positive (non-zero)
    """
    if not test.positive(value):
        raise ValidationError(value, "be positive (non-zero)")


def not_positive(value: int | float) -> None:
    """Validate that a value is not positive (non-zero), and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is positive (non-zero).

    :rtype: None

    >>> not_positive(42)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must not be positive (non-zero)
    >>> not_positive(0)
    >>> not_positive(-123.45)
    """
    if test.positive(value):
        raise ValidationError(value, "not be positive (non-zero)")


def negative(value: int | float) -> None:
    """Validate that a value is negative (non-zero), and if it isn't, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value isn't negative (non-zero).

    :rtype: None

    >>> negative(-123.45)
    >>> negative(0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must be negative (non-zero)
    >>> negative(42)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be negative (non-zero)
    """
    if not test.negative(value):
        raise ValidationError(value, "be negative (non-zero)")


def not_negative(value: int | float) -> None:
    """Validate that a value is not negative (non-zero), and if it is, raise an exception.

    :param Any value: The value to test.

    :raises ValidationError: Raised if the value is negative (non-zero).

    :rtype: None

    >>> not_negative(-123.45)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `-123.45` must not be negative (non-zero)
    >>> not_negative(0)
    >>> not_negative(42)
    """
    if test.negative(value):
        raise ValidationError(value, "not be negative (non-zero)")


def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is within a specified range (inclusive), and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value isn't within the specified range (inclusive).

    :rtype: None

    >>> range_inclusive(0, 0, 1)
    >>> range_inclusive(1, 0, 1)
    >>> range_inclusive(42, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be between 0 and 1 (inclusive)
    """
    if not test.range_inclusive(value, minimum, maximum):
        raise ValidationError(value, f"be between {minimum} and {maximum} (inclusive)")


def not_range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is not within a specified range (inclusive), and if it is, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value is within the specified range (inclusive).

    :rtype: None

    >>> not_range_inclusive(0, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must not be between 0 and 1 (inclusive)
    >>> not_range_inclusive(1, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `1` must not be between 0 and 1 (inclusive)
    >>> not_range_inclusive(42, 0, 1)
    """
    if test.range_inclusive(value, minimum, maximum):
        raise ValidationError(value, f"not be between {minimum} and {maximum} (inclusive)")


def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is within a specified range (non-inclusive), and if it isn't, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value isn't within the specified range (non-inclusive).

    :rtype: None

    >>> range_non_inclusive(0.5, 0, 1)
    >>> range_non_inclusive(0, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must be between 0 and 1 (non-inclusive)
    >>> range_non_inclusive(42, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be between 0 and 1 (non-inclusive)
    """
    if not test.range_non_inclusive(value, minimum, maximum):
        raise ValidationError(value, f"be between {minimum} and {maximum} (non-inclusive)")


def not_range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
    """Validate that a value is not within a specified range (non-inclusive), and if it is, raise an exception.

    :param Any value: The value to test.
    :param int | float minimum: The minimum value to test against.
    :param int | float maximum: The maximum value to test against.

    :raises ValidationError: Raised if the value is within the specified range (non-inclusive).

    :rtype: None

    >>> not_range_non_inclusive(0.5, 0, 1)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0.5` must not be between 0 and 1 (non-inclusive)
    >>> not_range_non_inclusive(0, 0, 1)
    >>> not_range_non_inclusive(42, 0, 1)
    """
    if test.range_non_inclusive(value, minimum, maximum):
        raise ValidationError(value, f"not be between {minimum} and {maximum} (non-inclusive)")


def eq(first: Any, second: Any) -> None:
    """Validate that a value is exactly equal to a second value, and if it isn't, raise an exception.

    :param Any first: The value to test.
    :param Any second: The value to test against.

    :raises ValidationError: Raised if the value isn't exactly equal to a second value.

    :rtype: None

    >>> eq("foo", "foo")
    >>> eq(42, 42)
    >>> eq(-123.45, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `-123.45` must be equal to `0`
    """
    if not test.eq(first, second):
        raise ValidationError(first, f"be equal to `{repr(second)}`")


def neq(first: Any, second: Any) -> None:
    """Validate that a value is not exactly equal to a second value, and if it is, raise an exception.

    :param Any first: The value to test.
    :param Any second: The value to test against.

    :raises ValidationError: Raised if the value is exactly equal to a second value.

    :rtype: None

    >>> neq("foo", "foo")
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `'foo'` must not be equal to `'foo'`
    >>> neq(42, 42)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must not be equal to `42`
    >>> neq(-123.45, 0)
    """
    if test.eq(first, second):
        raise ValidationError(first, f"not be equal to `{repr(second)}`")


def gt(first: int | float, second: int | float) -> None:
    """Validate that a value is greater than a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't greater than a second value.

    :rtype: None

    >>> gt(42, 0)
    >>> gt(0, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must be greater than `0`
    >>> gt(-123.45, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `-123.45` must be greater than `0`
    """
    if not test.gt(first, second):
        raise ValidationError(first, f"be greater than `{second}`")


def lt(first: int | float, second: int | float) -> None:
    """Validate that a value is less than a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't less than a second value.

    :rtype: None

    >>> lt(42, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be less than `0`
    >>> lt(0, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `0` must be less than `0`
    >>> lt(-123.45, 0)
    """
    if not test.lt(first, second):
        raise ValidationError(first, f"be less than `{second}`")


def gte(first: int | float, second: int | float) -> None:
    """Validate that a value is greater than or equal to a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't greater than or equal to a second value.

    :rtype: None

    >>> gte(42, 0)
    >>> gte(0, 0)
    >>> gte(-123.45, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `-123.45` must be greater than or equal to `0`
    """
    if not test.gte(first, second):
        raise ValidationError(first, f"be greater than or equal to `{second}`")


def lte(first: int | float, second: int | float) -> None:
    """Validate that a value is less than or equal to a second value, and if it isn't, raise an exception.

    :param int | float first: The value to test.
    :param int | float second: The value to test against.

    :raises ValidationError: Raised if the value isn't less than or equal to a second value.

    :rtype: None

    >>> lte(42, 0)
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be less than or equal to `0`
    >>> lte(0, 0)
    >>> lte(-123.45, 0)
    """
    if not test.lte(first, second):
        raise ValidationError(first, f"be less than or equal to `{second}`")
