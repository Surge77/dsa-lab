from Linear.arrays import MyArray as Array
from Non_Linear.graphs.directed.weighted.directed_weighted_graph_base import DirectedWeightedGraph

INF = float('inf')


def bfs(graph: DirectedWeightedGraph, start: int) -> Array:
    """
    Breadth-First Search (BFS) for directed weighted graph.
    Ignores weights, traverses level by level.

    Args:
        graph (DirectedWeightedGraph): The graph instance.
        start (int): Starting vertex.

    Returns:
        Array: BFS traversal order.

    Time Complexity: O(V + E)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()

    visited = Array()
    for _ in range(V):
        visited.append(False)

    result = Array()
    queue = Array()

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


def dfs(graph: DirectedWeightedGraph, start: int) -> Array:
    """
    Depth-First Search (DFS) for directed weighted graph.
    Ignores weights.

    Args:
        graph (DirectedWeightedGraph): The graph instance.
        start (int): Starting vertex.

    Returns:
        Array: DFS traversal order.

    Time Complexity: O(V + E)
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


def has_path(graph: DirectedWeightedGraph, u: int, v: int) -> bool:
    """
    Check if there is a path from u to v using DFS.

    Time Complexity: O(V + E)
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


def _transpose(graph: DirectedWeightedGraph) -> DirectedWeightedGraph:
    """
    Compute the transpose of a directed graph (reverse all edges).
    """
    V = graph.vertex_count()
    g_transpose = DirectedWeightedGraph(V)
    for u in range(V):
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            g_transpose.add_edge(v, u, w)
    return g_transpose


def connected_components(graph: DirectedWeightedGraph) -> Array:
    """
    Find strongly connected components (SCCs) using Kosaraju's algorithm.

    Returns:
        Array: Each element is an Array representing a strongly connected component.

    Time Complexity: O(V + E)
    """
    V = graph.vertex_count()
    visited = Array()
    for _ in range(V):
        visited.append(False)

    stack = Array()

    def fill_order(u: int):
        visited.set(u, True)
        for i in range(len(graph.adj[u])):
            v, _ = graph.adj[u].get(i)
            if not visited.get(v):
                fill_order(v)
        stack.append(u)

    for i in range(V):
        if not visited.get(i):
            fill_order(i)

    g_transpose = _transpose(graph)

    for i in range(V):
        visited.set(i, False)

    scc_list = Array()

    def dfs_collect(u: int, component: Array):
        visited.set(u, True)
        component.append(u)
        for i in range(len(g_transpose.adj[u])):
            v, _ = g_transpose.adj[u].get(i)
            if not visited.get(v):
                dfs_collect(v, component)

    while len(stack) > 0:
        u = stack.get(len(stack) - 1)
        stack.delete(len(stack) - 1)
        if not visited.get(u):
            component = Array()
            dfs_collect(u, component)
            scc_list.append(component)

    return scc_list


def dijkstra(graph: DirectedWeightedGraph, start: int) -> Array:
    """
    Dijkstra's algorithm for single-source shortest paths (non-negative weights).

    Args:
        graph (DirectedWeightedGraph): The graph instance.
        start (int): The source vertex.

    Returns:
        Array: Distance array with shortest distances from start to all vertices.

    Time Complexity: O(V²)
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()

    dist = Array()
    visited = Array()
    for _ in range(V):
        dist.append(INF)
        visited.append(False)
    dist.set(start, 0)

    def get_min_vertex():
        min_vertex = -1
        min_value = INF
        for i in range(V):
            if not visited.get(i) and dist.get(i) < min_value:
                min_value = dist.get(i)
                min_vertex = i
        return min_vertex

    for _ in range(V):
        u = get_min_vertex()
        if u == -1:
            break
        visited.set(u, True)
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            if not visited.get(v) and dist.get(u) + w < dist.get(v):
                dist.set(v, dist.get(u) + w)

    return dist


def bellman_ford(graph: DirectedWeightedGraph, start: int):
    """
    Bellman-Ford algorithm for single-source shortest paths.
    Handles negative weights and detects negative cycles.

    Args:
        graph (DirectedWeightedGraph): The graph instance.
        start (int): The source vertex.

    Returns:
        (Array, bool): Distance array and negative cycle flag.
    """
    graph._validate_vertex(start)
    V = graph.vertex_count()
    E = graph.edges()

    dist = Array()
    for _ in range(V):
        dist.append(INF)
    dist.set(start, 0)

    # Relax edges V-1 times
    for _ in range(V - 1):
        for u, v, w in E:
            if dist.get(u) != INF and dist.get(u) + w < dist.get(v):
                dist.set(v, dist.get(u) + w)

    # Check for negative cycles
    has_negative_cycle = False
    for u, v, w in E:
        if dist.get(u) != INF and dist.get(u) + w < dist.get(v):
            has_negative_cycle = True
            break

    return dist, has_negative_cycle


def floyd_warshall(graph: DirectedWeightedGraph) -> Array:
    """
    Floyd-Warshall algorithm for all-pairs shortest paths.

    Args:
        graph (DirectedWeightedGraph): The graph instance.

    Returns:
        Array: A 2D Array where dist[i][j] is the shortest distance from i to j.

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

    # Set initial distances from edges
    for u in range(V):
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            dist.get(u).set(v, w)

    # Core Floyd-Warshall updates
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist.get(i).get(k) + dist.get(k).get(j) < dist.get(i).get(j):
                    dist.get(i).set(j, dist.get(i).get(k) + dist.get(k).get(j))

    return dist
