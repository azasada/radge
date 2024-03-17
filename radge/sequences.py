"""
Sequences, permutations and so on.
"""

import random
from typing import Any, Callable, Optional


def seq(n: int, a: range, key: Optional[Callable[[int], Any]] = None) -> list:
    """Pick n random items from a range (possibly with repetitions).
    Optionally sort the resulting sequence using the key(x) function
    (takes in x, and returns the value that x should be compared by)."""
    ret = [random.choice(a) for _ in range(n)]
    random.shuffle(ret)
    if key:
        ret.sort(key=key)
    return ret


def seq_unique(n: int, a: range, key: Optional[Callable[[int], Any]] = None) -> list:
    """Pick n unique random items from a range.
    Optionally sort the resulting sequence using the key(x) function
    (takes in x, and returns the value that x should be compared by)."""
    if len(a) < n:
        raise IndexError(
            f"Can't pick {n} distinct elements from a range of length {len(a)}."
        )
    ret = random.sample(a, n)
    if key:
        ret.sort(key=key)
    return ret


def perm(n: int, key: Optional[Callable[[int], Any]] = None) -> list:
    """Return a random permutatation of the set {1,2,...,n}.
    Optionally sort the resulting sequence using the key(x) function
    (takes in x, and returns the value that x should be compared by)."""
    ret = list(range(1, n + 1))
    if key:
        ret.sort(key=key)
    else:
        random.shuffle(ret)
    return ret
