import random
import unittest

from radge.sequences import *


class TestSequence(unittest.TestCase):
    def test_seq(self):
        """Test if the elements of the generated sequence are contained in the original one."""
        for _ in range(100):
            n = random.randint(1, 100)
            a = range(1_000_000_000)
            self.assertTrue(all(x in a for x in seq(n, a)))

    def test_seq_unique(self):
        """Test if the elements of the generated sequence are unique."""
        for _ in range(100):
            n = random.randint(1, 100)
            a = range(1_000_000_000)
            self.assertEqual(len(seq_unique(n, a)), n)
        self.assertRaises(IndexError, seq_unique, 100, range(10))

    def test_perm(self):
        """Test if the generated seuqence is a permutation."""
        for _ in range(100):
            n = random.randint(1, 100_000)
            self.assertEqual(sorted(perm(n)), list(range(1, n + 1)))


if __name__ == "__main__":
    unittest.main(failfast=True)
