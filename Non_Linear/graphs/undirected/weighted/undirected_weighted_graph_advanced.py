from Linear.arrays import MyArray as Array
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base import (
    UndirectedWeightedGraph,
)

INF = float('inf')

def find_bridges(graph: UndirectedWeightedGraph):
    """
    Find all bridges in the undirected graph using Tarjan's algorithm.

    Args:
        graph (UndirectedWeightedGraph): The graph.

    Returns:
        Array: List of bridges as (u, v) pairs.

    Time Complexity: O(V + E)
    """
    V = graph.vertex_count()
    visited = Array()
    disc = Array()
    low = Array()
    parent = Array()
    bridges = Array()

    for _ in range(V):
        visited.append(False)
        disc.append(-1)
        low.append(-1)
        parent.append(-1)

    time = [0]  # Use list for mutability in nested function

    def dfs(u: int):
        visited.set(u, True)
        disc.set(u, time[0])
        low.set(u, time[0])
        time[0] += 1

        for i in range(len(graph.adj[u])):
            v, _ = graph.adj[u].get(i)
            if not visited.get(v):
                parent.set(v, u)
                dfs(v)
                low.set(u, min(low.get(u), low.get(v)))

                if low.get(v) > disc.get(u):
                    bridges.append((u, v))
            elif v != parent.get(u):
                low.set(u, min(low.get(u), disc.get(v)))

    for i in range(V):
        if not visited.get(i):
            dfs(i)

    return bridges


def find_articulation_points(graph: UndirectedWeightedGraph):
    """
    Find articulation points in the graph using Tarjan's algorithm.

    Args:
        graph (UndirectedWeightedGraph): The graph.

    Returns:
        Array: List of articulation points.

    Time Complexity: O(V + E)
    """
    V = graph.vertex_count()
    visited = Array()
    disc = Array()
    low = Array()
    parent = Array()
    ap = Array()  # Boolean array to track articulation points

    for _ in range(V):
        visited.append(False)
        disc.append(-1)
        low.append(-1)
        parent.append(-1)
        ap.append(False)

    time = [0]

    def dfs(u: int):
        children = 0
        visited.set(u, True)
        disc.set(u, time[0])
        low.set(u, time[0])
        time[0] += 1

        for i in range(len(graph.adj[u])):
            v, _ = graph.adj[u].get(i)
            if not visited.get(v):
                parent.set(v, u)
                children += 1
                dfs(v)

                low.set(u, min(low.get(u), low.get(v)))

                # (1) u is root and has 2+ children
                if parent.get(u) == -1 and children > 1:
                    ap.set(u, True)

                # (2) u is not root and low[v] >= disc[u]
                if parent.get(u) != -1 and low.get(v) >= disc.get(u):
                    ap.set(u, True)

            elif v != parent.get(u):
                low.set(u, min(low.get(u), disc.get(v)))

    for i in range(V):
        if not visited.get(i):
            dfs(i)

    # Collect articulation points
    result = Array()
    for i in range(V):
        if ap.get(i):
            result.append(i)

    return result


def is_connected(graph: UndirectedWeightedGraph) -> bool:
    """
    Check if all vertices with a non-zero degree belong to a single connected component.
    """
    V = graph.vertex_count()

    # Find a vertex with non-zero degree to start BFS
    start = -1
    for i in range(V):
        if graph.degree(i) > 0:
            start = i
            break

    if start == -1:
        return True  # No edges in the graph

    # BFS to check connectivity
    visited = Array()
    for _ in range(V):
        visited.append(False)

    queue = Array()
    visited.set(start, True)
    queue.append(start)

    while len(queue) > 0:
        node = queue.get(0)
        queue.delete(0)
        for j in range(len(graph.adj[node])):
            neighbor, _ = graph.adj[node].get(j)
            if not visited.get(neighbor):
                visited.set(neighbor, True)
                queue.append(neighbor)

    # Check if all non-zero degree vertices are visited
    for i in range(V):
        if graph.degree(i) > 0 and not visited.get(i):
            return False
    return True


def is_eulerian(graph: UndirectedWeightedGraph) -> str:
    """
    Determine if the graph has an Eulerian Path, Circuit, or None.

    Returns:
        str: "Eulerian Circuit", "Eulerian Path", or "Not Eulerian".
    """
    if not is_connected(graph):
        return "Not Eulerian"

    odd_degree_count = 0
    for i in range(graph.vertex_count()):
        if graph.degree(i) % 2 != 0:
            odd_degree_count += 1

    if odd_degree_count == 0:
        return "Eulerian Circuit"
    if odd_degree_count == 2:
        return "Eulerian Path"
    return "Not Eulerian"



def minimum_cut(graph: UndirectedWeightedGraph) -> float:
    """
    Compute the minimum cut of an undirected weighted graph using
    Stoer-Wagner algorithm.

    Args:
        graph (UndirectedWeightedGraph): The graph.

    Returns:
        float: Minimum cut value.

    Time Complexity: O(V³)
    """
    V = graph.vertex_count()
    if V == 0:
        return 0

    # Create adjacency matrix for fast access
    adj_matrix = Array()
    for _ in range(V):
        row = Array()
        for _ in range(V):
            row.append(0)
        adj_matrix.append(row)

    for u in range(V):
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            adj_matrix.get(u).set(v, adj_matrix.get(u).get(v) + w)

    vertices = Array()
    for i in range(V):
        vertices.append(i)

    min_cut_value = INF

    while len(vertices) > 1:
        used = [False] * len(vertices)
        weights = [0] * len(vertices)
        prev = 0

        for i in range(len(vertices)):
            # Select the most tightly connected unused vertex
            max_w = -1
            sel = -1
            for j in range(len(vertices)):
                if not used[j] and weights[j] > max_w:
                    max_w = weights[j]
                    sel = j

            if i == len(vertices) - 1:
                # Last vertex added: update minimum cut
                min_cut_value = min(min_cut_value, max_w)

                # Merge last two vertices
                for k in range(len(vertices)):
                    adj_matrix.get(prev).set(
                        k, adj_matrix.get(prev).get(k) + adj_matrix.get(sel).get(k)
                    )
                    adj_matrix.get(k).set(
                        prev, adj_matrix.get(k).get(prev) + adj_matrix.get(k).get(sel)
                    )
                vertices.delete(sel)
                break

            used[sel] = True
            if i == len(vertices) - 1:
                break
            prev = sel
            for k in range(len(vertices)):
                if not used[k]:
                    weights[k] += adj_matrix.get(sel).get(k)

    return min_cut_value

