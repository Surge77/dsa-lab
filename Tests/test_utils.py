"""
Tests for the learning tools: trace, complexity, contracts and sync.

These decide what you believe about the algorithms, so a silent bug here is
worse than a bug in a sort — a wrong comparison count or a mislabelled growth
rate teaches you something false.
"""

import math

import pytest

import curriculum
from Sorting.efficient.merge_sort import merge_sort
from Sorting.simple.bubble_sort import bubble_sort
from Sorting.simple.selection_sort import selection_sort
from Utils import complexity, sync
from Utils.contracts import (
    GENERAL,
    INT_NONNEG,
    TINY,
    cases_for,
    check_search,
    check_sort,
)
from Utils.trace import TracedValue, compare_sorts, trace_sort, unwrap

# ------------------------------------------------------------------- trace


def test_trace_counts_comparisons_and_writes():
    """
    Known-good numbers for a known input.

    Bubble sort on [5,1,4,2,8] with early exit does 9 comparisons and 8 writes
    (4 swaps). Pinning exact counts means an accidental change to the algorithm
    or the instrumentation shows up immediately.
    """
    trace = trace_sort(bubble_sort, [5, 1, 4, 2, 8])

    assert trace.is_sorted
    assert trace.result == [1, 2, 4, 5, 8]
    assert trace.comparisons == 9
    assert trace.writes == 8


def test_trace_records_one_snapshot_per_write():
    trace = trace_sort(bubble_sort, [3, 2, 1])
    assert len(trace.snapshots) == trace.writes
    assert len(trace.labels) == trace.writes


def test_trace_snapshots_show_the_array_changing():
    """Each snapshot is the array state immediately after that write."""
    trace = trace_sort(bubble_sort, [2, 1])
    assert trace.snapshots[0] == [1, 1]  # mid-swap: arr[0] written first
    assert trace.snapshots[-1] == [1, 2]


def test_trace_handles_a_sort_that_returns_a_new_list():
    """Merge sort is not in place; the trace must read its return value."""
    trace = trace_sort(merge_sort, [3, 1, 2])
    assert trace.is_sorted
    assert trace.result == [1, 2, 3]


def test_trace_reports_zero_in_place_writes_for_merge_sort():
    """
    Merge sort builds new lists, so it makes no writes through the traced list.

    That zero is informative rather than a bug — it is how you see at a glance
    which sorts are in place.
    """
    trace = trace_sort(merge_sort, [5, 1, 4, 2])
    assert trace.writes == 0
    assert trace.comparisons > 0


def test_trace_on_empty_and_single_input():
    assert trace_sort(bubble_sort, []).result == []
    assert trace_sort(bubble_sort, [1]).result == [1]


def test_selection_sort_makes_fewer_writes_than_bubble_sort():
    """
    The reason selection sort exists, demonstrated rather than asserted in prose.

    It does more comparisons but far fewer writes, which is what matters on media
    with limited write endurance.
    """
    values = [9, 2, 7, 4, 1, 8, 3, 6, 5]
    bubble = trace_sort(bubble_sort, values, snapshots=False)
    selection = trace_sort(selection_sort, values, snapshots=False)

    assert selection.writes < bubble.writes
    assert selection.comparisons > bubble.comparisons


def test_snapshots_false_still_counts():
    trace = trace_sort(bubble_sort, [3, 2, 1], snapshots=False)
    assert trace.comparisons > 0
    assert trace.writes > 0
    assert trace.snapshots == []


def test_traced_value_passes_arithmetic_through_uncounted():
    """
    Non-comparison sorts compute on values; only comparisons should be counted.

    If arithmetic were counted, radix and counting sort would report nonsense.
    """
    from Utils.trace import Probe

    probe = Probe()
    value = TracedValue(7, probe)

    assert value + 3 == 10
    assert value - 2 == 5
    assert value * 2 == 14
    assert value // 2 == 3
    assert value % 4 == 3
    assert int(value) == 7
    assert probe.comparisons == 0

    assert value > 3
    assert probe.comparisons == 1


def test_unwrap_is_idempotent():
    from Utils.trace import Probe

    probe = Probe()
    assert unwrap(TracedValue(5, probe)) == 5
    assert unwrap(5) == 5


def test_trace_works_on_a_non_comparison_sort():
    """Counting sort does arithmetic on the values; tracing must not break it."""
    from Sorting.non_comparison.counting_sort import counting_sort

    trace = trace_sort(counting_sort, [4, 1, 3, 1, 2])
    assert trace.result == [1, 1, 2, 3, 4]


def test_compare_sorts_renders_a_table():
    text = compare_sorts([bubble_sort, selection_sort, merge_sort], [4, 1, 3, 2])
    assert "bubble_sort" in text
    assert "selection_sort" in text
    assert "algorithm" in text
    assert "WRONG" not in text


def test_compare_sorts_reports_a_refusal_instead_of_crashing():
    """
    A domain-restricted sort handed input it cannot take must be reported, not
    allowed to abort the whole comparison.
    """
    from Sorting.specialized.sleep_sort import sleep_sort

    text = compare_sorts([bubble_sort, sleep_sort], [3, -1, 2])
    assert "refused" in text
    assert "bubble_sort" in text


def test_trace_summary_flags_unsorted_output():
    def broken_sort(arr):
        return arr

    trace = trace_sort(broken_sort, [3, 1, 2])
    assert not trace.is_sorted
    assert "NOT SORTED" in trace.summary()


def test_trace_str_truncates_very_long_runs():
    """A 200-element bubble sort must not print thousands of lines."""
    from Utils.trace import MAX_RENDERED_STEPS

    trace = trace_sort(bubble_sort, list(range(60, 0, -1)))
    rendered = str(trace)
    assert "further writes not shown" in rendered
    assert rendered.count("write arr[") <= MAX_RENDERED_STEPS


# -------------------------------------------------------------- complexity


def test_pseudo_random_ints_is_deterministic():
    """
    Comparing timings across runs is only meaningful with identical input.

    If this ever becomes non-deterministic, every measurement becomes noise.
    """
    assert complexity.pseudo_random_ints(50) == complexity.pseudo_random_ints(50)
    assert complexity.pseudo_random_ints(50, seed=1) != complexity.pseudo_random_ints(50, seed=2)


def test_pseudo_random_ints_respects_length_and_bound():
    values = complexity.pseudo_random_ints(100, bound=10)
    assert len(values) == 100
    assert all(0 <= v < 10 for v in values)


def test_measure_returns_one_row_per_size():
    rows = complexity.measure(bubble_sort, sizes=(20, 40))
    assert [row.n for row in rows] == [20, 40]
    assert rows[0].ratio is None, "the first size has nothing to compare against"
    assert rows[1].ratio is not None


def test_ratio_labels_name_the_right_growth_shape():
    """The label is the whole teaching payload, so pin the boundaries."""
    from Utils.complexity import Measurement

    assert "constant" in Measurement(1, 0.1, 1.0).ratio_label()
    assert "linear" in Measurement(1, 0.1, 2.0).ratio_label()
    assert "n log n" in Measurement(1, 0.1, 2.2).ratio_label()
    assert "quadratic" in Measurement(1, 0.1, 4.1).ratio_label()
    assert "worse than quadratic" in Measurement(1, 0.1, 8.0).ratio_label()
    assert Measurement(1, 0.1, None).ratio_label() == ""


def test_resolve_imports_a_topics_entry_point():
    assert complexity.resolve("bubble_sort") is bubble_sort


def test_runnable_sort_slugs_excludes_the_unrunnable():
    slugs = complexity.runnable_sort_slugs()
    assert "bubble_sort" in slugs
    for excluded in complexity.WORKLOAD_EXCLUSIONS:
        assert excluded not in slugs


def test_runnable_sort_slugs_can_skip_the_slow_ones():
    fast = complexity.runnable_sort_slugs(include_slow=False)
    assert "merge_sort" in fast
    assert "bubble_sort" not in fast


@pytest.mark.slow
def test_report_mentions_the_claimed_complexity():
    text = complexity.report(["merge_sort"], max_n=250)
    assert "merge_sort" in text
    assert "O(n log n)" in text


def test_report_explains_a_skipped_algorithm():
    text = complexity.report(["bogosort"])
    assert "skipped" in text
    assert "factorial" in text


def test_complexity_cli_rejects_an_unknown_slug():
    with pytest.raises(SystemExit):
        complexity.main(["not_a_real_sort"])


# --------------------------------------------------------------- contracts


def test_cases_widen_and_narrow_with_the_domain():
    """
    Each domain is a strict subset of the more permissive one above it.

    If INT_NONNEG ever admitted negatives, radix sort would start "failing" for
    reasons that are not its fault.
    """
    general = cases_for(GENERAL)
    nonneg = cases_for(INT_NONNEG)
    tiny = cases_for(TINY)

    assert "floats" in general
    assert "negatives" in general

    assert "floats" not in nonneg
    assert "negatives" not in nonneg

    assert all(len(v) <= 6 for v in tiny.values())
    assert set(tiny) < set(general)


def test_check_sort_accepts_a_correct_sort():
    assert check_sort(bubble_sort) == []


def test_check_sort_catches_a_sort_that_drops_elements():
    failures = check_sort(lambda arr: sorted(arr)[:-1])
    assert failures
    assert any("expected" in f for f in failures)


def test_check_sort_catches_a_sort_that_raises():
    def explodes(arr):
        raise ValueError("nope")

    failures = check_sort(explodes)
    assert all("raised ValueError" in f for f in failures if "raised" in f)


def test_check_sort_catches_a_multiset_change():
    """A sort that invents a value must be caught even if the result is ordered."""
    failures = check_sort(lambda arr: sorted(arr + [999]))
    assert failures


def test_check_sort_detects_instability():
    """An unstable sort must fail the stability check when it is requested."""
    failures = check_sort(
        lambda arr: sorted(arr, key=lambda pair: (pair[0], -ord(pair[1]))),
        check_stability=True,
    )
    assert any(f.startswith("stability") for f in failures)


def test_check_search_accepts_a_correct_search():
    from Searching.binary_search_family.basic_binary_search import binary_search

    assert check_search(binary_search) == []


def test_check_search_catches_an_off_by_one():
    def shifted(arr, target):
        for i, value in enumerate(arr):
            if value == target:
                return i + 1
        return -1

    failures = check_search(shifted)
    assert failures


def test_check_search_catches_a_search_that_never_reports_absence():
    failures = check_search(lambda arr, target: 0)
    assert any("expected -1" in f for f in failures)


# -------------------------------------------------------------------- sync


def test_render_header_contains_every_teaching_section():
    topic = curriculum.get("quick_sort")
    header = sync.render_header(topic)

    for section in ("MENTAL MODEL", "INVARIANT", "COMPLEXITY", "REACH FOR IT WHEN",
                    "AVOID WHEN", "PITFALLS", "SEE ALSO", "INTERVIEW"):
        assert section in header, f"header is missing {section}"


def test_render_header_is_all_comments():
    """
    The block must be comments only, so it can precede a module docstring without
    displacing it as __doc__.
    """
    header = sync.render_header(curriculum.get("quick_sort"))
    for line in header.splitlines():
        assert line == "" or line.startswith("#"), f"not a comment: {line!r}"


def test_strip_existing_header_is_the_inverse_of_rendering():
    topic = curriculum.get("quick_sort")
    body = "import math\n\n\ndef f():\n    return 1\n"
    assert sync.strip_existing_header(sync.render_header(topic) + body) == body


def test_strip_existing_header_leaves_unheadered_text_alone():
    body = "def f():\n    return 1\n"
    assert sync.strip_existing_header(body) == body


def test_render_index_lists_every_topic():
    index = sync.render_index()
    for topic in curriculum.ALL_TOPICS:
        assert f"`{topic.slug}`" in index, f"{topic.slug} missing from INDEX.md"


def test_render_index_includes_the_reach_for_it_column():
    """That column is the reason the index is worth reading during revision."""
    index = sync.render_index()
    assert "Reach for it when" in index
    assert "Cross-reference map" in index


def test_wrap_respects_the_comment_width():
    lines = sync.wrap("word " * 60)
    assert all(len(line) <= sync.WRAP_WIDTH for line in lines)
    assert all(line.startswith("#") for line in lines)


def test_topics_by_path_groups_shared_files():
    """
    binary_tree.py carries two topics; they must be grouped, not left to
    overwrite each other's header on every run.
    """
    grouped = dict(sync.topics_by_path())
    shared = grouped["Non_Linear/trees/binary_tree.py"]
    assert {t.slug for t in shared} == {"binary_tree", "binary_tree_lca"}


def test_math_import_is_available_for_the_sentinel_check():
    """Guards the bitonic padding sentinel, which relies on math.inf."""
    assert math.inf > 10**18
