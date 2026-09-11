"""
Tests for the drill system.

The study tool needs to be at least as trustworthy as the algorithms it drills:
if stub generation silently produces a file that cannot parse, or the scheduler
loses a streak, you stop believing the tool and stop using it.
"""

import ast
import json
from datetime import date, timedelta

import pytest

import curriculum
from drills import stubs
from drills.grade import grade
from drills.schedule import FAIL_INTERVAL_DAYS, INTERVALS, History, Record

SAMPLE_SLUGS = ["quick_sort", "binary_search", "stack", "min_heap", "trie", "bst"]


# ----------------------------------------------------------------- stubs


@pytest.mark.parametrize("topic", curriculum.ALL_TOPICS, ids=curriculum.slugs())
def test_every_topic_generates_parseable_stub(topic):
    """
    A stub that does not parse is useless and the failure would be confusing.

    Generating from the real file via ast means this also catches a reference file
    whose syntax has broken.
    """
    text = stubs.render_stub(topic)
    ast.parse(text)  # raises SyntaxError on failure


@pytest.mark.parametrize("slug", SAMPLE_SLUGS)
def test_stub_hides_the_implementation(slug):
    """
    Every body must be a NotImplementedError; none of the real logic survives.

    The docstrings and signatures stay — those are the contract, not the answer.
    """
    topic = curriculum.get(slug)
    tree = ast.parse(stubs.render_stub(topic))

    def bodies(node):
        for child in ast.walk(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield child

    functions = list(bodies(tree))
    assert functions, f"{slug}: stub contains no functions at all"

    for function in functions:
        statements = [s for s in function.body if not _is_docstring(s)]
        assert len(statements) == 1, f"{slug}.{function.name}: expected one statement"
        assert isinstance(statements[0], ast.Raise), (
            f"{slug}.{function.name}: body is not a raise"
        )


def _is_docstring(node) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)


@pytest.mark.parametrize("slug", SAMPLE_SLUGS)
def test_stub_preserves_signatures(slug):
    """The stub's top-level names match the reference's top-level names."""
    topic = curriculum.get(slug)
    reference = ast.parse((stubs.REPO_ROOT / topic.path).read_text(encoding="utf-8"))
    stub = ast.parse(stubs.render_stub(topic))

    def top_level_names(tree):
        return {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }

    assert top_level_names(stub) == top_level_names(reference)


def test_stub_mentions_the_invariant():
    """The banner must carry the invariant; it is the only hint you get."""
    topic = curriculum.get("quick_sort")
    text = stubs.render_stub(topic)
    assert "Invariant" in text
    assert "partition" in text


def test_create_attempt_does_not_clobber_existing_work(tmp_path, monkeypatch):
    """Losing a half-finished attempt to a re-run would be unforgivable."""
    monkeypatch.setattr(stubs, "ATTEMPTS_DIR", tmp_path)
    topic = curriculum.get("bubble_sort")

    path, written_first = stubs.create_attempt(topic)
    assert written_first
    path.write_text("# my work in progress\n", encoding="utf-8")

    same_path, written_again = stubs.create_attempt(topic)
    assert same_path == path
    assert written_again is False
    assert path.read_text(encoding="utf-8") == "# my work in progress\n"


def test_create_attempt_overwrites_when_asked(tmp_path, monkeypatch):
    monkeypatch.setattr(stubs, "ATTEMPTS_DIR", tmp_path)
    topic = curriculum.get("bubble_sort")

    path, _ = stubs.create_attempt(topic)
    path.write_text("# stale\n", encoding="utf-8")

    path, written = stubs.create_attempt(topic, overwrite=True)
    assert written
    assert "NotImplementedError" in path.read_text(encoding="utf-8")


# -------------------------------------------------------------- schedule


def test_new_record_is_flagged_new():
    record = Record(slug="x")
    assert record.is_new
    assert record.days_until_due() is None
    assert record.accuracy() is None


def test_passing_advances_the_interval():
    """
    Each consecutive pass pushes the next review further out.

    That expansion is the entire mechanism: a topic you keep getting right should
    stop consuming your time.
    """
    history = History()
    for expected_gap in INTERVALS:
        record = history.record_attempt("quick_sort", passed=True)
        due = date.fromisoformat(record.next_due)
        assert due == date.today() + timedelta(days=expected_gap)


def test_interval_stops_growing_at_the_last_step():
    history = History()
    for _ in range(len(INTERVALS) + 3):
        record = history.record_attempt("quick_sort", passed=True)
    due = date.fromisoformat(record.next_due)
    assert due == date.today() + timedelta(days=INTERVALS[-1])


def test_failing_resets_the_streak_and_brings_it_back_tomorrow():
    """
    A fail collapses the interval rather than stepping back one notch.

    A topic you got wrong is a topic you do not know, so it starts again.
    """
    history = History()
    for _ in range(4):
        history.record_attempt("quick_sort", passed=True)

    record = history.record_attempt("quick_sort", passed=False)

    assert record.streak == 0
    assert record.last_result == "fail"
    due = date.fromisoformat(record.next_due)
    assert due == date.today() + timedelta(days=FAIL_INTERVAL_DAYS)


def test_counts_accumulate():
    history = History()
    history.record_attempt("stack", passed=True)
    history.record_attempt("stack", passed=False)
    history.record_attempt("stack", passed=True)

    record = history.get("stack")
    assert (record.attempts, record.passes, record.fails) == (3, 2, 1)
    assert record.accuracy() == pytest.approx(2 / 3)
    assert record.streak == 1, "the trailing pass restarts the streak at 1"


def test_overdue_topics_come_before_unseen_ones():
    """
    Forgetting is more urgent than never having learned.

    A topic whose review date has passed must be offered before a brand-new one.
    """
    history = History()
    history.record_attempt("quick_sort", passed=True)
    history.get("quick_sort").next_due = (date.today() - timedelta(days=5)).isoformat()

    due = history.due_topics()
    assert due[0].slug == "quick_sort"


def test_topics_not_yet_due_are_excluded():
    history = History()
    history.record_attempt("quick_sort", passed=True)  # due tomorrow

    due_slugs = [t.slug for t in history.due_topics()]
    assert "quick_sort" not in due_slugs


def test_weakest_topics_ranks_by_pass_rate():
    history = History()
    for _ in range(4):
        history.record_attempt("stack", passed=True)
    for _ in range(4):
        history.record_attempt("queue", passed=False)

    weakest = [t.slug for t in history.weakest_topics(limit=2)]
    assert weakest[0] == "queue"


def test_round_trip_through_disk(tmp_path):
    """History must survive a save/load cycle intact."""
    path = tmp_path / "history.json"
    history = History()
    history.record_attempt("quick_sort", passed=True)
    history.record_attempt("stack", passed=False)
    history.save(path)

    reloaded = History.load(path)
    assert reloaded.get("quick_sort").passes == 1
    assert reloaded.get("stack").fails == 1
    assert reloaded.get("quick_sort").next_due == history.get("quick_sort").next_due


def test_corrupt_history_file_starts_fresh_instead_of_crashing(tmp_path):
    """
    A malformed progress file must not stop you revising.

    Refusing to start because the JSON is broken would be a worse failure than
    losing the history.
    """
    path = tmp_path / "history.json"
    path.write_text("{not valid json", encoding="utf-8")

    history = History.load(path)
    assert history.records == {}


def test_missing_history_file_starts_fresh(tmp_path):
    assert History.load(tmp_path / "absent.json").records == {}


def test_unknown_fields_in_history_are_ignored(tmp_path):
    """Forward compatibility: a newer file must not break an older reader."""
    path = tmp_path / "history.json"
    path.write_text(
        json.dumps({"version": 99, "records": {"stack": {"attempts": 2, "from_future": True}}}),
        encoding="utf-8",
    )

    history = History.load(path)
    assert history.get("stack").attempts == 2


def test_reset_one_topic_leaves_the_others():
    history = History()
    history.record_attempt("stack", passed=True)
    history.record_attempt("queue", passed=True)

    assert history.reset("stack") == 1
    assert "stack" not in history.records
    assert "queue" in history.records


def test_reset_all_clears_everything():
    history = History()
    history.record_attempt("stack", passed=True)
    history.record_attempt("queue", passed=True)

    assert history.reset() == 2
    assert history.records == {}


# ----------------------------------------------------------------- grading


def test_grading_an_unfilled_stub_fails(tmp_path, monkeypatch):
    """
    The stub itself must not pass. If it did, the whole exercise would be a no-op.
    """
    monkeypatch.setattr(stubs, "ATTEMPTS_DIR", tmp_path)
    topic = curriculum.get("bubble_sort")
    path, _ = stubs.create_attempt(topic)

    result = grade(topic, path)
    assert result.graded
    assert not result.passed


def test_grading_a_correct_attempt_passes(tmp_path):
    """A correct implementation placed in an attempt file must be graded PASS."""
    topic = curriculum.get("bubble_sort")
    path = tmp_path / "bubble_sort.py"
    path.write_text(
        "def bubble_sort(arr):\n"
        "    n = len(arr)\n"
        "    for i in range(n):\n"
        "        swapped = False\n"
        "        for j in range(n - i - 1):\n"
        "            if arr[j] > arr[j + 1]:\n"
        "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
        "                swapped = True\n"
        "        if not swapped:\n"
        "            break\n"
        "    return arr\n",
        encoding="utf-8",
    )

    result = grade(topic, path)
    assert result.passed, result.failures


def test_grading_an_incorrect_attempt_fails(tmp_path):
    """A sort that drops elements must not be graded PASS."""
    topic = curriculum.get("bubble_sort")
    path = tmp_path / "bubble_sort.py"
    path.write_text("def bubble_sort(arr):\n    return sorted(arr)[:-1]\n", encoding="utf-8")

    result = grade(topic, path)
    assert not result.passed


def test_grading_reports_a_missing_entry_point(tmp_path):
    """A file with the wrong function name gets a clear message, not a traceback."""
    topic = curriculum.get("bubble_sort")
    path = tmp_path / "bubble_sort.py"
    path.write_text("def not_the_right_name(arr):\n    return arr\n", encoding="utf-8")

    result = grade(topic, path)
    assert not result.passed
    assert any("bubble_sort" in failure for failure in result.failures)


def test_ungradable_topics_say_so_rather_than_failing(tmp_path):
    """
    A predicate-style search cannot use the array contract.

    Reporting 'not automatically graded' is honest; reporting FAIL would be a lie
    that trains the wrong reflex.
    """
    topic = curriculum.get("ubiquitous_binary_search")
    path = tmp_path / "ubiquitous.py"
    path.write_text(
        "def ubiquitous_binary_search(predicate, lo, hi):\n"
        "    while lo < hi:\n"
        "        mid = lo + (hi - lo) // 2\n"
        "        if predicate(mid):\n"
        "            hi = mid\n"
        "        else:\n"
        "            lo = mid + 1\n"
        "    return lo\n",
        encoding="utf-8",
    )

    result = grade(topic, path)
    assert result.graded is False
    assert result.note
