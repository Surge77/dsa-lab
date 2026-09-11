# Sorting — how to choose, and what the 27 algorithms are each for

Per-algorithm detail lives in the generated header at the top of each source
file and in [INDEX.md](../INDEX.md). This page is the decision layer: which one,
and why.

---

## The decision, in order

1. **Is the data integers in a small range?** → counting / radix / pigeonhole
   sort. You can beat the O(n log n) comparison bound by not comparing.
2. **Do you need stability?** → merge sort or tim sort. Not quick sort.
3. **Is memory tight?** → heap sort (O(1) space, guaranteed O(n log n)) or
   quick sort (O(log n) stack).
4. **Is the data already nearly ordered?** → insertion sort for small n,
   tim sort otherwise. Both are adaptive.
5. **Do you need a hard worst-case guarantee?** → heap sort or intro sort.
   Quick sort's worst case is O(n²).
6. **Otherwise** → intro sort (what `std::sort` does) or tim sort (what
   `list.sort` does). Both are hybrids, and that is not a coincidence.

Every production sort is a hybrid. That is the most useful single fact here.

---

## The comparison lower bound, and how to dodge it

Any sort that learns about order only through pairwise comparisons needs
Ω(n log n) comparisons in the worst case. The argument: there are n! possible
orderings, each comparison yields one bit, and log₂(n!) ≈ n log n.

So the only way to go faster is to stop comparing. The three non-comparison
sorts each buy speed with a different assumption:

| Sort | Assumption it buys with | Cost |
|---|---|---|
| counting | keys are integers in a range k | O(k) memory |
| radix | keys are fixed-width | d passes |
| bucket | keys are **uniformly distributed** | O(n²) if they are not |

Note that counting and radix depend on the key **range**, while bucket sort
depends on the key **distribution**. That distinction is the usual interview
follow-up, and it is why bucket sort has an O(n²) worst case and counting sort
does not.

---

## Properties, and why each matters

**Stable** — equal elements keep their relative order. Matters whenever you sort
by one field after another ("sort by date, then by name" only works if the
second sort is stable). It is also what makes radix sort possible: each digit
pass must be stable or the previous passes' work is destroyed.

**In-place** — O(1) or O(log n) extra space. Matters for large data and embedded
targets.

**Adaptive** — faster on partially sorted input. Real data is usually partially
sorted, which is why timsort beats textbook merge sort in practice.

These three are in tension. Merge sort is stable but not in-place; quick sort is
in-place but not stable; heap sort is in-place with a guaranteed bound but is
neither stable nor adaptive and has poor cache behaviour. There is no free lunch,
and naming the trade-off is usually the answer an interviewer wants.

---

## Families in this lab

### simple — O(n²), and each teaches one idea

- **bubble** — the baseline. Its swap count equals the input's inversion count.
- **insertion** — O(n) on sorted input, tiny constants. Every hybrid falls back
  to it below ~16 elements.
- **selection** — exactly n-1 swaps regardless of input. The one to use when
  writes are far more expensive than reads (EEPROM, flash).

### efficient — the three you must know cold

- **merge** — stable, O(n log n) always, O(n) space. The only choice for linked
  lists and external data.
- **quick** — in-place, best constants, O(n²) worst case. The default for arrays.
- **heap** — O(1) space, guaranteed O(n log n), poor cache locality.

### advanced — hybrids and gap sequences

- **shell** — insertion sort over shrinking gaps. The gap sequence *is* the
  algorithm.
- **tim** — runs + merges. CPython's `list.sort`.
- **intro** — quick sort with an insertion-sort floor and a heap-sort ceiling.
  C++'s `std::sort`.

### non-comparison — beating n log n

counting, radix, bucket, pigeonhole. See the table above.

### network — fixed comparison schedules for parallel hardware

- **odd-even** / **brick** (two names, one algorithm) — alternating independent
  compare-exchange phases. O(n) depth with n processors.
- **bitonic** — O(log² n) depth, data-independent, bakeable into silicon. Only
  defined for power-of-two lengths; this implementation pads.

### specialized — each illustrates exactly one point

cocktail shaker (direction matters), comb (gaps fix bubble's turtles), gnome
(one loop suffices), pancake (the allowed *operation* shapes the algorithm),
stooge (a recurrence can be worse than the obvious loop), bogosort (expected vs
worst case), sleep sort (producing sorted output is not proof of correctness).

### tree-based

- **tree sort** — insert into a BST, read inorder. Leaves a queryable structure
  behind.
- **cartesian tree sort** — adaptive; cost is O(n log k) for k existing runs.

### external — data that does not fit in memory

- **external merge sort** — sort chunks, then k-way merge. Peak memory
  independent of total size.
- **polyphase** — the tape-era variant, here in its balanced 3-tape form.

---

## Measure it yourself

```bash
python -m Utils.complexity                     # headline comparison
python -m Utils.complexity --all --max-n 2000  # everything runnable
```

Ratios between consecutive doublings: ~2 linear, ~2.1–2.3 n log n, ~4 quadratic.
Reading "O(N^2)" in a docstring does not convince; watching the time go ×4.2
three times in a row does.

See the steps, not just the result:

```python
from Utils.trace import trace_sort, compare_sorts
from Sorting.simple.bubble_sort import bubble_sort

print(trace_sort(bubble_sort, [5, 1, 4, 2, 8]))
```

`compare_sorts` prints comparisons and in-place writes side by side, which is the
fastest way to see why selection sort exists: it makes far fewer writes than
bubble sort for the same number of comparisons.

---

## Four real bugs that were in this directory

Worth knowing because each is a realistic mistake, not a typo:

1. **bitonic sort** returned silently wrong output for any length that was not a
   power of two. The network is only defined for powers of two.
2. **cartesian tree sort** called `sorted()` on the result of its inorder
   traversal — and since an inorder walk of a Cartesian tree returns the
   *original* array, the whole function was theatre around the builtin.
3. **sleep sort** did the same thing, ending with `return sorted(result)`.
4. **polyphase sort** merged each tape as if it were one sorted stream, when a
   tape holds a *sequence* of runs. Output was unsorted; empty input looped
   forever.

Two of those produced correct-looking output, which is why
`Tests/test_sorting.py` now asserts that neither function references `sorted`,
and why it checks the Cartesian tree's defining property directly.

---

## Interview mapping

| Problem | Technique |
|---|---|
| Kth Largest (LC 215) | quickselect — quick sort's partition |
| Sort Colors (LC 75) | three-way partition |
| Merge Intervals (LC 56) | sort, then one pass |
| Top K Frequent (LC 347) | bucket by frequency |
| Count of Smaller After Self (LC 315) | merge sort, counting during the merge |
| Maximum Gap (LC 164) | radix or bucket sort |
| Sort List (LC 148) | merge sort on a linked list |
| Pancake Sorting (LC 969) | prefix reversal |

Drill any of it: `python drill.py --topic sorting`
