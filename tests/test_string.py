import random
import unittest

from radge.string import *
from radge.utils import ALPHA_LOWER

MAX_N = 100
MAX_LEN = 1000


class TestString(unittest.TestCase):
    def test_random_string(self):
        """Test if the generated string comes from the given alphabet."""
        for _ in range(MAX_N):
            n = random.randint(1, MAX_LEN)
            s = String(n, ALPHA_LOWER)
            self.assertEqual(s.len, n)
            self.assertTrue(all(c in ALPHA_LOWER for c in s.s))

    def test_substring(self):
        """Test if the generated substring is contained within the original string."""
        for _ in range(MAX_N):
            n = random.randint(1, MAX_LEN)
            s = String(n, ALPHA_LOWER)
            for _ in range(MAX_LEN):
                l = random.randint(1, n)
                sub = s.substr(l)
                self.assertEqual(len(sub), l)

                ok = False
                for i in range(n - l + 1):
                    if s.s[i : (i + l)] == sub:
                        ok = True
                self.assertTrue(ok)

    def test_subsequence(self):
        """Test if the generated subsequence is contained within the original string."""
        for _ in range(MAX_N):
            n = random.randint(1, MAX_LEN)
            s = String(n, ALPHA_LOWER)
            for _ in range(MAX_N):
                l = random.randint(1, n)
                sub = s.subseq(l)
                self.assertEqual(len(sub), l)

                cnt, next_pos = 0, 0
                for c in sub:
                    found = False
                    for i in range(next_pos, n):
                        if s.s[i] == c:
                            found = True
                            cnt += 1
                            next_pos = i + 1
                            break
                    if not found:
                        break
                self.assertTrue(cnt == l)


if __name__ == "__main__":
    unittest.main(failfast=True)
