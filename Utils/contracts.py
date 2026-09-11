"""
What it means to be a correct sort or search, defined once.

Both the test suite (Tests/test_sorting.py, Tests/test_searching.py) and the
drill verifier (drill.py) import these, so your drill attempt is judged by
exactly the same rules as the reference implementation. There is no second,
weaker definition of correct hiding anywhere.

Each check returns a list of human-readable failure strings — empty means pass.
Returning strings rather than raising lets the drill report every problem at
once instead of stopping at the first.
"""

from collections.abc import Callable, Sequence
from typing import Any

# --------------------------------------------------------------------- domains

GENERAL = "general"  # any comparable numbers: ints, floats, negatives
INT_ANY = "int_any"  # integers including negatives, no floats
INT_NONNEG = "int_nonneg"  # non-negative integers only
TINY = "tiny"  # correct but so slow that n must stay small
FILE_BASED = "file_based"  # operates on files, not lists — tested separately

# Why each restricted sort is restricted. Kept here rather than in curriculum/
# because it is test configuration, not teaching material.
SORT_DOMAINS: dict[str, str] = {
    "counting_sort": INT_ANY,  # indexes a count array by value
    "pigeonhole_sort": INT_ANY,  # same, and rebuilds values from counts
    "radix_sort": INT_NONNEG,  # digit extraction assumes non-negative
    "sleep_sort": INT_NONNEG,  # a negative sleep is meaningless
    "bogosort": TINY,  # factorial expected time
    "stooge_sort": TINY,  # O(n^2.71)
    "external_merge_sort": FILE_BASED,
    "polyphase_sort": FILE_BASED,
}

# Sorts that do not promise to preserve the order of equal elements.
UNSTABLE_SORTS = {
    "selection_sort", "quick_sort", "heap_sort", "shell_sort", "intro_sort",
    "comb_sort", "pancake_sort", "stooge_sort", "bogosort", "sleep_sort",
    "tree_sort", "cartesian_tree_sort", "bitonic_sort", "polyphase_sort",
}


def cases_for(domain: str = GENERAL) -> dict[str, list[Any]]:
    """
    The input table a sort must handle, narrowed to what `domain` permits.

    Every sort sees the same named cases where its domain allows, which is what
    makes the parametrized suite a genuine apples-to-apples comparison.
    """
    base: dict[str, list[Any]] = {
        "empty": [],
        "single": [7],
        "two_sorted": [1, 2],
        "two_reversed": [2, 1],
        "all_equal": [4, 4, 4, 4],
        "duplicates": [3, 1, 3, 2, 1],
        "sorted": [1, 2, 3, 4, 5, 6],
        "reversed": [6, 5, 4, 3, 2, 1],
        "nearly_sorted": [1, 2, 4, 3, 5, 6],
        "random_small": [5, 1, 4, 2, 8, 3],
        "power_of_two": [8, 3, 5, 1, 7, 2, 6, 4],
    }

    if domain == TINY:
        return {k: v for k, v in base.items() if len(v) <= 6}

    base["random_medium"] = [42, 7, 19, 3, 88, 1, 56, 23, 9, 71, 4, 64, 15]
    base["large_reversed"] = list(range(40, 0, -1))

    if domain == INT_NONNEG:
        return base

    base["negatives"] = [3, -1, 0, -5, 2]
    base["all_negative"] = [-3, -1, -7, -2]

    if domain == INT_ANY:
        return base

    base["floats"] = [2.5, 1.1, 3.9, 0.2]
    base["mixed_numeric"] = [3, 1.5, -2, 0, 2.25]
    return base


def _result_of(sort_fn: Callable, values: Sequence[Any]) -> list[Any]:
    """
    Run a sort and read its output, whether it sorts in place or returns a list.

    The repo contains both conventions and a drill attempt may pick either, so
    the contract accepts both rather than forcing one.
    """
    working = list(values)
    returned = sort_fn(working)
    return list(returned) if isinstance(returned, list) else working


def check_sort(
    sort_fn: Callable,
    domain: str = GENERAL,
    check_stability: bool = False,
) -> list[str]:
    """
    Verify `sort_fn` against the full case table for `domain`.

    Returns a list of failure descriptions; empty means it passed.
    """
    failures: list[str] = []

    for name, values in cases_for(domain).items():
        expected = sorted(values)
        try:
            actual = _result_of(sort_fn, values)
        except Exception as exc:
            failures.append(f"{name}: raised {type(exc).__name__}: {exc}")
            continue
        if actual != expected:
            failures.append(f"{name}: {values} -> {actual}, expected {expected}")

    failures.extend(_check_does_not_corrupt_input(sort_fn, domain))

    if check_stability:
        failures.extend(_check_stability(sort_fn))

    return failures


def _check_does_not_corrupt_input(sort_fn: Callable, domain: str) -> list[str]:
    """A sort must permute its input, never invent, drop, or duplicate values."""
    values = cases_for(domain)["random_small"]
    try:
        actual = _result_of(sort_fn, values)
    except Exception:
        return []  # already reported by the main loop
    if sorted(actual) != sorted(values):
        return [f"multiset changed: {sorted(values)} -> {sorted(actual)}"]
    return []


def _check_stability(sort_fn: Callable) -> list[str]:
    """
    Equal keys must come out in their original relative order.

    Records are (key, tag) tuples: tuple comparison falls back to the tag, which
    would mask instability, so the tags are assigned in increasing order and the
    check reads them back rather than comparing tuples directly.
    """
    records = [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]
    try:
        actual = _result_of(sort_fn, records)
    except Exception as exc:
        return [f"stability: raised {type(exc).__name__}: {exc}"]

    for key in (1, 2):
        tags = [tag for k, tag in actual if k == key]
        if tags != sorted(tags):
            return [f"stability: key {key} came out as {tags}, expected ascending tags"]
    return []


# -------------------------------------------------------------------- searches

SEARCH_HAYSTACK = [1, 3, 5, 7, 9, 11, 13]


def check_search(search_fn: Callable, sorted_input: bool = True) -> list[str]:
    """
    Verify a search that returns an index, or -1 when the target is absent.

    Every search in the lab returns an index into the array it was given, so one
    contract covers the whole family. Predicate-style search (ubiquitous) and
    pattern search (sublist) have different shapes and are tested separately.
    """
    failures: list[str] = []
    haystack = list(SEARCH_HAYSTACK) if sorted_input else [9, 1, 13, 5, 3, 11, 7]

    for target in haystack:
        expected = haystack.index(target)
        try:
            actual = search_fn(list(haystack), target)
        except Exception as exc:
            failures.append(f"find {target}: raised {type(exc).__name__}: {exc}")
            continue
        if actual != expected:
            failures.append(f"find {target}: got index {actual}, expected {expected}")

    for absent in (0, 4, 14, -1):
        try:
            actual = search_fn(list(haystack), absent)
        except Exception as exc:
            failures.append(f"absent {absent}: raised {type(exc).__name__}: {exc}")
            continue
        if actual != -1:
            failures.append(f"absent {absent}: got index {actual}, expected -1")

    for name, arr in (("empty", []), ("single_hit", [5]), ("single_miss", [4])):
        target = 5
        expected = 0 if name == "single_hit" else -1
        try:
            actual = search_fn(list(arr), target)
        except Exception as exc:
            failures.append(f"{name}: raised {type(exc).__name__}: {exc}")
            continue
        if actual != expected:
            failures.append(f"{name}: got {actual}, expected {expected}")

    return failures
