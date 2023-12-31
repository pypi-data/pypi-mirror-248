"""An ultra-lightweight package for validating single conditions.

>>> import onecondition as oc
>>> oc.validate.not_negative(42)
>>> oc.validate.range_non_inclusive(0, 0, 1)
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `0` must be between 0 and 1 (non-inclusive)
"""

__version__ = "1.0.1"

# TODO: https://docs.python.org/2/library/doctest.html#unittest-api

from typing import Any


class ValidationError(ValueError):
    """A subclass of ValueError, this is raised any time a validation check fails.

    >>> raise ValidationError(42, "be the answer to life, the universe, and everything")
    Traceback (most recent call last):
        ...
    onecondition.ValidationError: Value `42` must be the answer to life, the universe, and everything
    """
    def __init__(
            self,
            value: Any,
            condition: str,
            message_format: str = "Value `{value_repr}` must {condition}"
    ):
        message = message_format.format(
            value=value,
            value_repr=repr(value),
            condition=condition)
        super().__init__(message)

