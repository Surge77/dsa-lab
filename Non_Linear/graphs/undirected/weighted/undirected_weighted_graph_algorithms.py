from Linear.arrays import MyArray as Array
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base import (
    UndirectedWeightedGraph,
)

INF = float('inf')

def bfs(graph: UndirectedWeightedGraph, start: int) -> Array:
    """
    Perform Breadth-First Search (BFS) on an undirected weighted graph.

    Args:
        graph (UndirectedWeightedGraph): The graph instance.
        start (int): Starting vertex.

    Returns:
        Array: Vertices in BFS traversal order.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()

    visited = Array()
    for _ in range(V):
        visited.append(False)

    result = Array()  # Stores BFS order
    queue = Array()   # BFS queue

    visited.set(start, True)
    queue.append(start)

    while len(queue) > 0:
        node = queue.get(0)
        queue.delete(0)
        result.append(node)

        for i in range(len(graph.adj[node])):
            neighbor, _ = graph.adj[node].get(i)
            if not visited.get(neighbor):
                visited.set(neighbor, True)
                queue.append(neighbor)

    return result


def dfs(graph: UndirectedWeightedGraph, start: int) -> Array:
    """
    Perform Depth-First Search (DFS) on an undirected weighted graph.

    Args:
        graph (UndirectedWeightedGraph): The graph instance.
        start (int): Starting vertex.

    Returns:
        Array: Vertices in DFS traversal order.

    Time Complexity: O(V + E)
    Space Complexity: O(V) (recursion stack + visited array)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()

    visited = Array()
    for _ in range(V):
        visited.append(False)

    result = Array()

    def dfs_recursive(node: int):
        visited.set(node, True)
        result.append(node)
        for i in range(len(graph.adj[node])):
            neighbor, _ = graph.adj[node].get(i)
            if not visited.get(neighbor):
                dfs_recursive(neighbor)

    dfs_recursive(start)
    return result


def has_path(graph: UndirectedWeightedGraph, u: int, v: int) -> bool:
    """
    Check if there exists a path between vertices u and v.

    Args:
        graph (UndirectedWeightedGraph): The graph instance.
        u (int): Start vertex.
        v (int): Destination vertex.

    Returns:
        bool: True if a path exists, False otherwise.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    graph._validate_vertex(u)
    graph._validate_vertex(v)

    if u == v:
        return True

    V = graph.vertex_count()
    visited = Array()
    for _ in range(V):
        visited.append(False)

    def dfs_check(node: int):
        visited.set(node, True)
        if node == v:
            return True
        for i in range(len(graph.adj[node])):
            neighbor, _ = graph.adj[node].get(i)
            if not visited.get(neighbor):
                if dfs_check(neighbor):
                    return True
        return False

    return dfs_check(u)


def connected_components(graph: UndirectedWeightedGraph) -> Array:
    """
    Find all connected components in the undirected graph.

    Returns:
        Array: An Array where each element is another Array containing vertices of a component.

    Time Complexity: O(V + E)
    """
    V = graph.vertex_count()
    visited = Array()
    for _ in range(V):
        visited.append(False)

    components = Array()

    def dfs_collect(node: int, comp: Array):
        visited.set(node, True)
        comp.append(node)
        for i in range(len(graph.adj[node])):
            neighbor, _ = graph.adj[node].get(i)
            if not visited.get(neighbor):
                dfs_collect(neighbor, comp)

    for i in range(V):
        if not visited.get(i):
            comp = Array()
            dfs_collect(i, comp)
            components.append(comp)

    return components


def dijkstra(graph: UndirectedWeightedGraph, start: int) -> Array:
    """
    Dijkstra's algorithm for single-source shortest paths
    in an undirected weighted graph with non-negative weights.

    Args:
        graph (UndirectedWeightedGraph): The graph.
        start (int): The source vertex.

    Returns:
        Array: Distance array where dist[i] is the shortest distance from start to i.

    Time Complexity: O(V² + E)
    Space Complexity: O(V)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()

    # Distance array initialized to infinity
    dist = Array()
    for _ in range(V):
        dist.append(INF)
    dist.set(start, 0)

    visited = Array()
    for _ in range(V):
        visited.append(False)

    def get_min_vertex():
        """Return the unvisited vertex with minimum distance."""
        min_vertex = -1
        min_value = INF
        for i in range(V):
            if not visited.get(i) and dist.get(i) < min_value:
                min_value = dist.get(i)
                min_vertex = i
        return min_vertex

    # Main Dijkstra loop
    for _ in range(V):
        u = get_min_vertex()
        if u == -1:
            break  # All reachable vertices processed
        visited.set(u, True)

        # Relax neighbors
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            if not visited.get(v) and dist.get(u) + w < dist.get(v):
                dist.set(v, dist.get(u) + w)

    return dist

def bellman_ford(graph: UndirectedWeightedGraph, start: int):
    """
    Bellman-Ford algorithm for single-source shortest paths.
    Works with negative edge weights and detects negative cycles.

    Args:
        graph (UndirectedWeightedGraph): The graph.
        start (int): The source vertex.

    Returns:
        (Array, bool): Tuple where:
            - Array: Distance array where dist[i] is the shortest distance from start to i.
            - bool: True if a negative weight cycle is detected, False otherwise.

    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()
    E_list = graph.edges()  # All edges (u, v, w)

    # Distance array
    dist = Array()
    for _ in range(V):
        dist.append(INF)
    dist.set(start, 0)

    # Relax all edges V-1 times
    for _ in range(V - 1):
        for edge in E_list:
            u, v, w = edge
            if dist.get(u) != INF and dist.get(u) + w < dist.get(v):
                dist.set(v, dist.get(u) + w)
            if dist.get(v) != INF and dist.get(v) + w < dist.get(u):
                dist.set(u, dist.get(v) + w)  # Because undirected

    # Check for negative cycles
    has_negative_cycle = False
    for edge in E_list:
        u, v, w = edge
        if dist.get(u) != INF and dist.get(u) + w < dist.get(v):
            has_negative_cycle = True
            break
        if dist.get(v) != INF and dist.get(v) + w < dist.get(u):
            has_negative_cycle = True
            break

    return dist, has_negative_cycle


def floyd_warshall(graph: UndirectedWeightedGraph):
    """
    Floyd-Warshall algorithm for all-pairs shortest paths.

    Args:
        graph (UndirectedWeightedGraph): The graph.

    Returns:
        Array: A 2D Array where dist[i][j] is the shortest distance between i and j.

    Time Complexity: O(V³)
    Space Complexity: O(V²)
    """
    V = graph.vertex_count()

    # Initialize distance matrix
    dist = Array()
    for i in range(V):
        row = Array()
        for j in range(V):
            if i == j:
                row.append(0)
            else:
                row.append(INF)
        dist.append(row)

    # Set initial distances based on edges
    for u in range(V):
        for k in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(k)
            dist.get(u).set(v, w)
            dist.get(v).set(u, w)  # Undirected graph

    # Main Floyd-Warshall loop
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist.get(i).get(k) + dist.get(k).get(j) < dist.get(i).get(j):
                    dist.get(i).set(j, dist.get(i).get(k) + dist.get(k).get(j))

    return dist
