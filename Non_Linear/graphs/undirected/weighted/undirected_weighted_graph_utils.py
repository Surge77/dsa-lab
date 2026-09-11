from Linear.arrays import MyArray as Array
from Linear.singly_linked_list import SinglyLinkedList as LinkedList
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base import (
    UndirectedWeightedGraph,
)


def get_weight(graph: UndirectedWeightedGraph, u: int, v: int):
    """
    Get the weight of an edge (u, v) in an undirected weighted graph.

    Args:
        graph (UndirectedWeightedGraph): The graph instance.
        u (int): First vertex.
        v (int): Second vertex.

    Returns:
        float or None: The weight of the edge if it exists, otherwise None.

    Time Complexity: O(deg(u))
    """
    graph._validate_vertex(u)
    graph._validate_vertex(v)

    for i in range(len(graph.adj[u])):
        neighbor, weight = graph.adj[u].get(i)
        if neighbor == v:
            return weight
    return None


def update_weight(graph: UndirectedWeightedGraph, u: int, v: int, new_weight: float) -> bool:
    """
    Update the weight of an existing edge (u, v) in the graph.

    Args:
        graph (UndirectedWeightedGraph): The graph instance.
        u (int): First vertex.
        v (int): Second vertex.
        new_weight (float): New weight to assign.

    Returns:
        bool: True if the edge was updated, False if edge doesn't exist.

    Time Complexity: O(deg(u) + deg(v))
    """
    graph._validate_vertex(u)
    graph._validate_vertex(v)

    updated = False

    # Update weight in u's adjacency list
    for i in range(len(graph.adj[u])):
        neighbor, weight = graph.adj[u].get(i)
        if neighbor == v:
            graph.adj[u].set(i, (v, new_weight))
            updated = True
            break

    # Update weight in v's adjacency list
    for i in range(len(graph.adj[v])):
        neighbor, weight = graph.adj[v].get(i)
        if neighbor == u:
            graph.adj[v].set(i, (u, new_weight))
            break

    return updated


def clear(graph: UndirectedWeightedGraph):
    """
    Remove all edges from the graph but retain vertices.
    Replaces each adjacency list with a new empty SinglyLinkedList.

    Time Complexity: O(V)
    """
    for i in range(graph.vertex_count()):
        graph.adj.set(i, LinkedList())  # Replace each list with an empty one


def graph_density(graph: UndirectedWeightedGraph) -> float:
    """
    Calculate and return the density of the undirected graph.

    Density = 2E / (V * (V - 1))
    where V = number of vertices, E = number of edges.

    Time Complexity: O(1)
    """
    V = graph.vertex_count()
    E = graph.edge_count()
    if V <= 1:
        return 0.0
    return (2 * E) / (V * (V - 1))


def is_connected(graph: UndirectedWeightedGraph) -> bool:
    """
    Check if the undirected graph is connected using BFS.

    Time Complexity: O(V + E)
    """
    V = graph.vertex_count()
    if V == 0:
        return True

    # Create visited array
    visited = Array()
    for _ in range(V):
        visited.append(False)

    # BFS queue using custom Array
    queue = Array()
    queue.append(0)
    visited.set(0, True)

    while len(queue) > 0:
        node = queue.get(0)
        queue.delete(0)
        for i in range(len(graph.adj[node])):
            neighbor, _ = graph.adj[node].get(i)
            if not visited.get(neighbor):
                visited.set(neighbor, True)
                queue.append(neighbor)

    # Check if all vertices were visited
    for i in range(V):
        if not visited.get(i):
            return False
    return True


def clone(graph: UndirectedWeightedGraph) -> UndirectedWeightedGraph:
    """
    Create and return a deep copy of the undirected weighted graph.

    Time Complexity: O(V + E)
    """
    new_graph = UndirectedWeightedGraph(graph.vertex_count())
    for u in range(graph.vertex_count()):
        for i in range(len(graph.adj[u])):
            v, w = graph.adj[u].get(i)
            if u < v:  # Avoid duplicate edges
                new_graph.add_edge(u, v, w)
    return new_graph

