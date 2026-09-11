"""
Watch an algorithm work, without modifying it.

The trick is to instrument the *data* rather than the function. `Probe` hands out
`TracedValue` wrappers that count every comparison they take part in, and a
`TracedList` that counts and snapshots every write. Any sort in this repo can
then be traced as-is:

    from Utils.trace import trace_sort
    from Sorting.simple.bubble_sort import bubble_sort

    print(trace_sort(bubble_sort, [5, 1, 4, 2, 8]))

Seeing that one pass spent four comparisons to accomplish three swaps is what
makes O(n^2) mean something. Reading the string "O(N^2)" in a docstring does not.
"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

MAX_RENDERED_STEPS = 40
MAX_RENDERED_WIDTH = 12


@dataclass
class Probe:
    """Shared counters for one traced run."""

    comparisons: int = 0
    writes: int = 0
    snapshots: list[list[Any]] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    record_snapshots: bool = True

    def record(self, state: Sequence[Any], label: str) -> None:
        if not self.record_snapshots:
            return
        self.snapshots.append([unwrap(v) for v in state])
        self.labels.append(label)


class TracedValue:
    """
    A value that reports every comparison it participates in.

    Only the comparison operators are instrumented; arithmetic is passed through
    untouched so algorithms that compute on values (radix, counting, bucket)
    still work.
    """

    __slots__ = ("value", "probe")

    def __init__(self, value: Any, probe: Probe) -> None:
        self.value = value
        self.probe = probe

    def _compare(self, other: Any) -> Any:
        self.probe.comparisons += 1
        return unwrap(other)

    def __lt__(self, other: Any) -> bool:
        return self.value < self._compare(other)

    def __le__(self, other: Any) -> bool:
        return self.value <= self._compare(other)

    def __gt__(self, other: Any) -> bool:
        return self.value > self._compare(other)

    def __ge__(self, other: Any) -> bool:
        return self.value >= self._compare(other)

    def __eq__(self, other: Any) -> bool:
        return self.value == self._compare(other)

    def __ne__(self, other: Any) -> bool:
        return self.value != self._compare(other)

    # Arithmetic and conversion are deliberately NOT counted: they are not
    # comparisons, and non-comparison sorts need them to behave normally.
    def __add__(self, other: Any) -> Any:
        return self.value + unwrap(other)

    def __sub__(self, other: Any) -> Any:
        return self.value - unwrap(other)

    def __mul__(self, other: Any) -> Any:
        return self.value * unwrap(other)

    def __floordiv__(self, other: Any) -> Any:
        return self.value // unwrap(other)

    def __truediv__(self, other: Any) -> Any:
        return self.value / unwrap(other)

    def __mod__(self, other: Any) -> Any:
        return self.value % unwrap(other)

    def __radd__(self, other: Any) -> Any:
        return unwrap(other) + self.value

    def __index__(self) -> int:
        return int(self.value)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return repr(self.value)


class TracedList(list):
    """A list that counts and snapshots every element write."""

    def __init__(self, values: Sequence[Any], probe: Probe) -> None:
        super().__init__(values)
        self.probe = probe

    def __setitem__(self, index, value) -> None:  # type: ignore[override]
        super().__setitem__(index, value)
        self.probe.writes += 1
        if isinstance(index, int):
            self.probe.record(self, f"write arr[{index}] = {unwrap(value)}")
        else:
            self.probe.record(self, f"write slice {index}")


def unwrap(value: Any) -> Any:
    """Strip a TracedValue back to the plain value it wraps."""
    return value.value if isinstance(value, TracedValue) else value


@dataclass
class Trace:
    """The result of one instrumented run."""

    name: str
    start: list[Any]
    result: list[Any]
    comparisons: int
    writes: int
    snapshots: list[list[Any]]
    labels: list[str]

    @property
    def is_sorted(self) -> bool:
        return self.result == sorted(self.start)

    def summary(self) -> str:
        verdict = "sorted" if self.is_sorted else "NOT SORTED"
        return (
            f"{self.name}  n={len(self.start)}  "
            f"{self.comparisons} comparisons  {self.writes} writes  -> {verdict}"
        )

    def __str__(self) -> str:
        lines = [self.summary(), f"  start {self.start}"]
        shown = self.snapshots[:MAX_RENDERED_STEPS]
        for i, (state, label) in enumerate(zip(shown, self.labels, strict=False), start=1):
            lines.append(f"  {i:4}  {state}   {label}")
        hidden = len(self.snapshots) - len(shown)
        if hidden > 0:
            lines.append(f"  ... {hidden} further writes not shown")
        lines.append(f"  final {self.result}")
        return "\n".join(lines)


def trace_sort(
    sort_fn: Callable,
    values: Sequence[Any],
    name: str | None = None,
    snapshots: bool = True,
) -> Trace:
    """
    Run `sort_fn` over `values` and report what it actually did.

    Works on both in-place sorts and sorts that return a new list: whichever the
    function produces, the final ordering is read back correctly.

    `snapshots=False` keeps the counters but skips recording array states, which
    matters for large inputs where the snapshot list would dominate memory.

    Note that `writes` counts writes through the traced list only. A sort that
    builds new lists instead of writing in place (merge sort, counting sort)
    therefore reports 0 writes — which is itself the useful signal.
    """
    probe = Probe(record_snapshots=snapshots)
    wrapped = [TracedValue(v, probe) for v in values]
    arr = TracedList(wrapped, probe)

    returned = sort_fn(arr)
    final = returned if isinstance(returned, list) else arr

    return Trace(
        name=name or getattr(sort_fn, "__name__", "sort"),
        start=list(values),
        result=[unwrap(v) for v in final],
        comparisons=probe.comparisons,
        writes=probe.writes,
        snapshots=probe.snapshots,
        labels=probe.labels,
    )


def compare_sorts(
    sort_fns: Sequence[Callable],
    values: Sequence[Any],
) -> str:
    """
    One-line-per-algorithm comparison of comparison and write counts.

    This is the cheapest way to see *why* selection sort is chosen for
    write-expensive media: it does n-1 writes where bubble sort does hundreds.
    """
    rows = []
    for fn in sort_fns:
        try:
            trace = trace_sort(fn, values, snapshots=False)
            rows.append((trace.name, trace.comparisons, trace.writes, trace.is_sorted))
        except Exception as exc:  # a domain-restricted sort may refuse this input
            rows.append((getattr(fn, "__name__", "?"), -1, -1, f"{type(exc).__name__}"))

    width = max(len(str(r[0])) for r in rows)
    lines = [f"n={len(values)}  input={list(values)[:MAX_RENDERED_WIDTH]}", ""]
    lines.append(f"{'algorithm':{width}}  {'compares':>9}  {'in-place writes':>15}  result")
    for name, comparisons, writes, ok in rows:
        if comparisons < 0:
            lines.append(f"{name:{width}}  {'—':>9}  {'—':>15}  refused ({ok})")
        else:
            verdict = "ok" if ok is True else "WRONG"
            lines.append(f"{name:{width}}  {comparisons:9}  {writes:15}  {verdict}")
    return "\n".join(lines)
