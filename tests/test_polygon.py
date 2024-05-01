import random
import unittest

from radge.polygon import *


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
            cross_products = []
            for i in range(2, len(poly)):
                w = poly[i] - poly[i - 1]
                cross_products.append(v.cross(w))
                v = w
            self.assertTrue(min(cross_products) * max(cross_products) >= 0)


if __name__ == "__main__":
    unittest.main(failfast=True)
