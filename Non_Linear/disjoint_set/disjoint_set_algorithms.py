from Linear.arrays import MyArray as Array
from Non_Linear.disjoint_set.disjoint_set_base import DisjointSet


def detect_cycle_undirected(num_vertices: int, edges: list) -> bool:
    """
    Detect if an undirected graph contains a cycle using Union-Find.

    Args:
        num_vertices (int): Number of vertices.
        edges (list): List of edges (u, v).

    Returns:
        bool: True if a cycle exists, False otherwise.

    Time Complexity: O(E * α(V)) where α is the inverse Ackermann function.
    """
    ds = DisjointSet(num_vertices)

    for u, v in edges:
        root_u = ds.find(u)
        root_v = ds.find(v)
        if root_u == root_v:
            return True  # Cycle found
        ds.union(root_u, root_v)

    return False


def kruskal_mst(num_vertices: int, edges: list):
    """
    Kruskal's algorithm to find the Minimum Spanning Tree (MST).

    Args:
        num_vertices (int): Number of vertices.
        edges (list): List of edges (u, v, weight).

    Returns:
        (Array, float): MST edges and total weight.

    Time Complexity: O(E log E) due to sorting.
    """
    ds = DisjointSet(num_vertices)
    # Sort a copy: `edges.sort()` would reorder the caller's list as a side
    # effect, which is surprising and makes the function unsafe to call twice on
    # data someone else still holds.
    edges_by_weight = sorted(edges, key=lambda edge: edge[2])

    mst_edges = Array()
    total_weight = 0.0

    for u, v, w in edges_by_weight:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst_edges.append((u, v, w))
            total_weight += w
        if len(mst_edges) == num_vertices - 1:
            break

    return mst_edges, total_weight
