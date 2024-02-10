"""
Utility functions and constants
"""

import random
from typing import Optional, Callable, Any
import unittest

NOISE = 4


def seq(n: int, a: range, key: Optional[Callable[[int], Any]] = None) -> list:
    """Pick n random items from a generator (possibly with repetitions).
    Optionally sort the resulting sequence using the key(x) function 
    (takes in x, and returns the value that x should be compared by)."""
    ret = [random.choice(a) for _ in range(n)]
    random.shuffle(ret)
    if key:
        ret.sort(key=key)
    return ret


def seq_unique(n: int, a: range, key: Optional[Callable[[int], Any]] = None) -> list:
    """Pick n distinct random items from a generator.
    Optionally sort the resulting sequence using the key(x) function 
    (takes in x, and returns the value that x should be compared by)."""
    if len(a) < n:
        raise IndexError(
            f"Can't pick {n} distinct elements from a range of length {len(a)}.")
    ret = random.sample(a, n)
    if key:
        ret.sort(key=key)
    return ret


class TestSequence(unittest.TestCase):
    def test_seq(self):
        for _ in range(100):
            n = random.randint(1, 100)
            a = range(1_000_000_000)
            self.assertTrue(all(x in a for x in seq(n, a)))

    def test_seq_unique(self):
        for _ in range(100):
            n = random.randint(1, 100)
            a = range(1_000_000_000)
            self.assertEqual(len(seq_unique(n, a)), n)
        self.assertRaises(IndexError, seq_unique, 100, range(10))


if __name__ == "__main__":
    unittest.main()
