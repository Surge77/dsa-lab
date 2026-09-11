"""
One parametrized suite covering every sorting algorithm in the lab.

This replaces roughly 1,300 lines of copy-pasted inline assertions that used to
sit at the bottom of each sort file and never ran under pytest. Because every
algorithm now faces the identical case table, a gap in one shows up immediately
instead of hiding behind its own bespoke tests.

Adding a sort to curriculum/sorting.py automatically adds it here.
"""

import contextlib
import importlib
import io
import pathlib
import sys

import pytest

import curriculum
from Utils.contracts import (
    FILE_BASED,
    GENERAL,
    SORT_DOMAINS,
    TINY,
    UNSTABLE_SORTS,
    check_sort,
)

SORT_TOPICS = [t for t in curriculum.ALL_TOPICS if t.is_sort]
LIST_SORT_TOPICS = [t for t in SORT_TOPICS if SORT_DOMAINS.get(t.slug) != FILE_BASED]
FILE_SORT_TOPICS = [t for t in SORT_TOPICS if SORT_DOMAINS.get(t.slug) == FILE_BASED]

SLOW_SLUGS = {"sleep_sort", "bogosort"}

UNSORTED_INPUT = [5, 1, 9, 3, 7, 4, 2, 8, 6, 0]


def load(topic):
    """Import a topic's entry point by way of its curriculum record."""
    module = importlib.import_module(topic.module)
    return getattr(module, topic.entry)


def calls_builtin_sorted(fn) -> bool:
    """
    True if `fn` references the builtin `sorted` or a `.sort()` method.

    Checks the compiled code object rather than the source text, so prose in the
    docstring explaining why the function must NOT call sorted() does not itself
    trip the check.
    """
    names = set(fn.__code__.co_names)
    return "sorted" in names or "sort" in names


def ids(topics) -> list:
    return [t.slug for t in topics]


def test_every_sort_is_registered():
    """
    Guard against a sort file existing with no curriculum entry.

    Two of these directories were previously unimportable because of hyphens in
    their names, which is exactly how six algorithms ended up with no tests at
    all. This test makes that failure mode loud.
    """
    on_disk = {
        str(p).replace("\\", "/")
        for p in pathlib.Path("Sorting").rglob("*.py")
        if p.name != "__init__.py"
    }
    registered = {path for t in SORT_TOPICS for path in t.all_paths}
    assert on_disk - registered == set(), "sort files with no curriculum entry"


@pytest.mark.parametrize("topic", LIST_SORT_TOPICS, ids=ids(LIST_SORT_TOPICS))
def test_sort_is_correct(topic):
    """Every list-based sort satisfies the shared contract for its domain."""
    if topic.slug in SLOW_SLUGS:
        pytest.skip(f"{topic.slug} is covered by its own slow test")

    domain = SORT_DOMAINS.get(topic.slug, GENERAL)
    failures = check_sort(load(topic), domain=domain)
    assert not failures, f"{topic.slug} failed:\n  " + "\n  ".join(failures)


@pytest.mark.parametrize("topic", LIST_SORT_TOPICS, ids=ids(LIST_SORT_TOPICS))
def test_stability_claim_is_honest(topic):
    """
    A sort that the curriculum calls stable must actually be stable.

    This is the check that catches a 'stable' sort whose merge takes from the
    right-hand run on ties — a bug invisible when sorting plain integers.
    """
    if topic.slug in SLOW_SLUGS or topic.stable is not True:
        pytest.skip("not claimed stable")
    if SORT_DOMAINS.get(topic.slug) in {TINY}:
        pytest.skip("domain too narrow for record input")
    if topic.slug in {"counting_sort", "pigeonhole_sort", "radix_sort", "bucket_sort"}:
        pytest.skip("non-comparison sorts index by integer value, not by record")

    failures = check_sort(load(topic), domain=GENERAL, check_stability=True)
    stability_failures = [f for f in failures if f.startswith("stability")]
    assert not stability_failures, f"{topic.slug}: " + "; ".join(stability_failures)


@pytest.mark.parametrize("topic", LIST_SORT_TOPICS, ids=ids(LIST_SORT_TOPICS))
def test_unstable_sorts_are_not_claimed_stable(topic):
    """The curriculum's stability flag agrees with the known-unstable list."""
    if topic.slug in UNSTABLE_SORTS:
        assert topic.stable is not True, (
            f"{topic.slug} is in UNSTABLE_SORTS but curriculum claims stable=True"
        )


@pytest.mark.parametrize("topic", LIST_SORT_TOPICS, ids=ids(LIST_SORT_TOPICS))
def test_sort_leaves_no_import_side_effects(topic):
    """
    Importing a sort module must print nothing and run nothing.

    Nine files used to execute their test function at import time, so merely
    importing a search printed 'All tests passed.' to stdout.
    """
    module_name = topic.module
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


# ------------------------------------------------------------- slow / special


@pytest.mark.slow
def test_bogosort_sorts_tiny_input():
    """Bogosort is correct but capped; it may legitimately give up."""
    from Sorting.specialized.bogosort import bogosort

    result = bogosort([3, 1, 2])
    assert result == [1, 2, 3]


@pytest.mark.slow
def test_bogosort_respects_attempt_cap():
    """With a tiny cap it must return rather than loop forever."""
    from Sorting.specialized.bogosort import bogosort

    bogosort([9, 8, 7, 6, 5, 4, 3, 2, 1], max_attempts=5)  # returns, does not hang


@pytest.mark.slow
@pytest.mark.flaky
def test_sleep_sort_orders_well_separated_values():
    """
    Widely separated values wake in order.

    Marked flaky on purpose: correctness here depends on the OS scheduler, not on
    the code, which is the entire lesson of the algorithm.
    """
    from Sorting.specialized.sleep_sort import sleep_sort

    assert sleep_sort([3, 1, 4, 0, 2], unit_seconds=0.05) == [0, 1, 2, 3, 4]


def test_sleep_sort_rejects_negative_values():
    from Sorting.specialized.sleep_sort import sleep_sort

    with pytest.raises(ValueError, match="non-negative"):
        sleep_sort([1, -2, 3])


def test_sleep_sort_does_not_delegate_to_builtin_sorted():
    """
    Guard against the tempting 'fix' that makes this a wrapper around sorted().

    The previous implementation ended with `return sorted(result)`, which made
    the thread machinery pure decoration. Asserting on the source is crude but it
    is the only way to catch a cheat that produces correct output.
    """
    from Sorting.specialized.sleep_sort import sleep_sort

    assert not calls_builtin_sorted(sleep_sort), (
        "sleep_sort must not call sorted() — that makes it a no-op wrapper"
    )


def test_cartesian_tree_sort_does_not_delegate_to_builtin_sorted():
    """The same guard for the other algorithm that used to cheat."""
    from Sorting.tree_based.cartesian_tree_sort import cartesian_tree_sort

    assert not calls_builtin_sorted(cartesian_tree_sort), (
        "cartesian_tree_sort must not call sorted()"
    )


def test_cartesian_tree_inorder_returns_original_order():
    """
    The defining property: inorder of a Cartesian tree is the INPUT order.

    If this ever returns sorted output, the tree construction is wrong — and the
    sort would appear to work anyway, which is how the old bug survived.
    """
    from Sorting.tree_based.cartesian_tree_sort import (
        build_cartesian_tree,
        inorder_traversal,
    )

    values = [5, 3, 7, 2, 4, 6, 8]
    assert inorder_traversal(build_cartesian_tree(values), []) == values


def test_bitonic_sort_handles_non_power_of_two_lengths():
    """Regression: this silently returned wrong output for n not a power of 2."""
    from Sorting.network.bitonic_sort import bitonic_sort

    for values in ([3, -1, 0, -5, 2], [5, 3, 7, 2, 4, 6, 8], [9, 1, 3]):
        assert bitonic_sort(list(values)) == sorted(values)


def test_bucket_sort_handles_values_outside_unit_interval():
    """Regression: the textbook [0, 1) assumption raised IndexError on ints."""
    from Sorting.non_comparison.bucket_sort import bucket_sort

    assert bucket_sort([3, 1, 2]) == [1, 2, 3]
    assert bucket_sort([120, -45, 0, 78]) == [-45, 0, 78, 120]


# ------------------------------------------------------------ external sorts


@pytest.fixture
def integer_file(tmp_path):
    """A newline-delimited integer file, plus the values it contains."""

    def make(values, name="input.txt"):
        path = tmp_path / name
        path.write_text("".join(f"{v}\n" for v in values), encoding="utf-8")
        return path

    return make


def read_integers(path: pathlib.Path) -> list:
    text = path.read_text(encoding="utf-8").strip()
    return [int(line) for line in text.splitlines()] if text else []


@pytest.mark.parametrize("topic", FILE_SORT_TOPICS, ids=ids(FILE_SORT_TOPICS))
def test_external_sort_sorts_a_file(topic, integer_file, tmp_path):
    """Both external sorts sort a file whose chunks exceed one pass."""
    sort_fn = load(topic)
    source = integer_file(UNSORTED_INPUT)
    destination = tmp_path / "out.txt"

    sort_fn(str(source), str(destination))

    assert read_integers(destination) == sorted(UNSORTED_INPUT)


@pytest.mark.parametrize("topic", FILE_SORT_TOPICS, ids=ids(FILE_SORT_TOPICS))
def test_external_sort_handles_empty_input(topic, integer_file, tmp_path):
    """Regression: polyphase_sort used to loop forever on an empty file."""
    sort_fn = load(topic)
    source = integer_file([])
    destination = tmp_path / "out.txt"

    sort_fn(str(source), str(destination))

    assert read_integers(destination) == []


@pytest.mark.parametrize("topic", FILE_SORT_TOPICS, ids=ids(FILE_SORT_TOPICS))
def test_external_sort_leaves_no_scratch_files(topic, integer_file, tmp_path):
    """
    Regression: chunk_*.txt and tape?.txt used to be left in the working
    directory, which is how four stray .txt files ended up committed at the
    repository root.
    """
    sort_fn = load(topic)
    source = integer_file(UNSORTED_INPUT)
    destination = tmp_path / "out.txt"

    sort_fn(str(source), str(destination))

    leftovers = sorted(p.name for p in tmp_path.iterdir())
    assert leftovers == ["input.txt", "out.txt"], f"scratch files left behind: {leftovers}"


def test_external_merge_sort_accepts_an_explicit_work_dir(integer_file, tmp_path):
    """A caller-supplied work dir is used and emptied of chunk files."""
    from Sorting.external.external_merge_sort import external_merge_sort

    work = tmp_path / "work"
    work.mkdir()
    source = integer_file(UNSORTED_INPUT)
    destination = tmp_path / "out.txt"

    external_merge_sort(str(source), str(destination), chunk_size=3, work_dir=str(work))

    assert read_integers(destination) == sorted(UNSORTED_INPUT)
    assert list(work.iterdir()) == []


def test_external_merge_sort_produces_more_than_one_chunk(integer_file, tmp_path):
    """
    With chunk_size smaller than the input, the merge phase must actually run.

    A chunk_size large enough to hold everything would pass the sorting test
    while never exercising the k-way merge at all.
    """
    from Sorting.external.external_merge_sort import split_and_sort

    work = tmp_path / "work"
    work.mkdir()
    source = integer_file(UNSORTED_INPUT)

    chunks = split_and_sort(str(source), 3, str(work))

    assert len(chunks) == 4
    for chunk in chunks:
        values = read_integers(pathlib.Path(chunk))
        assert values == sorted(values)
