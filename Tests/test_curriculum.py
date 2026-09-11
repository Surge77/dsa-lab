"""
The test that stops the lab rotting.

Every implementation file must have a curriculum entry, every entry must point at
code that exists and imports, every cross-reference must resolve, and INDEX.md
plus the in-file headers must match what the curriculum currently says.

Without this, INDEX.md becomes a stale artefact within a month and a new
algorithm lands with no documentation, no drill, and no index row — which is
exactly how six sorting algorithms previously ended up invisible and untested.
"""

import importlib
import pathlib

import pytest

import curriculum
from Utils import sync

SOURCE_DIRS = ["Linear", "Hash", "Non_Linear", "Searching", "Sorting"]

# Files deliberately not treated as standalone concepts, with the reason.
NOT_CONCEPTS = {
    "Non_Linear/graphs/undirected/undirected_graph_algorithms.py",
    "Non_Linear/graphs/undirected/undirected_graph_utils.py",
}


def normalise(path: pathlib.Path) -> str:
    return str(path).replace("\\", "/")


def implementation_files() -> set:
    """Every non-package Python file under the algorithm directories."""
    found = set()
    for directory in SOURCE_DIRS:
        for path in pathlib.Path(directory).rglob("*.py"):
            if path.name == "__init__.py":
                continue
            found.add(normalise(path))
    return found


def registered_files() -> set:
    """Every file claimed by some curriculum topic."""
    return {path for topic in curriculum.ALL_TOPICS for path in topic.all_paths}


def test_every_implementation_file_has_a_curriculum_entry():
    """
    No orphan implementations.

    If this fails, add a Topic to the matching curriculum module (or list the file
    in `also_covers` of the concept it belongs to).
    """
    orphans = implementation_files() - registered_files() - NOT_CONCEPTS
    assert not orphans, (
        "implementation files with no curriculum entry:\n  "
        + "\n  ".join(sorted(orphans))
    )


def test_every_curriculum_entry_points_at_a_real_file():
    """No entries for files that have been moved or deleted."""
    missing = {
        path for path in registered_files() if not pathlib.Path(path).exists()
    }
    assert not missing, f"curriculum references missing files: {sorted(missing)}"


@pytest.mark.parametrize("topic", curriculum.ALL_TOPICS, ids=curriculum.slugs())
def test_topic_entry_point_is_importable(topic):
    """
    The named module imports and the named entry point exists on it.

    Catches a renamed class or function before you discover it mid-revision.
    """
    module = importlib.import_module(topic.module)
    target = module
    for attribute in topic.entry.split("."):
        assert hasattr(target, attribute), (
            f"{topic.slug}: {topic.module} has no attribute '{attribute}' "
            f"(entry is '{topic.entry}')"
        )
        target = getattr(target, attribute)


@pytest.mark.parametrize("topic", curriculum.ALL_TOPICS, ids=curriculum.slugs())
def test_topic_cross_references_resolve(topic):
    """A `see_also` slug that does not exist is a dead link in the index."""
    dangling = [slug for slug in topic.see_also if slug not in curriculum.BY_SLUG]
    assert not dangling, f"{topic.slug} refers to unknown topics: {dangling}"


@pytest.mark.parametrize("topic", curriculum.ALL_TOPICS, ids=curriculum.slugs())
def test_topic_does_not_reference_itself(topic):
    assert topic.slug not in topic.see_also, f"{topic.slug} lists itself in see_also"


@pytest.mark.parametrize("topic", curriculum.ALL_TOPICS, ids=curriculum.slugs())
def test_topic_named_doc_exists(topic):
    """A `doc` path that does not exist would be a broken link in INDEX.md."""
    if topic.doc is None:
        pytest.skip("no longer-form note for this topic")
    assert pathlib.Path(topic.doc).exists(), f"{topic.slug} names a missing doc: {topic.doc}"


@pytest.mark.parametrize("topic", curriculum.ALL_TOPICS, ids=curriculum.slugs())
def test_topic_teaching_fields_are_substantive(topic):
    """
    Guard against placeholder entries.

    A one-line mental model is a TODO wearing a Topic's clothes; it would show up
    in INDEX.md and in the file header looking finished.
    """
    assert len(topic.mental_model) >= 80, f"{topic.slug}: mental_model too thin"
    assert len(topic.invariant) >= 30, f"{topic.slug}: invariant too thin"
    assert topic.use_when.strip(), f"{topic.slug}: use_when is empty"
    assert topic.avoid_when.strip(), f"{topic.slug}: avoid_when is empty"
    assert topic.pitfalls, f"{topic.slug}: no pitfalls recorded"


def test_index_is_in_sync_with_the_curriculum():
    """
    INDEX.md matches what the curriculum currently says.

    Fix by running `python -m Utils.sync`.
    """
    assert not sync.sync_index(check=True), (
        "INDEX.md is stale — run `python -m Utils.sync`"
    )


def test_in_file_headers_are_in_sync_with_the_curriculum():
    """
    Every generated header matches its Topic.

    Fix by running `python -m Utils.sync`.
    """
    count, paths = sync.sync_headers(check=True)
    assert count == 0, (
        "these files have stale teaching headers — run `python -m Utils.sync`:\n  "
        + "\n  ".join(paths)
    )


def test_sync_is_idempotent():
    """
    Running sync twice changes nothing the second time.

    This caught a real bug: two topics share binary_tree.py, and the first version
    of the header writer had them overwrite each other forever.
    """
    count_first, _ = sync.sync_headers(check=True)
    count_second, _ = sync.sync_headers(check=True)
    assert count_first == count_second == 0


def test_no_module_prints_on_import():
    """
    Importing any implementation module must be silent.

    Nine search modules used to run their assertions at import time.
    """
    import contextlib
    import io
    import sys

    noisy = []
    for topic in curriculum.ALL_TOPICS:
        original = sys.modules.pop(topic.module, None)
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                importlib.import_module(topic.module)
        finally:
            if original is not None:
                sys.modules[topic.module] = original
        if buffer.getvalue():
            noisy.append(f"{topic.module}: {buffer.getvalue()!r}")
    assert not noisy, "modules printing on import:\n  " + "\n  ".join(noisy)
