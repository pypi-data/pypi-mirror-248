# 1️⃣ OneCondition
### An ultra-lightweight package for validating single conditions.

## Usage
```doctest
>>> import onecondition as oc

>>> def inverse(user_input):
...     oc.validate.instance(user_input, (int, float))
...     oc.validate.positive(user_input)
...     return 1 / user_input

>>> inverse(4)
0.25
>>> inverse(0)
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `0` must be positive (non-zero)
>>> inverse("foobar")
Traceback (most recent call last):
    ...
onecondition.ValidationError: Value `'foobar'` must be an instance of (<class 'int'>, <class 'float'>), not a <class 'str'>

```

# Full Documentation
<p align="center"><a href="https://onecondition.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="onecondition on Read the Docs"></a></p>
