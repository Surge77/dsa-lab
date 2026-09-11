"""
Grade a drill attempt against the same checks the reference code faces.

Sorts and searches go through Utils/contracts.py — the identical contract the
test suite uses, so there is no weaker standard for your own work. Data
structures are graded by running the topic's real pytest file against your
module, substituted in place of the reference via the DSA_DRILL_SUBSTITUTE hook
in conftest.py.
"""

import importlib.util
import os
import pathlib
import subprocess
import sys
from dataclasses import dataclass, field

import curriculum
from Utils.contracts import GENERAL, SORT_DOMAINS, check_search, check_sort

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "Tests"
SUBSTITUTE_ENV = "DSA_DRILL_SUBSTITUTE"

# Searches whose signature is not (array, target) and so cannot use the shared
# search contract, with the reason shown to the user.
NON_CONTRACT_SEARCHES = {
    "ubiquitous_binary_search": "takes a predicate, not an array — compare against the reference",
    "rotated_binary_search": "needs rotated input — run Tests/test_searching.py",
    "sublist_search": "takes a pattern, not a scalar target",
    "astar": "takes a tree and two callables",
}


@dataclass
class Grade:
    """The outcome of grading one attempt."""

    slug: str
    graded: bool
    passed: bool
    failures: list[str] = field(default_factory=list)
    note: str | None = None

    def render(self) -> str:
        if not self.graded:
            return f"  not automatically graded: {self.note}"
        if self.passed:
            return "  PASS — every check satisfied"
        lines = [f"  FAIL — {len(self.failures)} problem(s):"]
        lines += [f"    - {failure}" for failure in self.failures[:12]]
        if len(self.failures) > 12:
            lines.append(f"    ... and {len(self.failures) - 12} more")
        return "\n".join(lines)


def load_attempt(path: pathlib.Path, module_name: str):
    """
    Import an attempt file as a module, without putting it on sys.path.

    Uses a unique module name so a second grading in the same process does not
    get a cached copy of the first attempt.
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def entry_of(module, topic: curriculum.Topic):
    """Resolve a topic's dotted entry name against a module."""
    target = module
    for attribute in topic.entry.split("."):
        target = getattr(target, attribute)
    return target


def test_file_for(topic: curriculum.Topic) -> pathlib.Path | None:
    """The per-topic pytest file, by convention Tests/test_<slug>.py."""
    candidate = TESTS_DIR / f"test_{topic.slug}.py"
    return candidate if candidate.exists() else None


def grade_sort(topic: curriculum.Topic, function) -> Grade:
    """Run the shared sort contract for this topic's input domain."""
    domain = SORT_DOMAINS.get(topic.slug, GENERAL)
    failures = check_sort(function, domain=domain, check_stability=topic.stable is True)
    return Grade(topic.slug, graded=True, passed=not failures, failures=failures)


def grade_search(topic: curriculum.Topic, function) -> Grade:
    """Run the shared search contract, where the signature allows."""
    if topic.slug in NON_CONTRACT_SEARCHES:
        return Grade(
            topic.slug, graded=False, passed=False, note=NON_CONTRACT_SEARCHES[topic.slug]
        )
    sorted_input = "linear" not in topic.family.lower()
    failures = check_search(function, sorted_input=sorted_input)
    return Grade(topic.slug, graded=True, passed=not failures, failures=failures)


def grade_structure(topic: curriculum.Topic, attempt_file: pathlib.Path) -> Grade:
    """
    Run the topic's real test file against the attempt.

    The substitution happens in a subprocess so a half-working attempt cannot
    corrupt the grading process's own imports — and so an infinite loop in your
    code kills a child rather than the CLI.
    """
    test_file = test_file_for(topic)
    if test_file is None:
        return Grade(
            topic.slug,
            graded=False,
            passed=False,
            note=f"no Tests/test_{topic.slug}.py to run — compare against {topic.path}",
        )

    env = dict(os.environ)
    env[SUBSTITUTE_ENV] = f"{topic.module}={attempt_file}"

    completed = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if completed.returncode == 0:
        return Grade(topic.slug, graded=True, passed=True)

    failures = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("FAILED") or line.startswith("ERROR")
    ]
    if not failures:
        tail = (completed.stdout + completed.stderr).strip().splitlines()[-6:]
        failures = [line.strip() for line in tail if line.strip()]
    return Grade(topic.slug, graded=True, passed=False, failures=failures)


def grade(topic: curriculum.Topic, attempt_file: pathlib.Path) -> Grade:
    """Grade one attempt, dispatching on what kind of thing the topic is."""
    if topic.is_sort or topic.is_search:
        try:
            module = load_attempt(attempt_file, f"_drill_{topic.slug}")
            function = entry_of(module, topic)
        except NotImplementedError:
            return Grade(topic.slug, graded=True, passed=False,
                         failures=["module raised NotImplementedError while importing"])
        except AttributeError:
            return Grade(topic.slug, graded=True, passed=False,
                         failures=[f"no '{topic.entry}' defined in your attempt"])
        except Exception as exc:
            return Grade(topic.slug, graded=True, passed=False,
                         failures=[f"attempt failed to import: {type(exc).__name__}: {exc}"])

        return grade_sort(topic, function) if topic.is_sort else grade_search(topic, function)

    return grade_structure(topic, attempt_file)


def diff_against_reference(topic: curriculum.Topic, attempt_file: pathlib.Path) -> str:
    """
    A unified diff of your attempt against the reference.

    Shown only after grading, because seeing it earlier removes the retrieval
    effort that makes the exercise work at all.
    """
    import difflib

    reference_path = REPO_ROOT / topic.path
    reference = reference_path.read_text(encoding="utf-8").splitlines()
    # Strip the generated teaching header so the diff is about code, not comments.
    if reference and reference[0].startswith("# --- curriculum:"):
        end = next((i for i, line in enumerate(reference) if line.startswith("# --- end")), 0)
        reference = reference[end + 1:]

    attempt = attempt_file.read_text(encoding="utf-8").splitlines()
    diff = difflib.unified_diff(
        attempt, reference, fromfile="your attempt", tofile=topic.path, lineterm="", n=2
    )
    return "\n".join(diff) or "  (identical)"
