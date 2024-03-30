import random
import unittest

from radge.polygon import *


def is_convex_angle(v: Vector, w: Vector) -> bool:
    return v.x * w.y - v.y * w.x >= 0


class TestPolygon(unittest.TestCase):
    def test_convex(self):
        """Test if the generated polygon is convex."""
        TESTS = 1000
        MAX_N = 1000

        for test in range(TESTS):
            random.seed(test)
            n = random.randint(3, MAX_N)
            poly = random_convex(n)
            v = poly[1] - poly[0]
            for i in range(2, n):
                w = poly[i] - poly[i - 1]
                self.assertTrue(is_convex_angle(v, w))
                v = w
