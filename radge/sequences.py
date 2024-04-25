"""
Sequences, permutations and so on.
"""

import random
from typing import Any, Callable, Optional
import radge.utils as utils


def seq(n: int, a: range, key: Optional[Callable[[int], Any]] = None) -> list:
    """Pick n random items from range a (possibly with repetitions).
    Optionally sort the resulting sequence using the key(x) function
    (takes in x, and returns the value that x should be compared by)."""
    random.seed(utils.SEED)
    ret = [random.choice(a) for _ in range(n)]
    random.shuffle(ret)
    if key:
        ret.sort(key=key)
    return ret


def seq_unique(n: int, a: range, key: Optional[Callable[[int], Any]] = None) -> list:
    """Pick n unique random items from range a.
    Optionally sort the resulting sequence using the key(x) function
    (takes in x, and returns the value that x should be compared by)."""
    if len(a) < n:
        raise IndexError(
            f"Can't pick {n} distinct elements from a range of length {len(a)}."
        )
    random.seed(utils.SEED)
    ret = random.sample(a, n)
    if key:
        ret.sort(key=key)
    return ret


def perm(n: int, key: Optional[Callable[[int], Any]] = None) -> list:
    """Return a random permutatation of the set {1,2,...,n}.
    Optionally sort the resulting sequence using the key(x) function
    (takes in x, and returns the value that x should be compared by)."""
    random.seed(utils.SEED)
    ret = list(range(1, n + 1))
    if key:
        ret.sort(key=key)
    else:
        random.shuffle(ret)
    return ret
