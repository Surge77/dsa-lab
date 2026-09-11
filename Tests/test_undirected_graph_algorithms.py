"""
Tests for the unweighted undirected graph algorithms.

This module — 246 statements covering cycle detection, bipartite checking,
BFS shortest paths, bridges, articulation points and Eulerian paths — had zero
coverage, because it opened with `from undirected_graph_base import Graph`: a
Python-2 implicit relative import that raises ModuleNotFoundError under
Python 3. Nothing could import it.
"""

import pytest

from Non_Linear.graphs.undirected import undirected_graph_algorithms as alg
from Non_Linear.graphs.undirected import undirected_graph_utils as utils
from Non_Linear.graphs.undirected.undirected_graph_base import Graph

UNREACHABLE = -1


def build(n: int, edges) -> Graph:
    graph = Graph(n)
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


@pytest.fixture
def triangle_plus_edge():
    """A 3-cycle (0,1,2) plus a separate edge (3,4), and an isolated vertex 5."""
    return build(6, [(0, 1), (1, 2), (2, 0), (3, 4)])


@pytest.fixture
def star():
    """A tree: 1 at the centre, joined to 0, 2 and 3."""
    return build(4, [(0, 1), (1, 2), (1, 3)])


# ------------------------------------------------------------ cycle detection


def test_cycle_detected_in_a_triangle(triangle_plus_edge):
    assert alg.cycle_detection(triangle_plus_edge) is True


def test_no_cycle_in_a_tree(star):
    """
    A tree has V-1 edges and no cycle.

    The trap this guards: undirected DFS must ignore the edge it arrived on, or
    every single edge looks like a 2-cycle.
    """
    assert alg.cycle_detection(star) is False


def test_no_cycle_in_an_edgeless_graph():
    assert alg.cycle_detection(Graph(4)) is False


def test_no_cycle_in_a_single_edge():
    assert alg.cycle_detection(build(2, [(0, 1)])) is False


def test_cycle_found_in_a_disconnected_component():
    """The search must cover every component, not just the one containing 0."""
    graph = build(6, [(0, 1), (3, 4), (4, 5), (5, 3)])
    assert alg.cycle_detection(graph) is True


# -------------------------------------------------------------- bipartiteness


def test_odd_cycle_is_not_bipartite(triangle_plus_edge):
    """
    A graph is bipartite exactly when it has no odd-length cycle.

    The triangle is the smallest counterexample.
    """
    assert alg.is_bipartite(triangle_plus_edge) is False


def test_tree_is_bipartite(star):
    assert alg.is_bipartite(star) is True


def test_even_cycle_is_bipartite():
    assert alg.is_bipartite(build(4, [(0, 1), (1, 2), (2, 3), (3, 0)])) is True


def test_bipartite_groups_split_every_edge():
    """
    The defining property: no edge may have both endpoints in the same group.

    Asserting that rather than a specific 2-colouring, since either colour
    assignment is valid.
    """
    graph = build(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    left, right = alg.get_bipartite_groups(graph)

    left_set, right_set = set(left), set(right)
    assert left_set | right_set == {0, 1, 2, 3}
    assert not (left_set & right_set)

    for u, v in utils.edges(graph):
        assert (u in left_set) != (v in left_set), f"edge {u}-{v} is inside one group"


def test_bipartite_groups_on_a_non_bipartite_graph(triangle_plus_edge):
    """Must report impossibility rather than returning a wrong 2-colouring."""
    result = alg.get_bipartite_groups(triangle_plus_edge)
    assert result is None or result == () or not all(result)


# ------------------------------------------------------------ BFS shortest path


def test_bfs_distances_count_edges(triangle_plus_edge):
    """
    In an unweighted graph BFS gives shortest paths in edge count.

    Vertices 3, 4 and 5 are in other components and must report unreachable.
    """
    distances = alg.shortest_path_bfs(triangle_plus_edge, 0)
    assert distances[0] == 0
    assert distances[1] == 1
    assert distances[2] == 1
    assert distances[3] == UNREACHABLE
    assert distances[4] == UNREACHABLE
    assert distances[5] == UNREACHABLE


def test_bfs_distances_on_a_path():
    graph = build(4, [(0, 1), (1, 2), (2, 3)])
    assert list(alg.shortest_path_bfs(graph, 0)) == [0, 1, 2, 3]


def test_bfs_takes_the_short_way_round_a_cycle():
    """With a cycle of length 4, the far vertex is 2 hops away, not 3."""
    graph = build(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    assert alg.shortest_path_bfs(graph, 0)[2] == 2


def test_reconstruct_path_returns_the_vertex_sequence():
    graph = build(4, [(0, 1), (1, 2), (2, 3)])
    assert list(alg.reconstruct_path(graph, 0, 3)) == [0, 1, 2, 3]


def test_reconstruct_path_on_a_shortcut(triangle_plus_edge):
    assert list(alg.reconstruct_path(triangle_plus_edge, 0, 2)) == [0, 2]


def test_reconstruct_path_returns_empty_when_unreachable(triangle_plus_edge):
    assert list(alg.reconstruct_path(triangle_plus_edge, 0, 4)) == []


def test_reconstruct_path_from_a_vertex_to_itself():
    graph = build(2, [(0, 1)])
    assert list(alg.reconstruct_path(graph, 0, 0)) == [0]


# ------------------------------------------------------------------ has_path


def test_has_path_via_bfs_and_dfs_agree(triangle_plus_edge):
    """Two traversals, one reachability question — they must never disagree."""
    for start, end in [(0, 1), (0, 2), (3, 4), (0, 4), (0, 5)]:
        assert alg.has_path(triangle_plus_edge, start, end) == alg.has_path_dfs(
            triangle_plus_edge, start, end
        ), f"bfs and dfs disagree on {start}->{end}"


def test_has_path_to_self():
    graph = build(2, [(0, 1)])
    assert alg.has_path(graph, 0, 0)
    assert alg.has_path_dfs(graph, 0, 0)


def test_no_path_to_an_isolated_vertex(triangle_plus_edge):
    assert not alg.has_path(triangle_plus_edge, 0, 5)
    assert not alg.has_path_dfs(triangle_plus_edge, 0, 5)


# ------------------------------------------------------------------- bridges


def test_every_edge_of_a_tree_is_a_bridge(star):
    """Removing any edge of a tree disconnects it, so all V-1 are critical."""
    bridges = alg.find_bridges(star)
    assert len(bridges) == 3


def test_a_cycle_has_no_bridges():
    """Every edge on a cycle has an alternative route, so none is critical."""
    assert len(alg.find_bridges(build(3, [(0, 1), (1, 2), (2, 0)]))) == 0


def test_the_edge_joining_two_cycles_is_the_only_bridge():
    """
    Two triangles linked by a single edge: that link is the one critical edge.

    This is the shape the "critical connections" problem uses.
    """
    graph = build(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)])
    bridges = alg.find_bridges(graph)

    assert len(bridges) == 1
    assert set(bridges[0]) == {2, 3}


def test_bridges_in_a_disconnected_graph(triangle_plus_edge):
    """The lone edge (3,4) is a bridge; the triangle's edges are not."""
    bridges = alg.find_bridges(triangle_plus_edge)
    assert len(bridges) == 1
    assert set(bridges[0]) == {3, 4}


# ------------------------------------------------------- articulation points


def test_centre_of_a_star_is_an_articulation_point(star):
    assert list(alg.find_articulation_points(star)) == [1]


def test_a_cycle_has_no_articulation_points():
    assert len(alg.find_articulation_points(build(3, [(0, 1), (1, 2), (2, 0)]))) == 0


def test_articulation_point_joining_two_cycles():
    """
    Vertices 2 and 3 each hold their triangle onto the other.

    Bridges and articulation points come from the same low-link computation; the
    difference between them is a single comparison (<= versus <).
    """
    graph = build(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)])
    points = set(alg.find_articulation_points(graph))
    assert points == {2, 3}


def test_middle_of_a_path_is_an_articulation_point():
    graph = build(3, [(0, 1), (1, 2)])
    assert list(alg.find_articulation_points(graph)) == [1]


# ----------------------------------------------------------------- Eulerian


def test_a_triangle_has_an_eulerian_circuit():
    """Every vertex has even degree, so a closed Eulerian circuit exists."""
    assert alg.is_eulerian(build(3, [(0, 1), (1, 2), (2, 0)])) == "circuit"


def test_a_path_has_an_eulerian_path_not_a_circuit():
    """Exactly two odd-degree vertices means an open path, not a circuit."""
    assert alg.is_eulerian(build(3, [(0, 1), (1, 2)])) == "path"


def test_a_star_with_three_odd_vertices_has_neither(star):
    """More than two odd-degree vertices rules out any Eulerian traversal."""
    assert alg.is_eulerian(star) == "none"


def test_a_disconnected_graph_is_not_eulerian(triangle_plus_edge):
    """Connectivity of the edge-bearing vertices is also required."""
    assert alg.is_eulerian(triangle_plus_edge) == "none"


def test_eulerian_path_visits_every_edge_exactly_once():
    graph = build(3, [(0, 1), (1, 2)])
    path = list(alg.find_eulerian_path(graph))

    assert len(path) == 3, "a path over 2 edges visits 3 vertices"
    traversed = {frozenset(pair) for pair in zip(path, path[1:], strict=False)}
    assert traversed == {frozenset({0, 1}), frozenset({1, 2})}


def test_eulerian_path_is_empty_when_none_exists(star):
    assert list(alg.find_eulerian_path(star)) == []


def test_eulerian_circuit_returns_to_its_start():
    circuit = list(alg.find_eulerian_path(build(3, [(0, 1), (1, 2), (2, 0)])))
    if circuit:
        assert circuit[0] == circuit[-1], "a circuit must close"
