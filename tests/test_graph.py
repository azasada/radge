import random
import unittest

from radge.graph import *


class TestTree(unittest.TestCase):
    def test_is_tree(self):
        """Test whether whatever was generated is, in fact, a tree."""
        TESTS = 100
        MAX_N = 300
        generator = random.sample([CombTree], counts=[100], k=TESTS)

        for i in range(TESTS):
            n = random.randint(1, MAX_N)
            tree = generator[i](n)

            vis = [False] * (n + 1)
            q = [1]
            while len(q) > 0:
                u = q.pop()
                vis[u] = True
                for v in range(1, n + 1):
                    if (
                        u * (u < v) + v * (v < u),
                        v * (u < v) + u * (v < u),
                    ) in tree.edges.keys() and not vis[v]:
                        q.append(v)
            self.assertTrue(tree.n == n and len(tree.edges)
                            == n - 1 and all(vis[1:]))


if __name__ == '__main__':
    unittest.main(failfast=True)
