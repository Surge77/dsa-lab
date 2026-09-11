from .undirected_graph_base import Graph


def is_connected(graph: Graph) -> bool:
    """
    Checks if the undirected graph is connected (there is a path between any two vertices).

    Uses BFS from the first vertex that has at least one edge.
    - Marks all reachable vertices.
    - Then checks if any vertex with at least one edge was not visited.

    Returns:
        True if the graph is connected, False otherwise.

    Time Complexity: O(V + E)
    """
    n = graph.vertex_count()
    if n == 0:
        return True  # By convention, empty graph is connected

    # Find the first vertex with an edge
    start = None
    for u in range(n):
        if len(graph.adj[u]) > 0:
            start = u
            break

    if start is None:
        # No edges at all, isolated vertices only
        # Convention: a graph with only isolated vertices is connected only if n <= 1
        return n <= 1

    # Standard BFS traversal
    visited = [False] * n
    queue = []
    queue.append(start)
    visited[start] = True

    while queue:
        u = queue.pop(0)
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if not visited[v]:
                visited[v] = True
                queue.append(v)

    # Check if all vertices are visited
    # A graph is only connected if there are no unreachable vertices
    for u in range(n):
        if not visited[u]:
            return False

    return True


def degree(graph: Graph, u: int) -> int:
    """
    Returns the degree (number of neighbors) of vertex u in the graph.

    Args:
        graph (Graph): The undirected graph object.
        u (int): The vertex whose degree is needed.

    Returns:
        int: Degree of vertex u.

    Raises:
        ValueError: If u is out of valid vertex range.

    Time Complexity: O(1)
    """
    graph._validate_vertex(u)
    return len(graph.adj[u])


def edges(graph: Graph):
    """
    Returns all unique edges in the undirected graph as a list of (u, v) tuples, where u < v.
    Self-loops are included as (u, u).

    Args:
        graph (Graph): The undirected graph object.

    Returns:
        List[Tuple[int, int]]: All unique edges.

    Time Complexity: O(V + E)
    """
    result = []
    n = graph.vertex_count()
    for u in range(n):
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            # Ensure each edge is listed only once (u < v or u == v for self-loop)
            if u < v or u == v:
                result.append((u, v))
    return result

def clear(graph: Graph) -> None:
    """
    Removes all edges from the graph, keeping all vertices intact.

    Args:
        graph (Graph): The undirected graph object.

    Time Complexity: O(V)
    """
    n = graph.vertex_count()
    for u in range(n):
        graph.adj[u] = graph.adj[u].__class__()  # Creates a new empty LinkedList for each vertex


def clone(graph: Graph) -> Graph:
    """
    Returns a deep copy of the graph.
    All vertices and their adjacency lists are duplicated,
    so modifying the clone does not affect the original.

    Args:
        graph (Graph): The graph to clone.

    Returns:
        Graph: A deep copy of the input graph.

    Time Complexity: O(V + E)
    """
    n = graph.vertex_count()
    new_graph = graph.__class__(n)
    for u in range(n):
        # For each neighbor in original, add it to the new adjacency list
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            # To prevent duplicate undirected edges, only add (u, v) if u <= v
            if u <= v:
                new_graph.add_edge(u, v)
    return new_graph


