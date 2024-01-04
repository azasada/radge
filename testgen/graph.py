"""
Generate graphs with various properties, including trees.
"""

import random
import math
from types import ClassMethodDescriptorType
from typing import Callable, ClassVar
from collections import defaultdict
import unittest


class Tree:
    def __init__(self, n: int, weighted: bool = False, weight_func: Callable[[], int] = lambda: 1):
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
        for (u, v, w) in edges:
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
        trunk = random.randint(self.n // 2, self.n)
        for i in range(2, trunk + 1):
            self.add_edge(i, i - 1)
        for i in range(trunk + 1, self.n + 1):
            self.add_edge(i, random.randint(1, trunk))


class StarTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a star tree - a couple of centers with all other nodes connected to them."""
        super().__init__(n, **kwargs)
        centers = random.randint(1, min(4, self.n))
        for i in range(2, centers + 1):
            self.add_edge(i, i - 1)
        for i in range(centers + 1, self.n + 1):
            self.add_edge(i, random.randint(1, centers))


class CombTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a comb tree - a trunk with O(sqrt(n)) nodes, each one with an O(sqrt(n))-long branch."""
        def circa_root(n: int) -> int:
            return int(math.sqrt(n)) + random.randint(-max(n - 1, 4), max(n - 1, 4))

        super().__init__(n, **kwargs)
        trunk = circa_root(self.n)
        for i in range(2, trunk + 1):
            self.add_edge(i, i - 1)
        node = trunk + 1
        for v in range(1, trunk + 1):
            branch = circa_root(self.n)
            # TODO: finish this


class BinaryTree(Tree):
    def __init__(self, n: int, **kwargs):
        """Initialize a binary tree - O(log n) depth."""
        super().__init__(n, **kwargs)
        for i in range(2, self.n + 1):
            self.add_edge(i, i // 2)


class TestTreeGeneration(unittest.TestCase):
    def test_is_tree(self):
        TESTS = 100
        MAX_N = 200
        generator = random.sample([RandomTree, CaterpillarTree, StarTree, BinaryTree], counts = [70, 10, 10, 10], k = TESTS)

        for i in range(TESTS):
            n = random.randint(1, MAX_N)
            tree = generator[i](n)
            # print(tree)

            # tree = connected graph with n vertices and n - 1 edges
            vis = [False] * (n + 1)
            q = [1]
            while len(q) > 0:
                u = q.pop()
                vis[u] = True
                for v in range(1, n + 1):
                    if (u * (u < v) + v * (v < u), v * (u < v) + u * (v < u), 1) in tree.edges.keys() and not vis[v]:
                        q.append(v)
            self.assertTrue(tree.n == n and len(tree.edges)
                            == n - 1 and all(vis[1:]))


if __name__ == "__main__":
    unittest.main()
