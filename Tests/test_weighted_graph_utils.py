"""
Tests for the weighted-graph utility and matrix modules.

Both had zero coverage. `undirected_weighted_graph_utils.py` was unimportable
(Python-2 implicit relative import); the matrix variant imported fine but nothing
ever exercised it, so its adjacency-matrix representation was untested.
"""

import pytest

from Non_Linear.graphs.directed.weighted.directed_weighted_graph_matrix import (
    DirectedWeightedGraphMatrix,
)
from Non_Linear.graphs.undirected.weighted import undirected_weighted_graph_utils as utils
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base import (
    UndirectedWeightedGraph,
)
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_matrix import (
    UndirectedWeightedGraphMatrix,
)

EDGES = [(0, 1, 2.0), (1, 2, 3.0), (2, 3, 4.0)]


@pytest.fixture
def graph():
    g = UndirectedWeightedGraph(4)
    for u, v, w in EDGES:
        g.add_edge(u, v, w)
    return g


# ------------------------------------------------------------------- utils


def test_get_weight_returns_the_stored_weight(graph):
    assert utils.get_weight(graph, 0, 1) == 2.0
    assert utils.get_weight(graph, 1, 0) == 2.0, "undirected weights are symmetric"


def test_get_weight_on_a_missing_edge(graph):
    """Absence must be reported, not guessed at with a zero."""
    assert utils.get_weight(graph, 0, 3) is None


def test_update_weight_changes_both_directions(graph):
    assert utils.update_weight(graph, 0, 1, 9.0) is True
    assert utils.get_weight(graph, 0, 1) == 9.0
    assert utils.get_weight(graph, 1, 0) == 9.0, "an update must reach both lists"


def test_update_weight_reports_a_missing_edge(graph):
    assert utils.update_weight(graph, 0, 3, 1.0) is False


def test_is_connected_on_a_path(graph):
    assert utils.is_connected(graph) is True


def test_is_connected_on_two_islands():
    g = UndirectedWeightedGraph(4)
    g.add_edge(0, 1, 1.0)
    g.add_edge(2, 3, 1.0)
    assert utils.is_connected(g) is False


def test_is_connected_with_an_isolated_vertex():
    g = UndirectedWeightedGraph(3)
    g.add_edge(0, 1, 1.0)
    assert utils.is_connected(g) is False


def test_graph_density_of_a_path(graph):
    """
    3 edges out of the 6 possible undirected pairs on 4 vertices.

    Density is the single number that tells you whether to store an adjacency
    list or a matrix.
    """
    assert utils.graph_density(graph) == pytest.approx(0.5)


def test_graph_density_of_a_complete_graph():
    g = UndirectedWeightedGraph(4)
    for u in range(4):
        for v in range(u + 1, 4):
            g.add_edge(u, v, 1.0)
    assert utils.graph_density(g) == pytest.approx(1.0)


def test_graph_density_of_an_edgeless_graph():
    assert utils.graph_density(UndirectedWeightedGraph(4)) == pytest.approx(0.0)


def test_clear_removes_every_edge_but_keeps_the_vertices(graph):
    utils.clear(graph)
    assert graph.edge_count() == 0
    assert graph.vertex_count() == 4


def test_clone_produces_an_equal_but_independent_graph(graph):
    """
    A clone that shares adjacency lists is the classic shallow-copy bug: edits to
    the copy silently corrupt the original.
    """
    copy = utils.clone(graph)

    assert copy.edge_count() == graph.edge_count()
    for u, v, w in EDGES:
        assert copy.has_edge(u, v)
        assert utils.get_weight(copy, u, v) == w

    copy.add_edge(0, 3, 7.0)
    assert copy.has_edge(0, 3)
    assert not graph.has_edge(0, 3), "clone must not share structure with the original"


# ------------------------------------------------------------------ matrix


def test_undirected_matrix_stores_edges_symmetrically():
    m = UndirectedWeightedGraphMatrix(3)
    m.add_edge(0, 1, 5.0)

    assert m.has_edge(0, 1)
    assert m.has_edge(1, 0)


def test_directed_matrix_does_not_mirror_edges():
    m = DirectedWeightedGraphMatrix(3)
    m.add_edge(0, 1, 5.0)

    assert m.has_edge(0, 1)
    assert not m.has_edge(1, 0)


def test_matrix_remove_edge():
    m = UndirectedWeightedGraphMatrix(3)
    m.add_edge(0, 1, 5.0)
    m.remove_edge(0, 1)

    assert not m.has_edge(0, 1)
    assert not m.has_edge(1, 0)


def test_matrix_edge_count():
    m = UndirectedWeightedGraphMatrix(4)
    m.add_edge(0, 1, 1.0)
    m.add_edge(1, 2, 1.0)
    assert m.edge_count() == 2


def test_matrix_neighbours():
    m = UndirectedWeightedGraphMatrix(4)
    m.add_edge(1, 0, 1.0)
    m.add_edge(1, 2, 2.0)

    neighbours = {n[0] if isinstance(n, (tuple, list)) else n for n in m.neighbors(1)}
    assert neighbours == {0, 2}


def test_matrix_edges_lists_each_edge_once():
    """
    An undirected matrix must not report both (u,v) and (v,u).

    Iterating the full V x V matrix and emitting every non-zero cell is the usual
    way this goes wrong, and it doubles every edge count downstream.
    """
    m = UndirectedWeightedGraphMatrix(3)
    m.add_edge(0, 1, 1.0)
    m.add_edge(1, 2, 2.0)

    pairs = [frozenset((u, v)) for u, v, *_ in m.edges()]
    assert len(pairs) == len(set(pairs)) == 2


def test_matrix_vertex_count_is_fixed():
    """
    The defining trade-off: a matrix allocates V^2 up front regardless of E.

    Cheap O(1) edge lookup, O(V^2) memory even for an empty graph.
    """
    m = UndirectedWeightedGraphMatrix(5)
    assert m.vertex_count() == 5
    assert m.edge_count() == 0
