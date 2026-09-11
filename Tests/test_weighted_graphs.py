"""
Tests for the weighted graph algorithms, which had none before.

Eight of these modules were unreachable: they opened with Python-2 implicit
relative imports such as `from undirected_weighted_graph_base import ...`, which
raise ModuleNotFoundError under Python 3. Dijkstra, Bellman-Ford,
Floyd-Warshall, Kruskal, Prim, max-flow, topological sort, bridges and min-cut
were all dead code that nothing could import and nothing tested.
"""

import pytest

from Non_Linear.graphs.directed.weighted import (
    directed_weighted_graph_advanced as d_advanced,
)
from Non_Linear.graphs.directed.weighted import (
    directed_weighted_graph_algorithms as d_algorithms,
)
from Non_Linear.graphs.directed.weighted import (
    directed_weighted_graph_utils as d_utils,
)
from Non_Linear.graphs.directed.weighted.directed_weighted_graph_base import (
    DirectedWeightedGraph,
)
from Non_Linear.graphs.undirected.weighted import (
    undirected_weighted_graph_advanced as u_advanced,
)
from Non_Linear.graphs.undirected.weighted import (
    undirected_weighted_graph_algorithms as u_algorithms,
)
from Non_Linear.graphs.undirected.weighted import undirected_weighted_graph_mst as mst
from Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base import (
    UndirectedWeightedGraph,
)

# A small weighted graph used throughout. Shortest paths from 0 are
# [0, 3, 1, 8, 11] — note 0->2->1 (cost 3) beats the direct 0->1 edge (cost 4),
# which is what makes it a real test of Dijkstra rather than of BFS.
EDGES = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5), (3, 4, 3)]
EXPECTED_DISTANCES = [0, 3, 1, 8, 11]
MST_WEIGHT = 11


@pytest.fixture
def undirected():
    graph = UndirectedWeightedGraph(5)
    for u, v, w in EDGES:
        graph.add_edge(u, v, w)
    return graph


@pytest.fixture
def directed():
    graph = DirectedWeightedGraph(5)
    for u, v, w in EDGES:
        graph.add_edge(u, v, w)
    return graph


# ------------------------------------------------------------------ base class


def test_undirected_edges_are_symmetric(undirected):
    """The defining property: an edge added once is visible from both ends."""
    assert undirected.has_edge(0, 1)
    assert undirected.has_edge(1, 0)


def test_directed_edges_are_not_symmetric(directed):
    """And the directed graph must NOT add the reverse edge."""
    assert directed.has_edge(0, 1)
    assert not directed.has_edge(1, 0)


def test_edge_counts(undirected, directed):
    assert undirected.edge_count() == len(EDGES)
    assert directed.edge_count() == len(EDGES)


def test_remove_edge(undirected):
    undirected.remove_edge(0, 1)
    assert not undirected.has_edge(0, 1)
    assert not undirected.has_edge(1, 0), "removal must clear both directions"


def test_invalid_vertices_are_rejected(undirected):
    """Out-of-range vertices must be rejected, not silently stored."""
    with pytest.raises((ValueError, IndexError)):
        undirected.add_edge(0, 99, 1.0)


# -------------------------------------------------------------------- traversal


def test_bfs_reaches_every_connected_vertex(undirected):
    assert sorted(u_algorithms.bfs(undirected, 0)) == [0, 1, 2, 3, 4]


def test_dfs_reaches_every_connected_vertex(undirected):
    assert sorted(u_algorithms.dfs(undirected, 0)) == [0, 1, 2, 3, 4]


def test_bfs_visits_the_start_vertex_first(undirected):
    assert u_algorithms.bfs(undirected, 0)[0] == 0


def test_connected_components_on_a_connected_graph(undirected):
    components = u_algorithms.connected_components(undirected)
    assert len(components) == 1


def test_connected_components_separates_islands():
    graph = UndirectedWeightedGraph(4)
    graph.add_edge(0, 1, 1)
    graph.add_edge(2, 3, 1)

    components = u_algorithms.connected_components(graph)
    assert len(components) == 2
    assert sorted(sorted(c) for c in components) == [[0, 1], [2, 3]]


def test_has_path(undirected):
    assert u_algorithms.has_path(undirected, 0, 4)

    isolated = UndirectedWeightedGraph(3)
    isolated.add_edge(0, 1, 1)
    assert not u_algorithms.has_path(isolated, 0, 2)


# ------------------------------------------------------------- shortest paths


def test_dijkstra_finds_shortest_weighted_paths(undirected):
    """
    The cheapest route to vertex 1 goes 0->2->1 for 3, not 0->1 for 4.

    A BFS would return the direct edge, so this case distinguishes a real
    Dijkstra from an unweighted traversal wearing its name.
    """
    assert list(u_algorithms.dijkstra(undirected, 0)) == EXPECTED_DISTANCES


def test_dijkstra_agrees_with_bellman_ford(undirected):
    """Two different algorithms, same answer on non-negative weights."""
    distances, has_negative_cycle = u_algorithms.bellman_ford(undirected, 0)
    assert list(distances) == list(u_algorithms.dijkstra(undirected, 0))
    assert has_negative_cycle is False


def test_dijkstra_on_a_directed_graph(directed):
    assert list(d_algorithms.dijkstra(directed, 0)) == EXPECTED_DISTANCES


def test_bellman_ford_detects_a_negative_cycle():
    """
    The reason Bellman-Ford exists. Dijkstra would return nonsense here.

    A negative cycle means no shortest path exists at all, and the extra Vth
    relaxation pass is what detects it.
    """
    graph = DirectedWeightedGraph(3)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, -1)
    graph.add_edge(2, 0, -1)

    _, has_negative_cycle = d_algorithms.bellman_ford(graph, 0)
    assert has_negative_cycle is True


def test_bellman_ford_handles_negative_edges_without_a_cycle():
    """Negative weights alone are fine; only negative CYCLES are fatal."""
    graph = DirectedWeightedGraph(3)
    graph.add_edge(0, 1, 4)
    graph.add_edge(0, 2, 5)
    graph.add_edge(2, 1, -3)

    distances, has_negative_cycle = d_algorithms.bellman_ford(graph, 0)
    assert has_negative_cycle is False
    assert distances[1] == 2, "0->2->1 costs 5 + (-3) = 2, beating the direct 4"


def test_floyd_warshall_computes_all_pairs(undirected):
    """Row 0 of the all-pairs matrix must match Dijkstra from vertex 0."""
    matrix = u_algorithms.floyd_warshall(undirected)
    assert list(matrix[0]) == EXPECTED_DISTANCES


def test_floyd_warshall_diagonal_is_zero(undirected):
    matrix = u_algorithms.floyd_warshall(undirected)
    for i in range(undirected.vertex_count()):
        assert matrix[i][i] == 0


def test_floyd_warshall_is_symmetric_for_undirected_graphs(undirected):
    matrix = u_algorithms.floyd_warshall(undirected)
    n = undirected.vertex_count()
    for i in range(n):
        for j in range(n):
            assert matrix[i][j] == matrix[j][i]


def test_shortest_path_dag_matches_dijkstra(directed):
    """
    On a DAG, relaxing in topological order beats Dijkstra and allows negatives.

    Same answers here because all weights are positive.
    """
    assert list(d_advanced.shortest_path_dag(directed, 0)) == EXPECTED_DISTANCES


# ---------------------------------------------------------------------- MST


def test_kruskal_and_prim_agree_on_total_weight(undirected):
    """
    Different strategies, same cost. An MST's weight is unique even when the
    particular set of edges is not, so total weight is the right assertion.
    """
    kruskal_edges, kruskal_total = mst.kruskal_mst(undirected)
    prim_edges, prim_total = mst.prim_mst(undirected, 0)

    assert kruskal_total == prim_total == MST_WEIGHT
    assert len(kruskal_edges) == len(prim_edges) == undirected.vertex_count() - 1


def test_mst_has_exactly_v_minus_one_edges(undirected):
    edges, _ = mst.kruskal_mst(undirected)
    assert len(edges) == undirected.vertex_count() - 1


def test_mst_is_not_the_same_as_shortest_paths():
    """
    A common confusion worth pinning down with a test.

    Here the MST omits the direct 0-2 edge, so the MST path from 0 to 2 costs
    more than the true shortest path between them.
    """
    graph = UndirectedWeightedGraph(3)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 1)
    graph.add_edge(0, 2, 2)

    _, total = mst.kruskal_mst(graph)
    assert total == 2, "MST takes the two cheap edges"

    distances = u_algorithms.dijkstra(graph, 0)
    assert distances[2] == 2, "shortest path may use the direct edge"


# ------------------------------------------------------------------- advanced


def test_directed_cycle_detection():
    acyclic = DirectedWeightedGraph(3)
    acyclic.add_edge(0, 1, 1)
    acyclic.add_edge(1, 2, 1)
    assert d_advanced.has_cycle(acyclic) is False

    cyclic = DirectedWeightedGraph(3)
    cyclic.add_edge(0, 1, 1)
    cyclic.add_edge(1, 2, 1)
    cyclic.add_edge(2, 0, 1)
    assert d_advanced.has_cycle(cyclic) is True


def test_topological_sort_respects_every_edge(directed):
    """
    Rather than asserting one specific order, check the property that defines a
    topological sort: for every edge u->v, u appears before v.
    """
    order = list(d_advanced.topological_sort(directed))
    position = {vertex: index for index, vertex in enumerate(order)}

    assert len(order) == directed.vertex_count()
    for u, v, _ in EDGES:
        assert position[u] < position[v], f"edge {u}->{v} violates the ordering"


def test_transpose_reverses_every_edge(directed):
    reversed_graph = d_advanced.transpose(directed)
    for u, v, _ in EDGES:
        assert reversed_graph.has_edge(v, u)
        assert not reversed_graph.has_edge(u, v)


def test_max_flow_equals_the_min_cut():
    """
    Two paths of capacity 2 and 2 out of a source offering 3 and 2.

    0->1->3 is limited to 2 by the 1->3 edge, 0->2->3 is limited to 2 by the
    0->2 edge, so the maximum flow is 4 — the min-cut value.
    """
    graph = DirectedWeightedGraph(4)
    graph.add_edge(0, 1, 3)
    graph.add_edge(0, 2, 2)
    graph.add_edge(1, 3, 2)
    graph.add_edge(2, 3, 3)

    assert d_advanced.max_flow(graph, 0, 3) == 4


def test_max_flow_is_zero_when_the_sink_is_unreachable():
    graph = DirectedWeightedGraph(3)
    graph.add_edge(0, 1, 5)
    assert d_advanced.max_flow(graph, 0, 2) == 0


def test_find_bridges_identifies_every_edge_of_a_path():
    """In a path graph every edge is a bridge — removing any disconnects it."""
    graph = UndirectedWeightedGraph(4)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 3, 1)

    assert len(u_advanced.find_bridges(graph)) == 3


def test_a_cycle_contains_no_bridges():
    """Every edge of a cycle has an alternative route, so none is critical."""
    graph = UndirectedWeightedGraph(3)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 0, 1)

    assert len(u_advanced.find_bridges(graph)) == 0


def test_articulation_point_in_a_path():
    """The middle vertex of a 3-vertex path is the only cut vertex."""
    graph = UndirectedWeightedGraph(3)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 1)

    points = list(u_advanced.find_articulation_points(graph))
    assert points == [1]


def test_is_connected(undirected):
    assert u_advanced.is_connected(undirected) is True

    split = UndirectedWeightedGraph(4)
    split.add_edge(0, 1, 1)
    split.add_edge(2, 3, 1)
    assert u_advanced.is_connected(split) is False


# ---------------------------------------------------------------------- utils


def test_degrees(directed):
    assert d_utils.out_degree(directed, 0) == 2
    assert d_utils.in_degree(directed, 1) == 2
    assert d_utils.in_degree(directed, 0) == 0


def test_get_and_update_weight(directed):
    assert d_utils.get_weight(directed, 0, 1) == 4

    assert d_utils.update_weight(directed, 0, 1, 9.0) is True
    assert d_utils.get_weight(directed, 0, 1) == 9.0

    assert d_utils.update_weight(directed, 1, 0, 9.0) is False, "no such edge"


def test_graph_density(directed):
    """5 edges out of the 20 possible directed pairs on 5 vertices."""
    assert d_utils.graph_density(directed) == pytest.approx(0.25)


def test_clear_removes_every_edge(directed):
    d_utils.clear(directed)
    assert directed.edge_count() == 0
