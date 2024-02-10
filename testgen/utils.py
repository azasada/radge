"""
Utility functions and constants
"""

import random
from typing import Optional, Callable, TypeVar, Any
import unittest
from unittest.main import main

NOISE = 4

T = TypeVar("T")


def seq(n: int, src: list[T], key: Optional[Callable[[T], Any]] = None) -> list:
    """Pick n random items from list (possibly with repetitions).
    Optionally sort the resulting sequence using the key(x) function 
    (takes in x, and returns the value that x should be compared by)."""
    if len(src) == 0:
        raise IndexError("Can't pick from an empty sequence.")
    ret = [random.choice(src) for _ in range(n)]
    if key:
        ret.sort(key=key)
    return ret


class TestSequence(unittest.TestCase):
    def test_seq(self):
        a = [1, 5, -1, 2, 7, 3]
        print(seq(3, a, lambda x: -x))

if __name__ == "__main__":
    unittest.main()
