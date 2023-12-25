from typing import Any

from sequence.sequences.integer.recursive_generalised_sequences import (
    HighOrderFibonacciNumbers,
    LucasSequenceU,
    LucasSequenceV,
)


class A000032(LucasSequenceV):
    """Lucas numbers (https://oeis.org/A000032)."""

    def __init__(self):
        super().__init__(p=1, q=-1)

    def __str__(self):
        return 'Lucas numbers'

    def __contains__(self, item: Any) -> bool:
        if item == 1:
            return True
        return super().__contains__(item=item)


LucasNumbers = A000032


class A000045(LucasSequenceU):
    """Fibonacci numbers (https://oeis.org/A000045)."""

    def __init__(self):
        super().__init__(p=1, q=-1)

    def __str__(self):
        return 'Fibonacci numbers'


FibonacciNumbers = A000045
FibonacciSequence = A000045


class A000073(HighOrderFibonacciNumbers):
    """Tribonacci numbers (https://oeis.org/A000073)."""

    def __init__(self):
        super().__init__(order=3)

    def __str__(self):
        return 'Tribonacci numbers'


TribonacciNumbers = A000073


class A000078(HighOrderFibonacciNumbers):
    """Tetranacci numbers (https://oeis.org/A000078)."""

    def __init__(self):
        super().__init__(order=4)

    def __str__(self):
        return 'Tetranacci numbers'


TetranacciNumbers = A000078


class A000129(LucasSequenceU):
    """Pell numbers (https://oeis.org/A000129)."""

    def __init__(self):
        super().__init__(p=2, q=-1)

    def __str__(self):
        return 'Pell numbers'


PellNumbers = A000129
LambdaNumbers = A000129


class A001591(HighOrderFibonacciNumbers):
    """Pentanacci numbers (https://oeis.org/A001591)."""
    def __init__(self):
        super().__init__(order=5)

    def __str__(self):
        return 'Pentanacci numbers'


PentanacciNumbers = A001591


class A001592(HighOrderFibonacciNumbers):
    """Hexanacci numbers (https://oeis.org/A001592)."""
    def __init__(self):
        super().__init__(order=6)

    def __str__(self):
        return 'Hexanacci numbers'


HexanacciNumbers = A001591


class A002203(LucasSequenceV):
    """Companion Pell numbers (https://oeis.org/A002203)."""
    def __init__(self):
        super().__init__(p=2, q=-1)

    def __str__(self):
        return 'Companion Pell numbers'


CompanionPellNumbers = A002203
PellLucasNumbers = A002203


class A079262(HighOrderFibonacciNumbers):
    """Octanacci numbers (https://oeis.org/A079262)."""
    def __init__(self):
        super().__init__(order=8)

    def __str__(self):
        return 'Octanacci numbers'


OctanacciNumbers = A079262


class A104144(HighOrderFibonacciNumbers):
    """Enneanacci numbers (https://oeis.org/A104144)."""
    def __init__(self):
        super().__init__(order=9)

    def __str__(self):
        return 'Enneanacci numbers'


EnneanacciNumebrs = A104144


class A122189(HighOrderFibonacciNumbers):
    """Heptanacci numbers (https://oeis.org/A122189)."""
    def __init__(self):
        super().__init__(order=7)

    def __str__(self):
        return 'Heptanacci numbers'


HeptanacciNumbers = A122189


class A214733(LucasSequenceU):
    """Sequence A214733 (https://oeis.org/A214733)."""

    def __init__(self):
        super().__init__(p=-1, q=3)

    def __str__(self):
        return 'sequence A214733'

    def __contains__(self, item):
        if item == 0:
            return True
        for element in self._as_generator():
            if element == item:
                return True
            if abs(element) > abs(item * 1_000):
                return False
        return None
