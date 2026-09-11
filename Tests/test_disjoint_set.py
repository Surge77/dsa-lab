"""
Tests for union-find, which had none before.

The module was unreachable: `disjoint_set_algorithms.py` began with
`from disjoint_set_base import DisjointSet`, a Python-2 implicit relative import
that raises ModuleNotFoundError under Python 3. Nothing could import it, so
nothing tested it.
"""

import pytest

from Non_Linear.disjoint_set.disjoint_set_algorithms import (
    detect_cycle_undirected,
    kruskal_mst,
)
from Non_Linear.disjoint_set.disjoint_set_base import DisjointSet


@pytest.fixture
def ds():
    return DisjointSet(6)


def test_every_element_starts_in_its_own_set(ds):
    assert ds.count_sets() == 6
    for i in range(6):
        assert ds.find(i) == i
        for j in range(6):
            if i != j:
                assert not ds.connected(i, j)


def test_union_merges_two_sets(ds):
    ds.union(0, 1)
    assert ds.connected(0, 1)
    assert ds.count_sets() == 5


def test_union_is_transitive(ds):
    """
    The property that makes union-find useful: connectivity propagates.

    Merging 0-1 and 1-2 must make 0 and 2 connected without anyone asking for it.
    """
    ds.union(0, 1)
    ds.union(1, 2)
    assert ds.connected(0, 2)
    assert ds.find(0) == ds.find(2)


def test_union_of_already_connected_elements_is_a_no_op(ds):
    ds.union(0, 1)
    before = ds.count_sets()
    ds.union(1, 0)
    assert ds.count_sets() == before


def test_union_is_symmetric(ds):
    ds.union(3, 4)
    assert ds.connected(3, 4)
    assert ds.connected(4, 3)


def test_separate_components_stay_separate(ds):
    ds.union(0, 1)
    ds.union(2, 3)
    assert not ds.connected(0, 2)
    assert ds.count_sets() == 4


def test_unioning_everything_leaves_one_set(ds):
    for i in range(5):
        ds.union(i, i + 1)
    assert ds.count_sets() == 1
    assert all(ds.connected(0, i) for i in range(6))


def test_find_returns_the_same_root_for_a_whole_component(ds):
    """All members of a component must agree on their representative."""
    ds.union(0, 1)
    ds.union(2, 3)
    ds.union(1, 3)
    roots = {ds.find(i) for i in (0, 1, 2, 3)}
    assert len(roots) == 1


def test_path_compression_flattens_deep_chains():
    """
    After find(), every node on the path should point straight at the root.

    Without compression these chains stay long and find() degrades to O(n), which
    is the whole reason the optimisation exists.
    """
    ds = DisjointSet(10)
    for i in range(9):
        ds.union(i, i + 1)

    root = ds.find(0)
    ds.find(9)  # walk the longest path, compressing it

    assert all(ds.parent.get(i) == root or i == root for i in range(10)), (
        "find() did not compress the path it walked"
    )


def test_out_of_range_elements_are_rejected(ds):
    """The base class validates with ValueError, not IndexError."""
    with pytest.raises(ValueError, match="out of bounds"):
        ds.find(6)
    with pytest.raises(ValueError, match="out of bounds"):
        ds.find(-1)


def test_len_reports_the_element_count(ds):
    assert len(ds) == 6


# ------------------------------------------------------------------ algorithms


def test_detect_cycle_finds_a_triangle():
    assert detect_cycle_undirected(3, [(0, 1), (1, 2), (2, 0)]) is True


def test_detect_cycle_accepts_a_tree():
    """A tree on n vertices has n-1 edges and no cycle."""
    assert detect_cycle_undirected(4, [(0, 1), (1, 2), (1, 3)]) is False


def test_detect_cycle_on_a_forest():
    """Two disconnected trees still contain no cycle."""
    assert detect_cycle_undirected(6, [(0, 1), (2, 3), (4, 5)]) is False


def test_detect_cycle_on_an_empty_edge_list():
    assert detect_cycle_undirected(3, []) is False


def test_detect_cycle_catches_a_duplicate_edge():
    """
    A repeated edge is a 2-cycle under union-find.

    Whether that counts as a cycle is a modelling decision; this records which
    answer the implementation gives so a future change is visible.
    """
    assert detect_cycle_undirected(2, [(0, 1), (0, 1)]) is True


def test_kruskal_builds_a_minimum_spanning_tree():
    """
    Edges are (u, v, weight). The MST of this 4-vertex graph costs 6.

    Kruskal sorts edges cheapest-first and accepts one only if it joins two
    different components — which is exactly the question union-find answers.
    """
    edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)]
    mst_edges, total = kruskal_mst(4, edges)

    assert total == 6
    assert len(mst_edges) == 3, "an MST on 4 vertices has exactly 3 edges"


def test_kruskal_prefers_cheaper_edges():
    """Given a choice between a cheap and an expensive edge, take the cheap one."""
    edges = [(0, 2, 100), (0, 1, 1), (1, 2, 1)]
    mst_edges, total = kruskal_mst(3, edges)

    assert total == 2
    assert sorted(edge[2] for edge in mst_edges) == [1, 1]


def test_kruskal_does_not_reorder_the_callers_edge_list():
    """
    Sorting in place would mutate an argument the caller still holds.

    The original did exactly that with `edges.sort()`.
    """
    edges = [(0, 2, 100), (0, 1, 1), (1, 2, 1)]
    snapshot = list(edges)

    kruskal_mst(3, edges)

    assert edges == snapshot


def test_kruskal_on_a_disconnected_graph_returns_a_forest():
    """
    With no edges between components, fewer than n-1 edges come back.

    Kruskal does not fail here — it silently returns a spanning forest, which is
    worth knowing before asserting on len() in production code.
    """
    edges = [(0, 1, 1), (2, 3, 1)]
    mst_edges, total = kruskal_mst(4, edges)

    assert total == 2
    assert len(mst_edges) == 2
