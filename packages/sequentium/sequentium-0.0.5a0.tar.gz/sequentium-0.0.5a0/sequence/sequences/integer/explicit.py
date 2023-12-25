from sequence.core.infinite_type import Explicit
from sequence.core.infinite_type import MonotonicIncreasing
from sequence.sequences.integer.explicit_generalised_sequences import GeneralisedNexusNumbers


class A000027(Explicit):
    """The natural numbers (https://oeis.org/A000027)."""

    def __contains__(self, item):
        return True

    def __str__(self):
        return 'natural numbers'

    def formula(self, index: int) -> int:
        return index


PositiveIntegers = A000027
NaturalNumbers = A000027


class A000326(Explicit):
    """Pentagonal numbers (https://oeis.org/A000326)."""

    def __contains__(self, item):
        if item < 0:
            return False
        if item == 0:
            return True

        n = (1 + (1 + 24 * item) ** (1 / 2)) / 6
        return n == int(n)

    def __str__(self):
        return 'pentagonal numbers'

    def formula(self, index: int) -> int:
        return index * (3 * index - 1) // 2


PentagonalNumbers = A000326


class A001045(MonotonicIncreasing, Explicit):
    """Jacobsthal numbers (https://oeis.org/A001045)."""

    def __str__(self):
        return 'Jacobsthal numbers'

    def formula(self, index: int) -> int:
        return round(2 ** index / 3)


JacobsthalNumbers = A001045
JacobsthalSequence = A001045


class A003215(GeneralisedNexusNumbers):
    """Hex (or centered hexagonal) numbers (https://oeis.org/A003215)."""

    def __init__(self):
        super().__init__(dimension=2)

    def __str__(self):
        return 'hex numbers'

    def __contains__(self, item):
        if item <= 0:
            return False

        n = (3 + (12 * item - 3) ** (1 / 2)) / 6
        return n == int(n)


HexNumbers = A003215
CenteredHexagonalNumbers = A003215


class A005408(Explicit):
    """The odd numbers (https://oeis.org/A005408)."""

    def __contains__(self, item: int) -> bool:
        return item % 2 == 1

    def __str__(self):
        return 'odd numbers'

    def formula(self, index: int) -> int:
        return 2 * index + 1


OddNumbers = A005408


class A014551(MonotonicIncreasing, Explicit):
    """Jacobsthal-Lucas numbers (https://oeis.org/A014551)."""

    def __contains__(self, item):
        if item == 1:
            return True
        return super().__contains__(item=item)

    def __str__(self):
        return 'Jacobsthal-Lucas numbers'

    def formula(self, index: int) -> int:
        return 2**index + (-1)**index


JachobsthalLucasNumbers = A014551


class A033999(Explicit):
    """Sequence of powers of -1 (https://oeis.org/A033999)."""

    def __contains__(self, item):
        return item in {-1, 1}

    def __str__(self):
        return 'sequence of powers of -1'

    def formula(self, index: int) -> int:
        return (-1)**index
