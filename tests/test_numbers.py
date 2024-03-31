import math
import unittest

from radge.numbers import *

TESTS = 1000
MAX_N = 1_000_000_000


class TestNumbers(unittest.TestCase):
    def test_random_prime(self):
        """Test if the generated number is a prime."""
        num_gen = Numbers(MAX_N)
        for i in range(TESTS):
            random.seed(i)
            p = num_gen.random_prime()
            self.assertTrue(p > 1)
            self.assertTrue(p < MAX_N)
            self.assertTrue(all(p % i != 0 for i in range(2, math.isqrt(p) + 1)))


if __name__ == "__main__":
    unittest.main(failfast=True)
