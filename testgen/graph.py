"""
Generate graphs with various properties, including trees.
"""

import random
from typing import Callable
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

# TODO: remove some leaves, sometimes
class BinaryTree(Tree):
    def __init__(self, n: int, weighted: bool = False, weight_func: Callable[[], int] = lambda: 1):
        """Initialize a binary tree."""
        super().__init__(n, weighted, weight_func)
        for i in range(2, self.n + 1):
            self.add_edge(i, i // 2)


class TestTreeGeneration(unittest.TestCase):
    def test_binary_tree(self):
        n = random.randint(7, 7)
        tree = BinaryTree(n)
        print(tree)
        deg = [0 for _ in range(tree.n + 1)]
        for (u, v, _) in tree.edges.keys():
            deg[u] += 1
            deg[v] += 1
        self.assertTrue(all(d <= 3 for d in deg))


if __name__ == "__main__":
    unittest.main()
