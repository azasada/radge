"""
Generate graphs with various properties, including trees.
"""

import math
import random
from typing import Callable, Optional

from .utils import NOISE


class Edge:
    """Edge between two vertices."""

    def __init__(self, u: int, v: int, w: Optional[int] = None):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self) -> str:
        """Return the edge as a string."""
        return f"{self.u} {self.v}" + (f" {self.w}" if self.w else "")


class Graph:
    """Vertices connected by edges."""

    def __init__(
        self,
        vertex_cnt: int,
        weight_func: Optional[Callable[[], int]] = None,
        directed: bool = False,
    ):
        """Initialize a graph."""
        self.vertex_cnt = vertex_cnt
        self.weight_func = weight_func
        self.directed = directed

        self.edge_cnt = 0
        self.edges = [[] for _ in range(vertex_cnt + 1)]
        perm = list(range(1, vertex_cnt + 1))
        random.shuffle(perm)
        self.perm = [0] + perm

    def permute_edge(self, edge: Edge) -> str:
        """Return the edge with vertices permuted."""
        split = str(edge).split()
        coin = random.randint(0, 1) if not self.directed else 1
        if not self.weight_func:
            u, v = map(int, split)
            return f"{coin * self.perm[u] + (1 - coin) * self.perm[v]} {(1 - coin) * self.perm[u] + coin * self.perm[v]}"
        else:
            u, v, w = map(int, split)
            return f"{coin * self.perm[u] + (1 - coin) * self.perm[v]} {(1 - coin) * self.perm[u] + coin * self.perm[v]} {w}"

    def __str__(self) -> str:
        """Return the graph as a string (listing of edges, each in a separate line)."""
        ret = []
        for v in range(1, self.vertex_cnt + 1):
            for edge in self.edges[v]:
                # to avoid duplicates in undirected graphs
                if self.directed or (not self.directed and edge.u <= edge.v):
                    ret.append(self.permute_edge(edge))
        random.shuffle(ret)

        return "\n".join(ret)

    def add_edge(self, u: int, v: int):
        """Add an edge u-v (and v-u if the graph is undirected)."""
        self.edge_cnt += 1
        w = self.weight_func() if self.weight_func else None
        self.edges[u].append(Edge(u, v, w))
        if not self.directed:
            self.edges[v].append(Edge(v, u, w))


def random_tree(
    vertex_cnt: int, weight_func: Optional[Callable[[], int]] = None
) -> Graph:
    """Return a random tree with vertex_cnt vertices."""
    tree = Graph(vertex_cnt, weight_func=weight_func)
    if vertex_cnt == 1:
        return tree
    code = [random.randint(0, vertex_cnt - 1) for _ in range(vertex_cnt - 2)]
    deg = [1] * (vertex_cnt + 1)
    for v in code:
        deg[v] += 1
    ptr = 0
    while deg[ptr] != 1:
        ptr += 1
    leaf = ptr

    for v in code:
        tree.add_edge(leaf + 1, v + 1)
        deg[v] -= 1
        if deg[v] == 1 and v < ptr:
            leaf = v
        else:
            ptr += 1
            while deg[ptr] != 1:
                ptr += 1
            leaf = ptr
    tree.add_edge(leaf + 1, vertex_cnt)

    return tree


def binary_tree(
    vertex_cnt: int, weight_func: Optional[Callable[[], int]] = None
) -> Graph:
    """Return a full binary tree with vertex_cnt vertices."""
    tree = Graph(vertex_cnt, weight_func=weight_func)
    for i in range(2, vertex_cnt + 1):
        tree.add_edge(i // 2, i)

    return tree


def caterpillar_tree(
    vertex_cnt: int, weight_func: Optional[Callable[[], int]] = None
) -> Graph:
    """Return a caterpillar tree with vertex_cnt vertices."""
    tree = Graph(vertex_cnt, weight_func=weight_func)
    if vertex_cnt == 1:
        return tree
    trunk_len = random.randint(vertex_cnt // 2, vertex_cnt)
    for i in range(2, trunk_len + 1):
        tree.add_edge(i, i - 1)
    for i in range(trunk_len + 1, vertex_cnt + 1):
        tree.add_edge(i, random.randint(1, trunk_len))

    return tree


def star_path_tree(
    vertex_cnt: int, star_cnt: int, weight_func: Optional[Callable[[], int]] = None
) -> Graph:
    """Return a star-path tree (high-degree vertices (stars) separated by paths) with vertex_cnt vertices, out of which star_cnt are stars."""
    if star_cnt > vertex_cnt:
        raise ValueError("star_cnt must not be more than vertex_cnt")
    tree = Graph(vertex_cnt, weight_func=weight_func)

    for i in range(2, star_cnt + 1):  # connect stars into a path
        tree.add_edge(i, i - 1)
    per_star = (vertex_cnt - star_cnt) // star_cnt
    for i in range(1, star_cnt + 1):
        for j in range(1, per_star + 1):  # add vertices to stars
            tree.add_edge(i, star_cnt + (i - 1) * per_star + j)
    # add remaining vertices to random stars
    for i in range(star_cnt + per_star * star_cnt + 1, vertex_cnt + 1):
        tree.add_edge(i, random.randint(1, star_cnt))

    return tree


def comb_tree(
    vertex_cnt: int, weight_func: Optional[Callable[[], int]] = None
) -> Graph:
    """Return a 'comb' tree (trunk with ~sqrt(n) vertices, of which each one has a ~sqrt(n)-long branch) with vertex_cnt vertices."""

    def approx_sqrt(n: int) -> int:
        s = int(math.sqrt(n))
        if s > NOISE and s < n - NOISE:
            return s + random.randint(-NOISE, NOISE)

        return s

    tree = Graph(vertex_cnt, weight_func=weight_func)
    trunk_len = approx_sqrt(vertex_cnt)
    for i in range(2, trunk_len + 1):
        tree.add_edge(i, i - 1)
    new_node, branch_node, branch_len = trunk_len + 1, 1, 0
    while new_node <= vertex_cnt:
        if branch_len == approx_sqrt(vertex_cnt) and branch_node < trunk_len:
            branch_node += 1
            branch_len = 0
        if branch_len == 0:
            tree.add_edge(branch_node, new_node)
        else:
            tree.add_edge(new_node - 1, new_node)
        new_node += 1
        branch_len += 1

    return tree


def random_graph(
    vertex_cnt: int,
    edge_cnt: int,
    weight_func: Optional[Callable[[], int]] = None,
    directed: bool = False,
    connected: bool = False,
    multi_edges: bool = False,
    self_loops: bool = False,
) -> Graph:
    """Return a random graph with vertex_cnt vertices and edge_cnt edges."""
    if edge_cnt > vertex_cnt * (vertex_cnt - 1) // 2:
        raise ValueError(
            "edge_cnt must not be more than vertex_cnt * (vertex_cnt - 1) / 2"
        )
    if edge_cnt < vertex_cnt - 1 and connected:
        raise ValueError(
            "edge_cnt must be at least vertex_cnt - 1 if the graph is to be connected."
        )
    graph = Graph(vertex_cnt, weight_func=weight_func, directed=directed)
    edges_set = set()
    cnt = 0
    if connected:
        tree = random_tree(vertex_cnt, weight_func=weight_func)
        graph.perm = tree.perm
        graph.edges = tree.edges
        graph.edge_cnt = tree.edge_cnt
        cnt = graph.edge_cnt
        for i in range(1, vertex_cnt + 1):
            for edge in graph.edges[i]:
                edges_set.add((edge.u, edge.v))
                if not directed:
                    edges_set.add((edge.v, edge.u))

    while cnt < edge_cnt:
        u, v = random.randint(1, vertex_cnt), random.randint(1, vertex_cnt)
        if (u == v and not self_loops) or ((u, v) in edges_set and not multi_edges):
            continue  # try again, because this edge is invalid
        graph.add_edge(u, v)

        cnt += 1
        if not multi_edges:  # if there are mutliedges then we don't care about the set
            edges_set.add((u, v))
            if not directed:
                edges_set.add((v, u))

    return graph


def dag(
    vertex_cnt: int,
    edge_cnt: int,
    weight_func: Optional[Callable[[], int]] = None,
    multi_edges: bool = False,
) -> Graph:
    """Return a random directed acyclic graph with vertex_cnt vertices and edge_cnt edges."""
    if edge_cnt > vertex_cnt * (vertex_cnt - 1) // 2:
        raise ValueError(
            "edge_cnt must not be more than vertex_cnt * (vertex_cnt - 1) / 2"
        )
    graph = Graph(vertex_cnt, weight_func=weight_func, directed=True)
    edges_set = set()
    cnt = 0

    while cnt < edge_cnt:
        # we assume that 1, 2, .., vertex_cnt is the topological order
        u = random.randint(1, vertex_cnt - 1)
        v = random.randint(u + 1, vertex_cnt)
        if (u, v) in edges_set and not multi_edges:
            continue
        graph.add_edge(u, v)

        cnt += 1
        if not multi_edges:  # if there are mutliedges then we don't care about the set
            edges_set.add((u, v))
    return graph
