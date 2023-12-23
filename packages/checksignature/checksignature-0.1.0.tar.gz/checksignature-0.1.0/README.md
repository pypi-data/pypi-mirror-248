# checksignature
> a function decorator for enforcing function signatures

[![tests](https://github.com/withtwoemms/checksignature/workflows/tests/badge.svg)](https://github.com/withtwoemms/checksignature/actions?query=workflow%3Atests)
[![publish](https://github.com/withtwoemms/checksignature/workflows/publish/badge.svg)](https://github.com/withtwoemms/checksignature/actions?query=workflow%3Apublish)
[![codecov](https://codecov.io/gh/withtwoemms/checksignature/branch/main/graph/badge.svg?token=95KK3WG5QW)](https://codecov.io/gh/withtwoemms/checksignature)

# Setup
Install build dependencies.
```
pip install -r requirements
```
Run [`nox`](https://nox.thea.codes/en/stable/) to build, install, and run `checksignature` tests.

# Usage

Decorate any funciton with `@checksignature`.
```python
@checksignature
def function(a: str, b: int, c, *args: int, **kwargs: int)::
    return a, b, c, args, kwargs
```
Upon invocation of `function`, the signature check is evaluated.
```python
function('one', 2, 3.0, 1, 2, 3, **{'four': 4})   #=> functions as usual--no problem.
function('one', 2, 3.0, 1, 2, 3, **{'four': 4.0}) #=> raises a TypeError
function('one', 2, 'x', 1, 2, 3, **{'four': 4})   #=> raises a TypeError
```
