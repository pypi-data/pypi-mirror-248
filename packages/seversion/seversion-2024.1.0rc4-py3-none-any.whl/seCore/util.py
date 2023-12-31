from typing import (
    ClassVar,
    Sequence,
)


class FancyEqMixin:
    """
    Mixin that implements C{__eq__} and C{__ne__}.

    Comparison is done using the list of attributes defined in
    C{compareAttributes}.
    """

    compareAttributes: ClassVar[Sequence[str]] = ()

    def __eq__(self, other: object) -> bool:
        if not self.compareAttributes:
            return self is other
        if isinstance(self, other.__class__):
            return all(
                getattr(self, name) == getattr(other, name)
                for name in self.compareAttributes
            )
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


__all__ = [
    "FancyEqMixin",
]
