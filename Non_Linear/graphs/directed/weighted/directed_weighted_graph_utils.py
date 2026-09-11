from Linear.singly_linked_list import SinglyLinkedList as LinkedList
from Non_Linear.graphs.directed.weighted.directed_weighted_graph_base import DirectedWeightedGraph


def get_weight(graph: DirectedWeightedGraph, u: int, v: int):
    """
    Get the weight of the edge u -> v.

    Returns:
        float or None: Weight if edge exists, otherwise None.

    Time Complexity: O(deg(u))
    """
    graph._validate_vertex(u)
    graph._validate_vertex(v)
    for i in range(len(graph.adj[u])):
        neighbor, weight = graph.adj[u].get(i)
        if neighbor == v:
            return weight
    return None


def update_weight(graph: DirectedWeightedGraph, u: int, v: int, new_weight: float) -> bool:
    """
    Update the weight of the edge u -> v.

    Returns:
        bool: True if updated, False if edge doesn't exist.

    Time Complexity: O(deg(u))
    """
    graph._validate_vertex(u)
    graph._validate_vertex(v)
    for i in range(len(graph.adj[u])):
        neighbor, weight = graph.adj[u].get(i)
        if neighbor == v:
            graph.adj[u].set(i, (v, new_weight))
            return True
    return False


def clear(graph: DirectedWeightedGraph):
    """
    Remove all edges but keep vertices.

    Time Complexity: O(V)
    """
    for i in range(graph.vertex_count()):
        graph.adj.set(i, LinkedList())


def out_degree(graph: DirectedWeightedGraph, u: int) -> int:
    """
    Return the out-degree (number of outgoing edges) of vertex u.

    Time Complexity: O(1)
    """
    graph._validate_vertex(u)
    return len(graph.adj[u])


def in_degree(graph: DirectedWeightedGraph, u: int) -> int:
    """
    Return the in-degree (number of incoming edges) of vertex u.

    Time Complexity: O(V + E)
    """
    graph._validate_vertex(u)
    count = 0
    for i in range(graph.vertex_count()):
        for j in range(len(graph.adj[i])):
            neighbor, _ = graph.adj[i].get(j)
            if neighbor == u:
                count += 1
    return count


def graph_density(graph: DirectedWeightedGraph) -> float:
    """
    Compute the density of a directed graph.

    Density = E / (V * (V - 1))

    Time Complexity: O(1)
    """
    V = graph.vertex_count()
    E = graph.edge_count()
    if V <= 1:
        return 0.0
    return E / (V * (V - 1))
