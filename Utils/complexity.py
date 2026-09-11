"""
Prove the Big-O empirically instead of believing the docstring.

Times an algorithm at doubling input sizes and reports the ratio between
consecutive timings. The ratio is the diagnostic:

    ~2.0  -> linear                 ~2.1-2.3 -> n log n
    ~4.0  -> quadratic              ~1.0     -> constant / logarithmic

Run it directly:

    python -m Utils.complexity                      # the headline comparison
    python -m Utils.complexity bubble_sort merge_sort quick_sort
    python -m Utils.complexity --all --max-n 2000

Theory, then measurement, then belief — in that order. It doubles as a
regression guard: if a "fast" sort starts showing a 4.0 ratio, something
quadratic crept in.
"""

import argparse
import importlib
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import curriculum

DEFAULT_SIZES = (250, 500, 1000, 2000)
QUADRATIC_SAFE_MAX_N = 2000
REPEATS = 3

# Sorts that cannot take the generic random-integer workload, with the reason.
WORKLOAD_EXCLUSIONS = {
    "bogosort": "factorial time — caps out around n=8",
    "sleep_sort": "runtime scales with value magnitude, not n",
    "external_merge_sort": "operates on files, not lists",
    "polyphase_sort": "operates on files, not lists",
}

# Algorithms whose cost is superlinear enough that large n is impractical.
SLOW_SLUGS = {
    "bubble_sort", "insertion_sort", "selection_sort", "gnome_sort",
    "stooge_sort", "pancake_sort", "odd_even_sort", "brick_sort",
    "cocktail_shaker_sort", "bucket_sort",
}

HEADLINE = ("bubble_sort", "insertion_sort", "merge_sort", "quick_sort", "heap_sort", "tim_sort")


@dataclass
class Measurement:
    n: int
    seconds: float
    ratio: float | None

    def ratio_label(self) -> str:
        if self.ratio is None:
            return ""
        if self.ratio < 1.4:
            shape = "~constant/log"
        elif self.ratio < 2.6:
            shape = "~n log n" if self.ratio > 2.05 else "~linear"
        elif self.ratio < 3.4:
            shape = "~n^1.5"
        elif self.ratio < 5.0:
            shape = "~quadratic"
        else:
            shape = "worse than quadratic"
        return f"x{self.ratio:.1f} {shape}"


def pseudo_random_ints(n: int, seed: int = 12345, bound: int = 10_000) -> list[int]:
    """
    A deterministic pseudo-random list, built without importing `random`.

    Determinism matters: comparing timings across runs is only meaningful if
    every algorithm sees byte-identical input.
    """
    state = seed
    out = []
    for _ in range(n):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        out.append(state % bound)
    return out


def time_once(fn: Callable, values: Sequence[int]) -> float:
    """Wall-clock seconds for one run over a fresh copy of `values`."""
    data = list(values)
    start = time.perf_counter()
    fn(data)
    return time.perf_counter() - start


def measure(fn: Callable, sizes: Sequence[int] = DEFAULT_SIZES) -> list[Measurement]:
    """
    Time `fn` at each size, taking the best of REPEATS runs.

    Best-of rather than mean, because the noise here is additive (GC, OS
    scheduling) and the minimum is the closest estimate of the true cost.
    """
    results: list[Measurement] = []
    previous: float | None = None
    for n in sizes:
        values = pseudo_random_ints(n)
        best = min(time_once(fn, values) for _ in range(REPEATS))
        ratio = (best / previous) if previous and previous > 0 else None
        results.append(Measurement(n=n, seconds=best, ratio=ratio))
        previous = best
    return results


def resolve(slug: str) -> Callable:
    """Import a topic's entry point from its curriculum record."""
    topic = curriculum.get(slug)
    module = importlib.import_module(topic.module)
    return getattr(module, topic.entry)


def runnable_sort_slugs(include_slow: bool = True) -> list[str]:
    """Sort slugs that the generic random-integer workload can actually drive."""
    slugs = []
    for topic in curriculum.ALL_TOPICS:
        if not topic.is_sort or topic.slug in WORKLOAD_EXCLUSIONS:
            continue
        if not include_slow and topic.slug in SLOW_SLUGS:
            continue
        slugs.append(topic.slug)
    return slugs


def report(slugs: Sequence[str], max_n: int = QUADRATIC_SAFE_MAX_N) -> str:
    """Render a timing table for each slug, one block per algorithm."""
    lines: list[str] = []
    for slug in slugs:
        if slug in WORKLOAD_EXCLUSIONS:
            lines.append(f"{slug}: skipped — {WORKLOAD_EXCLUSIONS[slug]}\n")
            continue

        cap = min(max_n, 500) if slug in SLOW_SLUGS and max_n > 2000 else max_n
        sizes = [n for n in DEFAULT_SIZES if n <= cap] or [DEFAULT_SIZES[0]]

        try:
            fn = resolve(slug)
            rows = measure(fn, sizes)
        except Exception as exc:
            lines.append(f"{slug}: FAILED — {type(exc).__name__}: {exc}\n")
            continue

        claimed = curriculum.get(slug).complexity
        lines.append(f"{slug}  (claims avg {claimed.average})")
        for row in rows:
            lines.append(f"    n={row.n:<6} {row.seconds * 1000:9.2f} ms   {row.ratio_label()}")
        lines.append("")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m Utils.complexity",
        description="Measure empirical growth rates and compare them to the claimed complexity.",
    )
    parser.add_argument("slugs", nargs="*", help="topic slugs to time (default: a headline set)")
    parser.add_argument("--all", action="store_true", help="time every runnable sort")
    parser.add_argument("--fast-only", action="store_true", help="skip the quadratic sorts")
    parser.add_argument("--max-n", type=int, default=QUADRATIC_SAFE_MAX_N, help="largest input size")
    args = parser.parse_args(argv)

    if args.all or args.fast_only:
        slugs = runnable_sort_slugs(include_slow=not args.fast_only)
    elif args.slugs:
        slugs = list(args.slugs)
    else:
        slugs = list(HEADLINE)

    unknown = [s for s in slugs if s not in curriculum.BY_SLUG]
    if unknown:
        parser.error(f"unknown topic slug(s): {', '.join(unknown)}")

    print(report(slugs, max_n=args.max_n))
    print("Ratio between consecutive doublings: ~2 linear, ~2.1-2.3 n log n, ~4 quadratic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
