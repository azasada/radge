import random
import unittest

from radge.sequences import *

TESTS = 100
MAX_LEN = 1000
MAX_N = 1_000_000_000


class TestSequence(unittest.TestCase):
    def test_seq(self):
        """Test if the elements of the generated sequence are contained in the original one."""
        for i in range(TESTS):
            random.seed(i)
            n = random.randint(1, MAX_LEN)
            a = range(MAX_N)
            self.assertTrue(all(x in a for x in seq(n, a)))

    def test_seq_unique(self):
        """Test if the elements of the generated sequence are unique."""
        for i in range(TESTS):
            random.seed(i)
            n = random.randint(1, MAX_LEN)
            a = range(MAX_N)
            self.assertEqual(len(seq_unique(n, a)), n)
        self.assertRaises(IndexError, seq_unique, 5, range(4))

    def test_perm(self):
        """Test if the generated seuqence is a permutation."""
        for i in range(TESTS):
            random.seed(i)
            n = random.randint(1, MAX_LEN)
            self.assertEqual(sorted(perm(n)), list(range(1, n + 1)))


if __name__ == "__main__":
    unittest.main(failfast=True)
