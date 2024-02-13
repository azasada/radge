import random
import unittest

from radge.graph import *


class TestTree(unittest.TestCase):
    def test_is_tree(self):
        """Test if the generated graph is a tree."""
        TESTS = 100
        MAX_N = 500
        tree_generators = [random_tree, binary_tree,
                           caterpillar_tree, star_path_tree, comb_tree]
        for _ in range(TESTS):
            vertex_cnt = random.randint(1, MAX_N)
            generator = random.choice(tree_generators)
            if generator == star_path_tree:
                self.assertRaises(ValueError, generator,
                                  vertex_cnt, vertex_cnt + 1)
                star_cnt = random.randint(1, vertex_cnt)
                tree = generator(vertex_cnt, star_cnt)
            else:
                tree = generator(vertex_cnt)

            print(tree)
            self.assertTrue(tree.edge_cnt == vertex_cnt - 1)

            vis = [False] * (tree.vertex_cnt + 1)

            def dfs(v):
                vis[v] = True
                for edge in tree.edges[v]:
                    if not vis[edge.v]:
                        dfs(edge.v)
            dfs(1)
            self.assertTrue(all(vis[1:]))


if __name__ == "__main__":
    unittest.main(failfast=True)
