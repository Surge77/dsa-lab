from Linear.arrays import MyArray as Array
from Non_Linear.graphs.directed.weighted.directed_weighted_graph_base import DirectedWeightedGraph

INF = float('inf')


def has_cycle(graph: DirectedWeightedGraph) -> bool:
    """
    Detect if a directed graph contains a cycle using DFS recursion stack.

    Args:
        graph (DirectedWeightedGraph): The graph instance.

    Returns:
        bool: True if a cycle exists, otherwise False.

    Time Complexity: O(V + E)
    """
    V = graph.vertex_count()
    visited = Array()
    rec_stack = Array()

    for _ in range(V):
        visited.append(False)
        rec_stack.append(False)

    def dfs(u: int) -> bool:
        visited.set(u, True)
        rec_stack.set(u, True)

        for i in range(len(graph.adj[u])):
            v, _ = graph.adj[u].get(i)
            if not visited.get(v):
                if dfs(v):
                    return True
            elif rec_stack.get(v):
                return True  # Found a cycle

        rec_stack.set(u, False)
        return False

    for i in range(V):
        if not visited.get(i):
            if dfs(i):
                return True

    return False


def topological_sort(graph: DirectedWeightedGraph) -> Array:
    """
    Perform topological sorting on a DAG.

    Args:
        graph (DirectedWeightedGraph): The graph instance.

    Returns:
        Array: Vertices in topologically sorted order.

    Time Complexity: O(V + E)
    """
    if has_cycle(graph):
        raise ValueError("Topological sort not possible: Graph contains a cycle.")

    V = graph.vertex_count()
    visited = Array()
    for _ in range(V):
        visited.append(False)

    result = Array()

    def dfs(u: int):
        visited.set(u, True)
        for i in range(len(graph.adj[u])):
            v, _ = graph.adj[u].get(i)
            if not visited.get(v):
                dfs(v)
        result.append(u)  # Append after exploring all neighbors

    for i in range(V):
        if not visited.get(i):
            dfs(i)

    # Reverse the result
    sorted_order = Array()
    for i in range(len(result) - 1, -1, -1):
        sorted_order.append(result.get(i))

    return sorted_order


def _bfs_residual(graph: DirectedWeightedGraph, s: int, t: int, parent: Array, residual: list) -> bool:
    """BFS to find augmenting path in residual graph."""
    V = graph.vertex_count()
    visited = [False] * V
    queue = [s]
    visited[s] = True
    parent.set(s, -1)

    while queue:
        u = queue.pop(0)
        for v, w in residual[u]:
            if not visited[v] and w > 0:
                parent.set(v, u)
                visited[v] = True
                if v == t:
                    return True
                queue.append(v)
    return False


def max_flow(graph: DirectedWeightedGraph, source: int, sink: int) -> float:
    """
    Compute max flow using Edmonds-Karp algorithm.

    Returns:
        float: Maximum flow value.
    """
    V = graph.vertex_count()

    # Build residual graph
    residual = [[] for _ in range(V)]
    for u in range(V):
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            residual[u].append([v, w])
            residual[v].append([u, 0])  # reverse edge with 0 capacity

    parent = Array()
    for _ in range(V):
        parent.append(-1)

    max_flow_value = 0

    while _bfs_residual(graph, source, sink, parent, residual):
        # Find bottleneck capacity
        path_flow = INF
        v = sink
        while v != source:
            u = parent.get(v)
            for edge in residual[u]:
                if edge[0] == v:
                    path_flow = min(path_flow, edge[1])
            v = u

        # Update residual graph
        v = sink
        while v != source:
            u = parent.get(v)
            for edge in residual[u]:
                if edge[0] == v:
                    edge[1] -= path_flow
            for edge in residual[v]:
                if edge[0] == u:
                    edge[1] += path_flow
            v = u

        max_flow_value += path_flow

    return max_flow_value


def transpose(graph: DirectedWeightedGraph) -> DirectedWeightedGraph:
    """
    Return the transpose of the graph (all edges reversed).
    """
    V = graph.vertex_count()
    g_t = DirectedWeightedGraph(V)
    for u in range(V):
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            g_t.add_edge(v, u, w)
    return g_t


def is_eulerian(graph: DirectedWeightedGraph) -> str:
    """
    Check if a directed graph has an Eulerian Path or Circuit.
    """
    V = graph.vertex_count()
    in_deg = [0] * V
    out_deg = [0] * V

    for u in range(V):
        for i in range(len(graph.adj[u])):
            v, _ = graph.adj[u].get(i)
            out_deg[u] += 1
            in_deg[v] += 1

    start_nodes = end_nodes = 0
    for i in range(V):
        if out_deg[i] - in_deg[i] > 1 or in_deg[i] - out_deg[i] > 1:
            return "Not Eulerian"
        if out_deg[i] - in_deg[i] == 1:
            start_nodes += 1
        elif in_deg[i] - out_deg[i] == 1:
            end_nodes += 1

    if start_nodes == 0 and end_nodes == 0:
        return "Eulerian Circuit"
    if start_nodes == 1 and end_nodes == 1:
        return "Eulerian Path"
    return "Not Eulerian"


def shortest_path_dag(graph: DirectedWeightedGraph, start: int) -> Array:
    """
    Compute shortest path in a DAG using topological sort.
    """
    graph._validate_vertex(start)
    order = topological_sort(graph)
    V = graph.vertex_count()
    dist = Array()
    for _ in range(V):
        dist.append(INF)
    dist.set(start, 0)

    for i in range(len(order)):
        u = order.get(i)
        if dist.get(u) != INF:
            for j in range(len(graph.adj[u])):
                v, w = graph.adj[u].get(j)
                if dist.get(u) + w < dist.get(v):
                    dist.set(v, dist.get(u) + w)
    return dist
