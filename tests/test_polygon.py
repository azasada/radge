import random
import unittest

from radge.polygon import *


class TestPolygon(unittest.TestCase):
    def test_polygon(self):
        poly = random_convex(5)
        # TODO: this test
        self.assertTrue(True)
