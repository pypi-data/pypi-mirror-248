# nullability

Pass nullable arguments that may not exist.

[![PyPI version](https://img.shields.io/pypi/v/nullability.svg)](https://pypi.org/project/nullability)

### Usage

```python
>>> Nullable(1).value
1

>>> print(Nullable(None).value)
None

>>> Nullable.if_not_none(1)
Nullable(value=1)

>>> print(Nullable.if_not_none(None))
None
```

### Usecase example:

```python
>>> from dataclasses import dataclass
>>> from typing import Optional
>>> from nullability import Nullable

>>> @dataclass
... class Foo:
...     bar: Optional[int]
...     baz: Optional[int]
...
...     def update(
...         self,
...         bar: Optional[Nullable[int]]=None,
...         baz: Optional[Nullable[int]]=None,
...     ):
...         if bar:
...             self.bar = bar.value
...         if baz:
...             self.baz = baz.value
...         return self

>>> foo = Foo(bar=1, baz=2)

>>> foo.update(bar=Nullable(3))
Foo(bar=3, baz=2)

>>> foo.update(baz=Nullable(None))
Foo(bar=3, baz=None)

>>> foo.update(bar=Nullable.if_not_none(None))
Foo(bar=3, baz=None)

>>> foo.update(bar=Nullable.if_not_none(4))
Foo(bar=4, baz=None)
```
