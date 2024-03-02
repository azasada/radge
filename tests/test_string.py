import random
import unittest

from radge.string import *
from radge.utils import ALPHA_LOWER


class TestString(unittest.TestCase):
    def test_random_string(self):
        """Test if the generated string comes from the given alphabet."""
        for _ in range(100):
            n = random.randint(1, 100)
            s = String(n, ALPHA_LOWER)
            self.assertEqual(s.len, n)
            self.assertTrue(all(c in ALPHA_LOWER for c in s.s))

if __name__ == "__main__":
    unittest.main(failfast=True)
