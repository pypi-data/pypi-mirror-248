"""An ultra-lightweight package for validating single conditions.

>>> import onecondition as oc
>>> oc.validate.not_negative(42)
>>> oc.validate.range_non_inclusive(0, 0, 1)
Traceback (most recent call last):
    ...
onecondition.validate.ValidationError: Value `0` must be between 0 and 1 (non-inclusive)
"""

__version__ = "0.3.0"

from onecondition.validate import ValidationError
