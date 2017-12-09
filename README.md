# firanka

[![Build Status](https://travis-ci.org/smok-serwis/firanka.svg)](https://travis-ci.org/smok-serwis/firanka)
[![Maintainability](https://api.codeclimate.com/v1/badges/97a30fdc35e61f8d7c86/maintainability)](https://codeclimate.com/github/smok-serwis/firanka/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/97a30fdc35e61f8d7c86/test_coverage)](https://codeclimate.com/github/smok-serwis/firanka/test_coverage)
[![PyPI version](https://badge.fury.io/py/firanka.svg)](https://badge.fury.io/py/firanka)
[![PyPI](https://img.shields.io/pypi/pyversions/firanka.svg)]()
[![PyPI](https://img.shields.io/pypi/implementation/firanka.svg)]()
[![PyPI](https://img.shields.io/pypi/wheel/firanka.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

firanka is a Python library to perform calculations on particular kinds of
functions. These functions have a domain, which is a single continuous subset
of the real number line. These functions can have any values.

firanka allows you do define two classes of such functions or series.

First are the _DiscreteSeries_. _DiscreteSeries_ further divide the function
domain into slices (left-closed, right-open) that have constant values.
Manipulating _DiscreteSeries_ and performing calculations on them is cheap.

Then you have _FunctionSeries_. These are simply defined by user-supplied
Python callable.

Best part is, you can join series together (given a joining operator),
slice them and so on.


# Usage
## Ranges

```python
from firanka.series import Range
```

Range would have been better called an **interval**. It is a continuous subset
of the real number line.

You can create Ranges as follows:

```python
Range(-5, 5, True, False) == Range('<-5;5)')
```

First boolean argument signifies whether the interval is left-closed,
and second whether it is right-closed.

Range's are immutable and hashable. They can be sliced:

```python
Range('<-5;5>')[0:] == Range('<0;5>')
```

You can check whether a range contains a point

```python
5 not in Range('<-1;5)')
```

Or you can check for strict inclusion

```python
Range('<-1;1>') in Range('<-2;2>')
```

