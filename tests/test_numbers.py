import math
import unittest

from radge.numbers import *


class TestNumbers(unittest.TestCase):
    def test_random_prime(self):
        """Test if the generated number is a prime."""
        max_n = 1_000_000_000
        num_gen = Numbers(max_n)
        for _ in range(1_000):
            p = num_gen.random_prime()
            self.assertTrue(p > 1)
            self.assertTrue(p < max_n)
            self.assertTrue(all(p % i != 0 for i in range(2, math.isqrt(p) + 1)))


if __name__ == "__main__":
    unittest.main(failfast=True)
