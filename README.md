# dsa-lab

Data structures and algorithms implemented from scratch in Python — **plus a
spaced-repetition drill system so the code is something you practise, not
something you reread.**

63 concepts. 27 sorting algorithms, 15 searching algorithms, 21 data structures.
No built-in containers used in the implementations.

```bash
python drill.py                 # what should I revise right now?
```

---

## Revising, by how much time you have

| You have | Do this |
|---|---|
| 30 seconds — "what do I not know?" | `python drill.py --list --due-only` |
| 5 minutes — refresh one thing | `python drill.py --topic heaps` and read the invariant |
| 20 minutes — actually learn | `python drill.py`, implement, `--check`, read the pitfalls |
| An hour | three drills from three different families |
| "which sort do I use?" | [INDEX.md](INDEX.md), rightmost column |
| "how does X work?" | `head -60 <the file>` — the teaching header is at the top |
| interview next week | `python drill.py --stats`, then the `INTERVIEW` lines in your weak files |
| "prove the Big-O" | `python -m Utils.complexity` |
| "show me it working" | `python -c "from Utils.trace import trace_sort; ..."` |

Full guide: **[docs/how_to_revise.md](docs/how_to_revise.md)**

---

## The drill loop

```
$ python drill.py --topic quick_sort

  Quick sort   [Sorting / efficient]   slug: quick_sort

  INVARIANT — the thing to hold on to
    After partition(lo, hi) returns p: arr[p] is final,
    arr[lo:p] <= arr[p] <= arr[p+1:hi+1].

  TARGET COMPLEXITY   O(n log n) / O(n log n) / O(n^2)   space O(log n)
  PROPERTIES          stable no  in-place yes  adaptive no

  YOUR FILE   drills/attempts/quick_sort.py
              (fresh stub: every body raises NotImplementedError)

  Fill in every body, then:
      python drill.py --check quick_sort
```

You get the invariant and the target complexity. You do **not** get the code, the
pitfalls, or the interview problems — those are the reward for having tried.

Grading uses `Utils/contracts.py`, the same contract the reference
implementations face in CI, so there is no softer standard for your own work.
Pass and the interval expands (1 → 3 → 7 → 16 → 35 → 90 days); fail and it
resets to tomorrow.

---

## Layout

```
Linear/          arrays, stack, queue, circular queue, deque, linked lists
Hash/            hash map, hash set
Non_Linear/      trees, BST, traversals, heaps, trie, union-find, 4 graph kinds
Sorting/         27 algorithms in 8 families
Searching/       15 algorithms in 4 families

curriculum/      the single source of truth — one Topic record per concept
drills/          stub generation, grading, spaced repetition
Utils/           trace.py, complexity.py, contracts.py, sync.py
Tests/           pytest suite
docs/            longer-form notes
INDEX.md         generated: every concept, one row each
drill.py         the CLI
```

### The curriculum is the source of truth

Each concept has one `Topic` record holding its mental model, invariant,
complexity, when-to-use, when-not-to-use, pitfalls, cross-references and
interview problems. From that single record the repo generates:

- **INDEX.md** — the navigable table
- **the teaching header** at the top of each implementation file
- **the drill prompt** you see in the CLI
- **the blank-slate stub** you implement into

```bash
python -m Utils.sync          # regenerate
python -m Utils.sync --check  # fail if stale (CI does this)
```

Nothing can drift, because nothing is written twice. `Tests/test_curriculum.py`
fails if an implementation file has no curriculum entry, if a cross-reference
dangles, or if INDEX.md is out of date.

---

## Building intuition

**Watch it work** — instruments the data, not the function, so it works on any
sort here without modification:

```python
from Utils.trace import trace_sort, compare_sorts
from Sorting.simple.bubble_sort import bubble_sort

print(trace_sort(bubble_sort, [5, 1, 4, 2, 8]))
# bubble_sort  n=5  9 comparisons  8 writes  -> sorted
#   start [5, 1, 4, 2, 8]
#      1  [1, 1, 4, 2, 8]   write arr[0] = 1
#      2  [1, 5, 4, 2, 8]   write arr[1] = 5
#      ...
```

**Prove the complexity** rather than trusting the docstring:

```bash
$ python -m Utils.complexity
bubble_sort  (claims avg O(n^2))
    n=250          1.46 ms
    n=500          6.57 ms   x4.5 ~quadratic
    n=1000        27.60 ms   x4.2 ~quadratic
    n=2000       116.18 ms   x4.2 ~quadratic

merge_sort  (claims avg O(n log n))
    n=250          0.22 ms
    n=500          0.46 ms   x2.1 ~n log n
    n=1000         1.01 ms   x2.2 ~n log n
    n=2000         2.18 ms   x2.2 ~n log n
```

---

## Tests

```bash
python -m pytest              # everything
python -m pytest -m "not slow"   # skip sleep sort and bogosort
python -m pytest --cov        # coverage
```

Sorts and searches are covered by two parametrized suites driven off the
curriculum, so adding an algorithm adds its tests automatically and a gap cannot
hide behind a bespoke test file.

---

## Setup

No dependencies for the library itself.

```bash
git clone <this repo> && cd dsa-lab
python -m pip install -e ".[dev]"   # pytest, pytest-cov, ruff
python drill.py
```

Python 3.10+. `conftest.py` puts the repo root on `sys.path`, so `python -m
pytest` and `python drill.py` both work in a bare checkout with no install step.

See also [docs/setup_guide.md](docs/setup_guide.md).

---

## Reading order, if the repo is new to you

1. [INDEX.md](INDEX.md) — see the whole surface
2. [docs/how_to_revise.md](docs/how_to_revise.md) — how to use it
3. [docs/sorting.md](docs/sorting.md) and [docs/searching.md](docs/searching.md)
   — the decision layers: which algorithm, and why
4. Any implementation file — the teaching header at the top is the summary

---

## License

See [LICENSE](LICENSE).
