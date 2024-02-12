"""
Generate graphs with various properties, including trees.
"""

import math
import random
from collections import defaultdict
from typing import Callable

from .utils import NOISE


class Tree:
    """Connected graph with no cycles."""

    def __init__(self, n: int, weighted: bool = False, weight_func: Callable[[], int] = lambda: 1):
        self.n = n
        self.weighted = weighted
        self.weight_func = weight_func

        self.edges = defaultdict(int)
        self.weights = {}
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
        for u, v in edges:
            coin = random.randint(0, 1)
            ret_str += f"\n{self.perm[u * coin + v * (1 - coin)]} {self.perm[u * (1 - coin) + v * coin]}"
            if self.weighted:
                ret_str += f" {self.weights[(u, v)]}"
        return ret_str

    def add_edge(self, u: int, v: int):
        # edges are always pairs (u, v) with u <= v
        if u > v:
            u, v = v, u
        self.edges[(u, v)] += 1
        self.weights[(u, v)] = self.weight_func()


class RandomTree(Tree):
    """Tree generated using a random Pruefer code."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.n == 1:
            return
        code = [random.randint(0, self.n - 1) for _ in range(self.n - 2)]
        deg = [1] * self.n
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
        self.add_edge(leaf + 1, self.n)


class CaterpillarTree(Tree):
    """Long trunk with small branches connected to it."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        trunk_len = random.randint(self.n // 2, self.n)
        for i in range(2, trunk_len + 1):
            self.add_edge(i, i - 1)
        for i in range(trunk_len + 1, self.n + 1):
            self.add_edge(i, random.randint(1, trunk_len))


class StarTree(Tree):
    """Small number of centers with all other nodes connected to them."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        centers = random.randint(1, min(self.n, NOISE))
        for i in range(2, centers + 1):
            self.add_edge(i, i - 1)
        for i in range(centers + 1, self.n + 1):
            self.add_edge(i, random.randint(1, centers))


class CombTree(Tree):
    """Trunk with ~sqrt(n) nodes, each one with an ~sqrt(n)-long branch."""

    def __init__(self, *args, **kwargs):

        def approx_sqrt(n: int) -> int:
            s = int(math.sqrt(n))
            if s > NOISE and s < n - NOISE:
                return s + random.randint(-NOISE, NOISE)
            return s

        super().__init__(*args, **kwargs)
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
    """Tree with depth ~log n."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(2, self.n + 1):
            self.add_edge(i, i // 2)


class Graph(Tree):
    """Set of nodes connected by edges."""

    def __init__(self, n: int, m: int, directed: bool = False, acyclic: bool = False, connected: bool = False, self_loops: bool = False, multi_edges: bool = False, **kwargs):
        """Note: parameter m (number of edges) will be "overridden" if both acyclic and connected are true and multiedges are false (but then you should be initializing a tree anyway)."""
        super().__init__(n, **kwargs)
        self.m = m
        self.directed = directed
        self.acyclic = acyclic
        self.connected = connected
        self.self_loops = self_loops
        self.multi_edges = multi_edges

    def __str__(self) -> str:
        """Return the graph as a string.
        First line: n, m
        Next m lines: edges
        """
        edges = list(self.edges.keys())
        random.shuffle(edges)

        ret_str = f"{self.n} {self.m}"
        for u, v in edges:
            ret_str += f"\n{self.perm[u]} {self.perm[v]}"
            if self.weighted:
                ret_str += f" {self.weights[(u, v)]}"
        return ret_str

    def add_edge(self, u: int, v: int):
        self.edges[(u, v)] += 1
        self.weights[(u, v)] = self.weight_func()


class RandomGraph(Graph):
    """Random graph."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.acyclic:
            if self.directed:
                for _ in range(self.m):
                    u = random.randint(1, self.n)
                    v = random.randint(u + 1, self.n)
                    self.add_edge(u, v)
            else:
                self.edges = RandomTree(
                    n=self.n, weighted=self.weighted, weight_func=self.weight_func).edges
                if not self.connected:
                    cut = min(self.m - (self.n - 1), random.randint(1, self.m))
                    for _ in range(cut):
                        to_remove = random.choice(list(self.edges.items()))[0]
                        self.edges[to_remove] -= 1
                        if self.edges[to_remove] == 0:
                            del self.edges[to_remove]
        else:
            if self.connected:
                self.edges = RandomTree(
                    n=self.n, weighted=self.weighted, weight_func=self.weight_func).edges
                for _ in range(self.m - (self.n - 1)):
                    u = random.randint(1, self.n)
                    v = random.randint(u + 0 if self.self_loops else 1, self.n)
                    # check for multiedges in both cases (undirected and directed)
