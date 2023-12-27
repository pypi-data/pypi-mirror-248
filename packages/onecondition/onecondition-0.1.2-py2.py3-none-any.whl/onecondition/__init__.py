"""An ultra-lightweight package for validating single conditions."""

__version__ = "0.1.2"

from dataclasses import dataclass
from typing import Any


@dataclass
class Test:
    """A data class containing methods to test various conditions about 1 or more values."""
    @staticmethod
    def none(value: Any) -> bool:
        """Tests if a value is None.

        :param Any value: The value to test.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return value is None

    @staticmethod
    def specific_type(value: Any, value_type: type) -> bool:
        """Tests if a value is a specific type (do not consider inheritance).

        :param Any value: The value to test.
        :param type value_type: The type to test the value against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return type(value) is value_type

    @staticmethod
    def instance(value: Any, value_type: type) -> bool:
        """Tests if a value is an instance (the same as or a subclass) of a specific type.

        :param Any value: The value to test.
        :param type value_type: The type to test the value against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return isinstance(value, value_type)

    @staticmethod
    def zero(value: int | float) -> bool:
        """Tests if a value is exactly equal to 0.

        :param int | float value: The value to test.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return value == 0

    @staticmethod
    def positive(value: int | float) -> bool:
        """Tests if a value is positive (non-zero).

        :param int | float value: The value to test.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return value > 0

    @staticmethod
    def negative(value: int | float) -> bool:
        """Tests if a value is negative (non-zero).

        :param int | float value: The value to test.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return value < 0

    @staticmethod
    def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> bool:
        """Tests if a value is within a specified range (inclusive).

        :param int | float value: The value to test.
        :param int | float minimum: The minimum value to test against.
        :param int | float maximum: The maximum value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return minimum <= value <= maximum

    @staticmethod
    def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> bool:
        """Tests if a value is within a specified range (non-inclusive).

        :param int | float value: The value to test.
        :param int | float minimum: The minimum value to test against.
        :param int | float maximum: The maximum value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return minimum < value < maximum

    @staticmethod
    def eq(first: int | float, second: int | float) -> bool:
        """Tests if a value is exactly equal to a second value.

        :param int | float first: The value to test.
        :param int | float second: The value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return first == second

    @staticmethod
    def gt(first: int | float, second: int | float) -> bool:
        """Tests if a value is greater than a second value.

        :param int | float first: The value to test.
        :param int | float second: The value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return first > second

    @staticmethod
    def lte(first: int | float, second: int | float) -> bool:
        """Tests if a value is less than or equal to a second value.

        :param int | float first: The value to test.
        :param int | float second: The value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return first <= second

    @staticmethod
    def lt(first: int | float, second: int | float) -> bool:
        """Tests if a value is less than a second value.

        :param int | float first: The value to test.
        :param int | float second: The value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return first < second

    @staticmethod
    def gte(first: int | float, second: int | float) -> bool:
        """Tests if a value is greater than or equal to a second value.

        :param int | float first: The value to test.
        :param int | float second: The value to test against.

        :return: The result of the evaluation.
        :rtype: bool
        """
        return first >= second


class ValidationError(ValueError):
    """A subclass of ValueError, this is raised any time a validation check fails."""
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(message)


@dataclass
class Validate:
    """A data class containing methods to validate various conditions about 1 or more values."""
    @staticmethod
    def none(value: Any) -> None:
        if Test.none(value):
            raise ValidationError(f"Value '{value}' must be None")

    @staticmethod
    def not_none(value: Any) -> None:
        if not Test.none(value):
            raise ValidationError(f"Value must not be None")

    @staticmethod
    def specific_type(value: Any, value_type: type) -> None:
        if not Test.specific_type(value, value_type):
            raise ValidationError(f"Value '{value}' must be of type {value_type}, not {type(value)}")

    @staticmethod
    def not_specific_type(value: Any, value_type: type) -> None:
        if Test.type(value, value_type):
            raise ValidationError(f"Value '{value}' must be not of type {value_type}")

    @staticmethod
    def instance(value: Any, value_type: type) -> None:
        if not Test.instance(value, value_type):
            raise ValidationError(f"Value '{value}' must be an instance of {value_type}, not a {type(value)}")

    @staticmethod
    def not_instance(value: Any, value_type: type) -> None:
        if Test.instance(value, value_type):
            raise ValidationError(f"Value '{value}' must not be an instance of {value_type}")

    @staticmethod
    def zero(value: int | float) -> None:
        if not Test.zero(value):
            raise ValidationError(f"Value '{value}' must be zero")

    @staticmethod
    def not_zero(value: int | float) -> None:
        if Test.zero(value):
            raise ValidationError(f"Value '{value}' must not be zero")

    @staticmethod
    def positive(value: int | float) -> None:
        if not Test.positive(value):
            raise ValidationError(f"Value '{value}' must be positive (non-zero)")

    @staticmethod
    def not_positive(value: int | float) -> None:
        if Test.positive(value):
            raise ValidationError(f"Value '{value}' must not be positive")

    @staticmethod
    def negative(value: int | float) -> None:
        if not Test.negative(value):
            raise ValidationError(f"Value '{value}' must be negative (non-zero)")

    @staticmethod
    def not_negative(value: int | float) -> None:
        if Test.negative(value):
            raise ValidationError(f"Value '{value}' must not be negative")

    @staticmethod
    def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
        if not Test.range_inclusive(value, minimum, maximum):
            raise ValidationError(f"Value '{value}' must be between {minimum} and {maximum} (inclusive)")

    @staticmethod
    def not_range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
        if Test.range_inclusive(value, minimum, maximum):
            raise ValidationError(f"Value '{value}' must not be between {minimum} and {maximum} (inclusive)")

    @staticmethod
    def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
        if not Test.range_non_inclusive(value, minimum, maximum):
            raise ValidationError(f"Value '{value}' must be between {minimum} and {maximum} (non-inclusive)")

    @staticmethod
    def not_range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
        if Test.range_non_inclusive(value, minimum, maximum):
            raise ValidationError(f"Value '{value}' must not be between {minimum} and {maximum} (non-inclusive)")

    @staticmethod
    def eq(first: int | float, second: int | float) -> None:
        if not Test.eq(first, second):
            raise ValidationError(f"Value '{first}' must be equal to '{second}'")

    @staticmethod
    def neq(first: int | float, second: int | float) -> None:
        if Test.eq(first, second):
            raise ValidationError(f"Value '{first}' must not be equal to '{second}'")

    @staticmethod
    def gt(first: int | float, second: int | float) -> None:
        if not Test.gt(first, second):
            raise ValidationError(f"Value '{first}' must be greater than '{second}'")

    @staticmethod
    def lte(first: int | float, second: int | float) -> None:
        if not Test.lte(first, second):
            raise ValidationError(f"Value '{first}' must be less than or equal to '{second}'")

    @staticmethod
    def lt(first: int | float, second: int | float) -> None:
        if not Test.lt(first, second):
            raise ValidationError(f"Value '{first}' must be less than '{second}'")

    @staticmethod
    def gte(first: int | float, second: int | float) -> None:
        if not Test.gte(first, second):
            raise ValidationError(f"Value '{first}' must be greater than or equal to '{second}'")
