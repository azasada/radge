"""
Generate graphs with various properties, including trees.
"""

import random
import math
from typing import Callable
from collections import defaultdict
import unittest


from utils import NOISE


class Tree:
    """Tree: a connected graph with no cycles."""

    def __init__(
        self, n: int, weighted: bool = False, weight_func: Callable[[], int] = lambda: 1
    ):
        """Initialize a tree with n nodes."""
        self.n = n
        self.weighted = weighted
        self.weight_func = weight_func

        self.edges = defaultdict(int)
        self.perm = list(range(1, n + 1))
        random.shuffle(self.perm)
        self.perm = [0] + self.perm

    def __str__(self) -> str:
        """Return the tree as a string.
        First line: n
        Next n-1 lines: edges
        """
        edges = list(self.edges.keys())
        random.shuffle(edges)

        ret_str = f"{self.n}"
        for u, v, w in edges:
            coin = random.randint(0, 1)
            ret_str += f"\n{self.perm[u * coin + v * (1 - coin)]} {self.perm[u * (1 - coin) + v * coin]}"
            if self.weighted:
                ret_str += f" {w}"
        return ret_str

    def add_edge(self, u: int, v: int):
        """Add an edge to the tree."""
        # edges are always triples (u, v, w) with u <= v
        if u > v:
            u, v = v, u
        self.edges[(u, v, self.weight_func())] += 1


class RandomTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a random tree using a Pruefer code."""
        super().__init__(n, **kwargs)
        if n == 1:
            return
        code = [random.randint(0, n - 1) for _ in range(n - 2)]
        deg = [1] * n
        for v in code:
            deg[v] += 1
        ptr = 0
        while deg[ptr] != 1:
            ptr += 1
        leaf = ptr

        for v in code:
            self.add_edge(leaf + 1, v + 1)
            deg[v] -= 1
            if deg[v] == 1 and v < ptr:
                leaf = v
            else:
                ptr += 1
                while deg[ptr] != 1:
                    ptr += 1
                leaf = ptr
        self.add_edge(leaf + 1, n)


class CaterpillarTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a caterpillar tree - a long trunk with small branches connected to it."""
        super().__init__(n, **kwargs)
        trunk_len = random.randint(self.n // 2, self.n)
        for i in range(2, trunk_len + 1):
            self.add_edge(i, i - 1)
        for i in range(trunk_len + 1, self.n + 1):
            self.add_edge(i, random.randint(1, trunk_len))


class StarTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a star tree - a couple of centers with all other nodes connected to them."""
        super().__init__(n, **kwargs)
        centers = random.randint(1, min(self.n, NOISE))
        for i in range(2, centers + 1):
            self.add_edge(i, i - 1)
        for i in range(centers + 1, self.n + 1):
            self.add_edge(i, random.randint(1, centers))


class CombTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a comb tree - a trunk with O(sqrt(n)) nodes, each one with an O(sqrt(n))-long branch."""

        def approx_sqrt(n: int) -> int:
            s = int(math.sqrt(n))
            if s > NOISE and s < n - NOISE:
                return s + random.randint(-NOISE, NOISE)
            return s

        super().__init__(n, **kwargs)
        trunk_len = approx_sqrt(self.n)
        for i in range(2, trunk_len + 1):
            self.add_edge(i, i - 1)
        new_node, branch_node, branch_len = trunk_len + 1, 1, 0
        while new_node <= self.n:
            if branch_len == approx_sqrt(self.n) and branch_node < trunk_len:
                branch_node += 1
                branch_len = 0
            if branch_len == 0:
                self.add_edge(branch_node, new_node)
            else:
                self.add_edge(new_node - 1, new_node)
            new_node += 1
            branch_len += 1


class BinaryTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a binary tree - O(log n) depth."""
        super().__init__(n, **kwargs)
        for i in range(2, self.n + 1):
            self.add_edge(i, i // 2)


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
                        1,
                    ) in tree.edges.keys() and not vis[v]:
                        q.append(v)
            self.assertTrue(tree.n == n and len(tree.edges)
                            == n - 1 and all(vis[1:]))


class Graph(Tree):
    pass


if __name__ == "__main__":
    unittest.main()
