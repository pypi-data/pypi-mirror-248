"""
Compatibility module to provide backwards compatibility for useful Python
features.

This is mainly for use of internal code. We encourage you to use
the latest version of Python directly from your code, if possible.
"""

from typing import Any, cast


# type note: Can't find a Comparable type, despite
# https://github.com/python/typing/issues/59
def cmp(a: object, b: object) -> int:
    """
    Compare two objects.

    Returns a negative number if C{a < b}, zero if they are equal, and a
    positive number if C{a > b}.
    """
    if a < b:  # type: ignore[operator]
        return -1
    elif a == b:
        return 0
    else:
        return 1


def comparable(klass):
    """
    Class decorator that ensures support for the special C{__cmp__} method.

    C{__eq__}, C{__lt__}, etc. methods are added to the class, relying on
    C{__cmp__} to implement their comparisons.
    """

    def __eq__(self: Any, other: object) -> bool:
        c = cast(bool, self.__cmp__(other))
        if c is NotImplemented:
            return c
        return c == 0

    def __ne__(self: Any, other: object) -> bool:
        c = cast(bool, self.__cmp__(other))
        if c is NotImplemented:
            return c
        return c != 0

    def __lt__(self: Any, other: object) -> bool:
        c = cast(bool, self.__cmp__(other))
        if c is NotImplemented:
            return c
        return c < 0

    def __le__(self: Any, other: object) -> bool:
        c = cast(bool, self.__cmp__(other))
        if c is NotImplemented:
            return c
        return c <= 0

    def __gt__(self: Any, other: object) -> bool:
        c = cast(bool, self.__cmp__(other))
        if c is NotImplemented:
            return c
        return c > 0

    def __ge__(self: Any, other: object) -> bool:
        c = cast(bool, self.__cmp__(other))
        if c is NotImplemented:
            return c
        return c >= 0

    klass.__lt__ = __lt__
    klass.__gt__ = __gt__
    klass.__le__ = __le__
    klass.__ge__ = __ge__
    klass.__eq__ = __eq__
    klass.__ne__ = __ne__
    return klass


__all__ = [
    "cmp",
    "comparable",
]
