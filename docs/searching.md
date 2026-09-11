# Searching — the one shape worth memorising, and the 14 variations

Per-algorithm detail lives in the generated header at the top of each source
file and in [INDEX.md](../INDEX.md). This page is the decision layer.

---

## The decision, in order

1. **Is the data sorted and randomly accessible?** No → linear search. There is
   no alternative, and sorting first to enable binary search costs O(n log n)
   for a single lookup.
2. **Is the length known?** No → exponential search. It is O(log i) in the
   answer's *index*, independent of total length.
3. **Is the array rotated?** → rotated binary search. At least one half of any
   window is still sorted.
4. **Are the keys uniformly distributed numbers?** → interpolation search,
   O(log log n). But O(n) on skewed input, so know your data.
5. **Is backward movement expensive?** → jump search, O(√n) with forward jumps
   only.
6. **Is the question "minimum X such that condition holds"?** → the predicate
   form. See below. This is the one that matters.
7. **Otherwise** → plain binary search.

---

## The general form (learn this one)

Most binary-search interview problems are not about arrays at all. They are about
finding the boundary of a **monotone predicate**:

```
predicate:  false  false  false  TRUE  TRUE  TRUE
                               ^
                          find this
```

```python
def first_true(predicate, lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

`Searching/advanced/ubiquitous_binary_search.py`.

Three things to get right:

- **Monotonicity is a precondition, not a detail.** If the predicate flips back
  and forth, the method is invalid — not merely slow. Verify it.
- **Use the half-open form** shown above: `while lo < hi`, then `hi = mid` or
  `lo = mid + 1`. Mixing in `hi = mid - 1` from the closed-interval form gives
  an infinite loop or an off-by-one.
- **`hi` starts at a value where the predicate is known true** — an upper bound
  on the *answer*, not the array length.

Once you see it, this solves: Koko Eating Bananas (LC 875), Capacity to Ship
Packages (LC 1011), Split Array Largest Sum (LC 410), Minimum Days to Make m
Bouquets (LC 1482), Median of Two Sorted Arrays (LC 4). They are the same
problem wearing different clothes.

---

## Binary search boundary arithmetic

The idea is never the hard part. These are:

```python
mid = left + (right - left) // 2   # not (left + right) // 2
```

Irrelevant in Python (arbitrary-precision ints) but it is the canonical answer
and the overflow reason is worth knowing.

**Two consistent forms; never mix them:**

| | Closed interval | Half-open |
|---|---|---|
| loop | `while left <= right` | `while left < right` |
| discard left | `left = mid + 1` | `left = mid + 1` |
| discard right | `right = mid - 1` | `right = mid` |
| answer | returned inside the loop | `left` after the loop |

Taking one line from each column is the most common binary-search bug in
existence.

**Plain binary search returns *some* matching index, not the first.** Leftmost
and rightmost bounds need the variant that records a hit and keeps narrowing.

---

## Why ternary search is slower than binary search

A tempting intuition says splitting into three parts beats splitting into two.
Count comparisons rather than iterations:

- binary: log₂(n) iterations × 1 comparison = **log₂(n)**
- ternary: log₃(n) iterations × 2 comparisons = 2·log₃(n) ≈ **1.26·log₂(n)**

So ternary search does about 26% *more* work. Its legitimate use is not array
lookup at all — it is finding the extremum of a **unimodal function**, where
binary search does not apply.

---

## The linear family

Four variants, and the honest summary is that none of them beats O(n):

- **linear search** — the baseline. Requires nothing of the data.
- **recursive** — the same, with O(n) stack instead of O(1). Useful only to show
  how a loop maps to a recurrence; `RecursionError` around n=1000 in CPython.
- **bidirectional** — scans from both ends. Halves the *iteration* count but
  doubles comparisons per iteration, so the comparison count is unchanged. Also
  may return the rightmost of several matches.
- **sentinel** — plants the target in the last slot so the loop needs no bounds
  check: one comparison per step instead of two. Real win in C, lost in the noise
  in Python. It **mutates its input** and must restore it on every path,
  including the not-found path.

---

## Complexity at a glance

| Algorithm | Average | Requires |
|---|---|---|
| linear | O(n) | nothing |
| sentinel | O(n), half the comparisons | writable array |
| binary | O(log n) | sorted + random access |
| exponential | O(log i) | sorted, unbounded length OK |
| fibonacci | O(log n) | sorted; no division needed |
| interpolation | O(log log n) | sorted **and** uniformly distributed |
| jump | O(√n) | sorted; forward-only movement |
| ternary | ~1.26·log₂(n) | sorted, or unimodal function |
| sublist | O(n·m) | nothing |
| A* | O(b^d) worst | a heuristic |

---

## A* in one paragraph

Best-first search ordered by `f = g + h`, where `g` is the cost already paid and
`h` estimates the cost remaining. Pure `g` is Dijkstra; pure `h` is greedy
best-first; A* is the combination. If `h` never overestimates (**admissible**),
the first time the goal is popped its path is optimal. An inadmissible heuristic
still returns an answer — just not the best one, silently. Setting `h = 0`
reduces it to Dijkstra, which is the standard sanity check when a heuristic is
under suspicion.

The implementation detail that bites: heap entries must carry a tiebreaker
counter, or two equal f-scores force Python to compare the node objects and raise
`TypeError`.

---

## A note on how these used to behave

Nine of these modules executed their own test assertions **at import time**.
Importing `binary_search` printed `All tests passed.` as a side effect. That is
why `Tests/test_searching.py` now asserts that importing any search module
produces no output at all.

`sublist_search` also returned a bare `bool`, so it could tell you *whether* a
pattern was present but never *where* — and it compared with `main_list[i:i+m]`,
allocating a fresh list per attempt while claiming O(1) space. It now returns an
index, with `contains_sublist` and `all_occurrences` alongside it.

---

## Interview mapping

| Problem | Technique |
|---|---|
| Binary Search (LC 704) | the basic form |
| First Bad Version (LC 278) | predicate form |
| Search in Rotated Sorted Array (LC 33) | identify the sorted half |
| …with duplicates (LC 81) | duplicates break it; O(n) worst case |
| Find Peak Element (LC 162) | binary search on a unimodal array |
| Koko Eating Bananas (LC 875) | binary search on the answer |
| Median of Two Sorted Arrays (LC 4) | binary search on the partition |
| Search in Unknown-Size Array (LC 702) | exponential search |
| Implement strStr() (LC 28) | sublist search, then KMP |

Drill any of it: `python drill.py --topic searching`
