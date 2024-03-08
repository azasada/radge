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

            self.assertTrue(tree.edge_cnt == vertex_cnt - 1)

            vis = [False] * (tree.vertex_cnt + 1)

            def dfs(v):
                vis[v] = True
                for edge in tree.edges[v]:
                    if not vis[edge.v]:
                        dfs(edge.v)
            dfs(1)
            self.assertTrue(all(vis[1:]))

    def test_dag(self):
        """Test if the generated graph is a directed acyclic graph."""
        TESTS = 100
        MAX_N = 500
        for _ in range(TESTS):
            vertex_cnt = random.randint(1, MAX_N)
            edge_cnt = random.randint(0, vertex_cnt * (vertex_cnt - 1) // 2)
            graph = dag(vertex_cnt, edge_cnt)

            in_deg = [0] * (graph.vertex_cnt + 1)
            for i in range(1, graph.vertex_cnt + 1):
                for edge in graph.edges[i]:
                    in_deg[edge.v] += 1
            q = []
            for i in range(1, graph.vertex_cnt + 1):
                if in_deg[i] == 0:
                    q.append(i)
            topo = []
            while q:
                v = q.pop()
                topo.append(v)
                for edge in graph.edges[v]:
                    in_deg[edge.v] -= 1
                    if in_deg[edge.v] == 0:
                        q.append(edge.v)
            self.assertTrue(len(topo) == graph.vertex_cnt)

    def test_connected(self):
        """Tests if the generated graph is connected."""
        TESTS = 1
        MAX_N = 10
        for _ in range(TESTS):
            vertex_cnt = random.randint(1, MAX_N)
            edge_cnt = random.randint(
                vertex_cnt - 1, vertex_cnt * (vertex_cnt - 1) // 2)
            graph = random_graph(vertex_cnt, edge_cnt, connected=True)

            vis = [False] * (graph.vertex_cnt + 1)

            def dfs(v):
                vis[v] = True
                for edge in graph.edges[v]:
                    if not vis[edge.v]:
                        dfs(edge.v)
            dfs(1)
            self.assertTrue(all(vis[1:]))


if __name__ == "__main__":
    unittest.main(failfast=True)
