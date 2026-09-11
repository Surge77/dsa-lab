"""
One parametrized suite covering every searching algorithm in the lab.

Before this file, `Searching/` had zero collected tests: each module carried its
own inline assertions and nine of them *executed those assertions at import
time*, printing "All tests passed." as a side effect of being imported.

Adding a search to curriculum/searching.py automatically adds it here.
"""

import contextlib
import importlib
import io
import pathlib
import sys

import pytest

import curriculum
from Utils.contracts import check_search

# Searches that take (array, target) and return an index or -1.
INDEX_SEARCH_SLUGS = [
    "linear_search",
    "recursive_linear_search",
    "bidirectional_linear_search",
    "sentinel_search",
    "binary_search",
    "recursive_binary_search",
    "exponential_search",
    "fibonacci_search",
    "interpolation_search",
    "jump_search",
    "ternary_search",
]

# Searches that do not require sorted input.
UNSORTED_OK = {"linear_search", "recursive_linear_search", "bidirectional_linear_search"}

# Different shapes, tested individually below.
SPECIAL_SLUGS = {"rotated_binary_search", "ubiquitous_binary_search", "sublist_search", "astar"}

SEARCH_TOPICS = [t for t in curriculum.ALL_TOPICS if t.is_search]


def load(slug):
    topic = curriculum.get(slug)
    module = importlib.import_module(topic.module)
    return getattr(module, topic.entry)


def test_every_search_is_registered():
    """A search file with no curriculum entry is a gap; fail loudly on it."""
    on_disk = {
        str(p).replace("\\", "/")
        for p in pathlib.Path("Searching").rglob("*.py")
        if p.name != "__init__.py"
    }
    registered = {path for t in SEARCH_TOPICS for path in t.all_paths}
    assert on_disk - registered == set(), "search files with no curriculum entry"


def test_every_search_is_covered_by_a_test():
    """Every search topic is either in the shared contract list or tested specially."""
    covered = set(INDEX_SEARCH_SLUGS) | SPECIAL_SLUGS
    uncovered = {t.slug for t in SEARCH_TOPICS} - covered
    assert not uncovered, f"search topics with no test: {sorted(uncovered)}"


@pytest.mark.parametrize("slug", INDEX_SEARCH_SLUGS)
def test_index_search_contract(slug):
    """Every index-returning search satisfies the shared contract."""
    failures = check_search(load(slug), sorted_input=True)
    assert not failures, f"{slug} failed:\n  " + "\n  ".join(failures)


@pytest.mark.parametrize("slug", sorted(UNSORTED_OK))
def test_linear_searches_work_on_unsorted_input(slug):
    """
    The linear family's whole selling point is requiring nothing of the data.

    If one of these ever fails here, it has quietly grown a sortedness
    assumption and is no longer a linear search.
    """
    failures = check_search(load(slug), sorted_input=False)
    assert not failures, f"{slug} on unsorted input:\n  " + "\n  ".join(failures)


@pytest.mark.parametrize("slug", [t.slug for t in SEARCH_TOPICS])
def test_search_leaves_no_import_side_effects(slug):
    """
    Importing a search module must print nothing.

    Nine files used to run their tests at import time; this is the regression
    test for that.
    """
    module_name = curriculum.get(slug).module
    original = sys.modules.pop(module_name, None)

    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            importlib.import_module(module_name)
    finally:
        # Re-importing replaced the module object; restore the original so tests
        # holding references to its functions still see the same objects.
        if original is not None:
            sys.modules[module_name] = original
    assert buffer.getvalue() == "", f"{module_name} printed on import: {buffer.getvalue()!r}"


def test_sentinel_search_restores_the_array_it_mutated():
    """
    The sentinel trick overwrites the last element and must put it back.

    Forgetting the restore is data corruption, not a wrong answer, so it deserves
    its own test rather than hiding inside the generic contract.
    """
    from Searching.linear_search_family.sentinel_linear_search import sentinel_search

    arr = [1, 3, 5, 7, 9]
    original = list(arr)

    sentinel_search(arr, 5)
    assert arr == original, "found case corrupted the array"

    sentinel_search(arr, 42)
    assert arr == original, "absent case corrupted the array"


def test_sentinel_search_finds_a_target_in_the_last_slot():
    """
    The element that gets overwritten is the one most easily lost.

    A sentinel implementation that does not re-check the saved last value reports
    -1 for a target that genuinely lived there.
    """
    from Searching.linear_search_family.sentinel_linear_search import sentinel_search

    assert sentinel_search([1, 3, 5, 7, 9], 9) == 4


def test_linear_search_all_returns_every_match():
    """linear_search returns the first index; linear_search_all returns them all."""
    from Searching.linear_search_family.basic_linear_search import (
        linear_search,
        linear_search_all,
    )

    arr = [4, 1, 4, 9, 4]
    assert linear_search(arr, 4) == 0
    assert linear_search_all(arr, 4) == [0, 2, 4]
    assert linear_search_all(arr, 7) == []


# --------------------------------------------------------------- rotated array


@pytest.mark.parametrize(
    "arr,target,expected_value",
    [
        ([4, 5, 6, 7, 0, 1, 2], 0, 0),
        ([4, 5, 6, 7, 0, 1, 2], 4, 4),
        ([4, 5, 6, 7, 0, 1, 2], 2, 2),
        ([1, 2, 3, 4, 5], 3, 3),  # rotation of zero
        ([5, 1, 2, 3, 4], 5, 5),  # pivot at index 0
        ([2, 1], 1, 1),
        ([1], 1, 1),
    ],
)
def test_rotated_binary_search_finds_present_values(arr, target, expected_value):
    """Works across every rotation offset, including no rotation at all."""
    from Searching.binary_search_family.rotated_binary_search import rotated_binary_search

    index = rotated_binary_search(list(arr), target)
    assert index != -1, f"{target} not found in {arr}"
    assert arr[index] == expected_value


@pytest.mark.parametrize("arr", [[4, 5, 6, 7, 0, 1, 2], [1], [], [3, 1]])
def test_rotated_binary_search_reports_absent_values(arr):
    from Searching.binary_search_family.rotated_binary_search import rotated_binary_search

    assert rotated_binary_search(list(arr), 99) == -1


# ------------------------------------------------------------ predicate search


def test_ubiquitous_binary_search_finds_the_first_true():
    """
    The general form: find the boundary of a monotone predicate.

    This single shape solves most binary-search interview problems, so it gets
    tested on an answer space rather than on an array.
    """
    from Searching.advanced.ubiquitous_binary_search import ubiquitous_binary_search

    # First n in [0, 100] with n * n >= 50  ->  8, because 7*7=49 and 8*8=64.
    assert ubiquitous_binary_search(lambda n: n * n >= 50, 0, 100) == 8

    # Boundary at the very start of the range.
    assert ubiquitous_binary_search(lambda n: n >= 0, 0, 10) == 0

    # Boundary at the very end of the range.
    assert ubiquitous_binary_search(lambda n: n >= 10, 0, 10) == 10


def test_ubiquitous_binary_search_solves_a_capacity_problem():
    """
    The shape in which it actually shows up: minimum capacity that suffices.

    Smallest ship capacity that clears these weights in 3 days. This is LeetCode
    1011 in five lines, which is the point of learning the predicate form.
    """
    from Searching.advanced.ubiquitous_binary_search import ubiquitous_binary_search

    weights = [3, 2, 2, 4, 1, 4]
    days = 3

    def can_ship(capacity: int) -> bool:
        used, load = 1, 0
        for weight in weights:
            if load + weight > capacity:
                used += 1
                load = 0
            load += weight
        return used <= days

    assert ubiquitous_binary_search(can_ship, max(weights), sum(weights)) == 6


def test_min_square_at_least_demo_still_works():
    """The worked example shipped alongside the predicate search."""
    from Searching.advanced.ubiquitous_binary_search import min_square_at_least

    assert min_square_at_least(50) == 8
    assert min_square_at_least(49) == 7
    assert min_square_at_least(0) == 0


# -------------------------------------------------------------- sublist search


@pytest.mark.parametrize(
    "haystack,needle,expected",
    [
        ([1, 2, 3, 4, 5], [3, 4], 2),
        ([1, 2, 3, 4, 5], [1, 2], 0),
        ([1, 2, 3, 4, 5], [4, 5], 3),
        ([1, 2, 3, 4, 5], [5, 6], -1),
        ([1, 2, 3], [1, 2, 3, 4], -1),
        ([], [1], -1),
        ([1, 2, 1, 2, 3], [1, 2, 3], 2),  # false start at index 0
    ],
)
def test_sublist_search(haystack, needle, expected):
    """
    Contiguous pattern matching, including the false-start case.

    [1,2,1,2,3] searching [1,2,3] is the case that separates a correct naive
    matcher from one that forgets to restart the inner walk.
    """
    from Searching.advanced.sublist_search import sublist_search

    assert sublist_search(list(haystack), list(needle)) == expected


def test_sublist_search_matches_empty_pattern_at_zero():
    """Convention, matching str.find: the empty pattern is present at index 0."""
    from Searching.advanced.sublist_search import sublist_search

    assert sublist_search([1, 2, 3], []) == 0
    assert sublist_search([], []) == 0


def test_contains_sublist_answers_the_boolean_question():
    from Searching.advanced.sublist_search import contains_sublist

    assert contains_sublist([1, 2, 3, 4], [2, 3]) is True
    assert contains_sublist([1, 2, 3, 4], [3, 2]) is False


def test_all_occurrences_includes_overlapping_matches():
    """Overlap matters: [1,1,1] contains [1,1] at both 0 and 1."""
    from Searching.advanced.sublist_search import all_occurrences

    assert all_occurrences([1, 1, 1], [1, 1]) == [0, 1]
    assert all_occurrences([1, 2, 1, 2, 1], [1, 2]) == [0, 2]
    assert all_occurrences([1, 2, 3], [9]) == []


# ------------------------------------------------------------------------ A*


def build_demo_tree():
    """
    The tree the original module demonstrated on, rebuilt as a fixture.

            A
          / | \\
         B  C  D
        / \\     |
       E   F    G  (goal)

    B->F costs 2, D->G costs 1, every other edge costs 1.
    """
    from Searching.tree_search_family.astar import TreeNode

    a, b, c, d = TreeNode("A"), TreeNode("B"), TreeNode("C"), TreeNode("D")
    e = TreeNode("E")
    f = TreeNode("F", cost=2)
    g = TreeNode("G", cost=1)
    a.children = [b, c, d]
    b.children = [e, f]
    d.children = [g]
    return a


def test_astar_finds_the_optimal_path():
    """With an admissible heuristic, the first goal pop is the optimal path."""
    from Searching.tree_search_family.astar import astar_tree_search

    def goal(node):
        return node.value == "G"

    def heuristic(node):
        return {"D": 1, "G": 0}.get(node.value, 2)

    path = astar_tree_search(build_demo_tree(), goal, heuristic)
    assert path is not None
    assert [n.value for n in path] == ["A", "D", "G"]


def test_astar_with_zero_heuristic_is_dijkstra():
    """
    h = 0 reduces A* to Dijkstra and must still find the optimal path.

    This is the standard sanity check when a heuristic is under suspicion.
    """
    from Searching.tree_search_family.astar import astar_tree_search

    path = astar_tree_search(build_demo_tree(), lambda n: n.value == "G", lambda n: 0)
    assert path is not None
    assert [n.value for n in path] == ["A", "D", "G"]


def test_astar_returns_none_when_the_goal_is_unreachable():
    from Searching.tree_search_family.astar import astar_tree_search

    path = astar_tree_search(build_demo_tree(), lambda n: n.value == "Z", lambda n: 0)
    assert path is None


def test_astar_handles_equal_f_scores_without_comparing_nodes():
    """
    Equal f-scores must not force a comparison of two TreeNode objects.

    A constant heuristic and uniform costs make ties unavoidable; without the
    tiebreaker counter in the heap tuple this raises TypeError.
    """
    from Searching.tree_search_family.astar import TreeNode, astar_tree_search

    root = TreeNode("root")
    root.children = [TreeNode(str(i)) for i in range(6)]

    path = astar_tree_search(root, lambda n: n.value == "5", lambda n: 1)
    assert path is not None
    assert [n.value for n in path] == ["root", "5"]
