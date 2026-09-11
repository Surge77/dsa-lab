from Linear.arrays import MyArray as Array
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base import (
    UndirectedWeightedGraph,
)

INF = float('inf')

# This is an inner helper class
class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure with path compression and union by rank.
    Used for cycle detection in Kruskal's MST algorithm.
    """
    def __init__(self, size: int):
        self.parent = Array()
        self.rank = Array()
        for i in range(size):
            self.parent.append(i)
            self.rank.append(0)

    def find(self, x: int) -> int:
        """
        Find the root of element x with path compression.
        """
        if self.parent.get(x) != x:
            self.parent.set(x, self.find(self.parent.get(x)))
        return self.parent.get(x)

    def union(self, x: int, y: int) -> bool:
        """
        Union sets containing x and y.
        Returns True if union was performed (different sets), False if already connected.
        """
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX == rootY:
            return False

        # Union by rank
        if self.rank.get(rootX) < self.rank.get(rootY):
            self.parent.set(rootX, rootY)
        elif self.rank.get(rootX) > self.rank.get(rootY):
            self.parent.set(rootY, rootX)
        else:
            self.parent.set(rootY, rootX)
            self.rank.set(rootX, self.rank.get(rootX) + 1)
        return True


def kruskal_mst(graph: UndirectedWeightedGraph):
    """
    Kruskal's algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (UndirectedWeightedGraph): The graph instance.

    Returns:
        (Array, float): Tuple with MST edges [(u, v, w)] and total weight.

    Time Complexity: O(E log E)
    Space Complexity: O(V)
    """
    V = graph.vertex_count()
    edges = graph.edges()  # List of (u, v, w)

    # Sort edges by weight (using Python's built-in sort for simplicity)
    edges.sort(key=lambda x: x[2])

    uf = UnionFind(V)
    mst_edges = Array()
    total_weight = 0.0

    for u, v, w in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
        if len(mst_edges) == V - 1:
            break

    return mst_edges, total_weight


def prim_mst(graph: UndirectedWeightedGraph, start: int = 0):
    """
    Prim's algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (UndirectedWeightedGraph): The graph instance.
        start (int): Starting vertex for MST.

    Returns:
        (Array, float): Tuple with MST edges [(u, v, w)] and total weight.

    Time Complexity: O(V²)
    Space Complexity: O(V)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()

    key = Array()
    parent = Array()
    visited = Array()

    for _ in range(V):
        key.append(INF)
        parent.append(-1)
        visited.append(False)

    key.set(start, 0)
    total_weight = 0.0
    mst_edges = Array()

    def get_min_vertex():
        min_vertex = -1
        min_value = INF
        for i in range(V):
            if not visited.get(i) and key.get(i) < min_value:
                min_value = key.get(i)
                min_vertex = i
        return min_vertex

    for _ in range(V):
        u = get_min_vertex()
        if u == -1:
            break
        visited.set(u, True)
        total_weight += key.get(u)

        if parent.get(u) != -1:  # Add edge to MST
            mst_edges.append((parent.get(u), u, key.get(u)))

        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            if not visited.get(v) and w < key.get(v):
                key.set(v, w)
                parent.set(v, u)

    return mst_edges, total_weight
