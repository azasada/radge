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

    def test_connected(self):
        """Test whether the generated graph is connected."""
        TESTS = 100
        MAX_N = 7
        generator = random.sample([RandomGraph], counts=[100], k=TESTS)

        for i in range(TESTS):
            n = random.randint(1, MAX_N)
            m = random.randint(1, n * (n - 1) // 2)
            # graph = generator[i](n, m, directed=True, connected=True)

            vis = [False] * (n + 1)
            q = [1]
            while len(q) > 0:
                u = q.pop()
                vis[u] = True
                for v in range(1, n + 1):
                    if (u, v) in graph.edges.keys() and not vis[v]:
                        q.append(v)
            print(vis)

            print(graph)
            self.assertTrue(all(vis[1:]))


if __name__ == "__main__":
    unittest.main(failfast=True)
