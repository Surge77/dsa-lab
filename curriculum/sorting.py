"""Curriculum entries for every sorting algorithm in the lab."""

from curriculum.schema import Complexity, Topic

C = Complexity

SORTING_TOPICS = [
    # ---------------------------------------------------------------- simple
    Topic(
        slug="bubble_sort",
        name="Bubble sort",
        family="Sorting / simple",
        module="Sorting.simple.bubble_sort",
        entry="bubble_sort",
        mental_model=(
            "Sweep left to right swapping any out-of-order neighbours. Each full "
            "sweep drags the largest remaining value to the end like a bubble "
            "rising, so after pass i the last i slots are final. Stop early if a "
            "sweep makes no swaps."
        ),
        invariant="After pass i, arr[n-i:] holds the i largest values, sorted.",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=True,
        in_place=True,
        adaptive=True,
        use_when="Teaching, or n is tiny and you want the shortest correct code.",
        avoid_when="Always, in production. Insertion sort dominates it at every size.",
        pitfalls=[
            "Inner loop bound must be n-i-1; using n-1 reads past the end or "
            "wastes comparisons over the already-final tail.",
            "Without the swapped flag it is O(n^2) even on sorted input, which "
            "loses the only property that makes it interesting.",
            "Comparing arr[j] > arr[j+1] (not >=) is what keeps it stable; "
            "flipping to >= silently breaks stability.",
        ],
        see_also=["insertion_sort", "cocktail_shaker_sort", "odd_even_sort"],
        interview=[
            "Rarely asked directly — asked as 'why is this slow?'",
            "Counting inversions (bubble's swap count = inversion count)",
        ],
    ),
    Topic(
        slug="insertion_sort",
        name="Insertion sort",
        family="Sorting / simple",
        module="Sorting.simple.insertion_sort",
        entry="insertion_sort",
        mental_model=(
            "How you sort a dealt hand of cards. Keep a sorted prefix; take the "
            "next element and slide it left past everything larger until it "
            "lands. The shifting, not swapping, is what makes it fast in "
            "practice."
        ),
        invariant="Before iteration i, arr[:i] is sorted (but not yet final).",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=True,
        in_place=True,
        adaptive=True,
        use_when=(
            "n < ~32, or the data is nearly sorted. This is why every serious "
            "hybrid sort (timsort, introsort) falls back to it at small sizes."
        ),
        avoid_when="Large random input — the O(n^2) is real, not theoretical.",
        pitfalls=[
            "Shifting with arr[j+1] = arr[j] then placing the key once is O(n) "
            "writes per element; swapping instead triples the write traffic.",
            "The while guard needs j >= 0 checked before arr[j] > key, or "
            "Python's negative indexing silently wraps to the end of the list.",
            "Its O(n) best case only holds if you break out of the inner loop; "
            "scanning the whole prefix regardless loses adaptivity.",
        ],
        see_also=["bubble_sort", "shell_sort", "tim_sort", "gnome_sort"],
        interview=[
            "Insertion Sort List (LC 147)",
            "Sort a k-sorted / nearly-sorted array",
        ],
    ),
    Topic(
        slug="selection_sort",
        name="Selection sort",
        family="Sorting / simple",
        module="Sorting.simple.selection_sort",
        entry="selection_sort",
        mental_model=(
            "Scan the unsorted suffix for its minimum, swap it into the front of "
            "that suffix, repeat. The distinguishing feature is the write count: "
            "exactly n-1 swaps, no matter how scrambled the input is."
        ),
        invariant="After pass i, arr[:i+1] holds the i+1 smallest values, sorted and final.",
        complexity=C("O(n^2)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when=(
            "Writes are far more expensive than reads — EEPROM, flash, or a "
            "medium with limited write endurance."
        ),
        avoid_when="You need stability, or the input may already be sorted (no early exit exists).",
        pitfalls=[
            "Swapping the found minimum is what breaks stability; equal values "
            "jump over each other. Shifting instead would fix it and turn the "
            "algorithm into insertion sort.",
            "Comparison count is n(n-1)/2 regardless of input — there is no "
            "best case to optimise toward.",
            "Easy to write the inner loop tracking the minimum *value* instead "
            "of its *index*, which then cannot be swapped.",
        ],
        see_also=["heap_sort", "bubble_sort", "cartesian_tree_sort"],
        interview=["Kth smallest by partial selection", "Why heap sort is 'selection sort with a better bag'"],
    ),
    # ------------------------------------------------------------- efficient
    Topic(
        slug="merge_sort",
        name="Merge sort",
        family="Sorting / efficient",
        module="Sorting.efficient.merge_sort",
        entry="merge_sort",
        mental_model=(
            "Split in half, sort each half, then merge two sorted lists by "
            "repeatedly taking the smaller head. All the work is in the merge; "
            "the split is free. Recursion depth log n, each level touches n "
            "elements, hence n log n with no bad case."
        ),
        invariant=(
            "merge(a, b) emits values in non-decreasing order and, on ties, "
            "takes from `a` first — which is exactly why the sort is stable."
        ),
        complexity=C("O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
        stable=True,
        in_place=False,
        adaptive=False,
        use_when=(
            "Stability is required; sorting linked lists (O(1) extra space "
            "there); external sorting; any guaranteed-n-log-n requirement."
        ),
        avoid_when="Memory is tight and the data is an array — quick sort is in-place and has a smaller constant.",
        pitfalls=[
            "Taking from the right half on ties destroys stability and the bug "
            "is invisible on integers — only visible when sorting records.",
            "Allocating new lists inside the merge at every level is what makes "
            "naive implementations slow; a single scratch buffer reused across "
            "levels is the standard fix.",
            "mid = len(arr) // 2 with a base case of len <= 1 — a base case of "
            "len == 0 recurses forever on single-element lists.",
        ],
        see_also=["tim_sort", "quick_sort", "external_merge_sort", "polyphase_sort"],
        interview=[
            "Sort List (LC 148)",
            "Count of Smaller Numbers After Self (LC 315)",
            "Reverse Pairs / inversion counting (LC 493)",
            "Merge k Sorted Lists (LC 23)",
        ],
    ),
    Topic(
        slug="quick_sort",
        name="Quick sort",
        family="Sorting / efficient",
        module="Sorting.efficient.quick_sort",
        entry="quick_sort",
        mental_model=(
            "Pick a pivot and partition so that smaller values sit left and "
            "larger right. The pivot is now in its final position — permanently. "
            "Recurse on both sides. There is no merge step: the partition *is* "
            "the work."
        ),
        invariant=(
            "After partition(lo, hi) returns p: arr[p] is final, "
            "arr[lo:p] <= arr[p] <= arr[p+1:hi+1]."
        ),
        complexity=C("O(n log n)", "O(n log n)", "O(n^2)", "O(log n)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when=(
            "Default for in-memory arrays. Lower constant factor than merge "
            "sort and sequential memory access that the cache likes."
        ),
        avoid_when=(
            "Worst-case latency matters (use heap sort or introsort), or "
            "stability is required (use merge/tim sort)."
        ),
        pitfalls=[
            "Already-sorted input with a first- or last-element pivot gives "
            "O(n^2) time AND O(n) recursion depth — a stack overflow, not just "
            "slowness. Random or median-of-3 pivot defends against it.",
            "Lomuto and Hoare partition schemes return different things; "
            "copying a recursion line from one into the other loops forever.",
            "Recursing on [lo, p] instead of [lo, p-1] never shrinks the range "
            "when the pivot lands at p == lo.",
            "Arrays of all-equal values degrade to O(n^2) under Lomuto; "
            "three-way (Dutch national flag) partitioning fixes it.",
        ],
        see_also=["intro_sort", "merge_sort", "heap_sort", "bucket_sort"],
        interview=[
            "Kth Largest Element in an Array (LC 215) — quickselect",
            "Sort Colors (LC 75) — three-way partition",
            "Wiggle Sort II (LC 324)",
            "Top K Frequent Elements (LC 347)",
        ],
    ),
    Topic(
        slug="heap_sort",
        name="Heap sort",
        family="Sorting / efficient",
        module="Sorting.efficient.heap_sort",
        entry="heap_sort",
        mental_model=(
            "Selection sort where the 'find the max' step is O(log n) instead of "
            "O(n), because the unsorted region is kept as a max-heap. Build the "
            "heap in O(n), then repeatedly swap the root to the back and sift "
            "down over a region one shorter."
        ),
        invariant=(
            "arr[:heap_size] satisfies the max-heap property and arr[heap_size:] "
            "is sorted and final."
        ),
        complexity=C("O(n log n)", "O(n log n)", "O(n log n)", "O(1)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when=(
            "You need a hard O(n log n) ceiling with O(1) space — embedded, "
            "real-time, or as introsort's bail-out when quick sort goes bad."
        ),
        avoid_when=(
            "Throughput matters on ordinary data: its memory access jumps around "
            "the array, so it loses to quick sort on cache despite equal "
            "asymptotics."
        ),
        pitfalls=[
            "Build the heap bottom-up from n//2 - 1 down to 0 — that is O(n). "
            "Inserting n elements one at a time is O(n log n) and throws away "
            "the cheap build.",
            "The sift-down during the extraction phase must be bounded by the "
            "shrinking heap size, not len(arr), or it pulls sorted values back "
            "into the heap.",
            "Child indices are 2i+1 and 2i+2 for 0-based arrays; the 2i/2i+1 "
            "form is for 1-based and mixing them corrupts the heap silently.",
        ],
        see_also=["min_heap", "max_heap", "selection_sort", "intro_sort"],
        interview=[
            "Kth Largest Element in a Stream (LC 703)",
            "Merge k Sorted Lists (LC 23)",
            "Find Median from Data Stream (LC 295) — two heaps",
        ],
    ),
    # -------------------------------------------------------------- advanced
    Topic(
        slug="shell_sort",
        name="Shell sort",
        family="Sorting / advanced",
        module="Sorting.advanced.shell_sort",
        entry="shell_sort",
        mental_model=(
            "Insertion sort's weakness is that an element can only move one slot "
            "per swap. So run insertion sort on elements a gap apart, shrinking "
            "the gap to 1. Early large-gap passes move values a long way cheaply; "
            "the final gap-1 pass is a plain insertion sort on nearly-sorted data."
        ),
        invariant=(
            "After the pass with gap g, the array is g-sorted: "
            "arr[i] <= arr[i+g] for every valid i."
        ),
        complexity=C("O(n log n)", "depends on gap sequence", "O(n^2) (halving gaps)", "O(1)"),
        stable=False,
        in_place=True,
        adaptive=True,
        use_when="Medium n, no recursion allowed, O(1) space required — common in embedded code.",
        avoid_when="You need a provable bound: its complexity is an open problem for good gap sequences.",
        pitfalls=[
            "The gap sequence IS the algorithm. Naive halving gives O(n^2); "
            "Ciura or Sedgewick sequences are what make it competitive.",
            "Long-range swaps hop over equal values, so it is not stable — "
            "surprising to people who think of it as 'just insertion sort'.",
            "The loop must still end with gap == 1, or the array is only "
            "g-sorted and not sorted.",
        ],
        see_also=["insertion_sort", "comb_sort", "tim_sort"],
        interview=["Rarely asked; cited as the 'gap' idea behind comb sort"],
    ),
    Topic(
        slug="tim_sort",
        name="Tim sort",
        family="Sorting / advanced",
        module="Sorting.advanced.tim_sort",
        entry="tim_sort",
        mental_model=(
            "Real data arrives in runs. Insertion-sort fixed-size blocks, then "
            "merge-sort the blocks together, doubling the merge width each round. "
            "This is CPython's list.sort and Java's Arrays.sort for objects."
        ),
        invariant=(
            "After the run-building phase every block of RUN elements is sorted; "
            "after the merge pass of width w every block of 2w is sorted."
        ),
        complexity=C("O(n)", "O(n log n)", "O(n log n)", "O(n)"),
        stable=True,
        in_place=False,
        adaptive=True,
        use_when="The general-purpose default for real-world, partially-ordered data.",
        avoid_when="Space is tight, or data is uniformly random (plain merge sort is simpler for the same cost).",
        pitfalls=[
            "Production timsort detects *natural* runs of varying length and "
            "reverses descending ones; the fixed-RUN version here is the "
            "simplified teaching form and is not adaptive in the same way.",
            "Merging must walk widths 2*RUN, 4*RUN, ... and clamp the right "
            "edge to n-1, or the last partial block is dropped.",
            "Stability depends on the merge taking from the left run on ties, "
            "same as plain merge sort.",
        ],
        see_also=["merge_sort", "insertion_sort", "intro_sort"],
        interview=[
            "Why is Python's sort stable and fast on real data?",
            "Merge Intervals (LC 56) — sorting nearly-ordered input",
        ],
    ),
    Topic(
        slug="intro_sort",
        name="Intro sort",
        family="Sorting / advanced",
        module="Sorting.advanced.intro_sort",
        entry="introsort",
        mental_model=(
            "Quick sort with two escape hatches. Below a size threshold, switch "
            "to insertion sort (cheaper constants). If recursion exceeds "
            "2*log2(n), switch to heap sort (kills the O(n^2) case). This is "
            "C++ std::sort."
        ),
        invariant=(
            "Quick sort's partition invariant holds, plus: recursion depth never "
            "exceeds maxdepth before heap sort takes over."
        ),
        complexity=C("O(n log n)", "O(n log n)", "O(n log n)", "O(log n)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when="You want quick sort's speed with a guaranteed worst case. The right default for arrays.",
        avoid_when="Stability required — use tim sort.",
        pitfalls=[
            "The depth limit must be decremented per recursive call, not per "
            "partition, or the heap-sort fallback never fires.",
            "Falling back to heap sort on the *whole* array rather than the "
            "current sub-range corrupts already-partitioned regions.",
            "The insertion-sort threshold is a tuned constant (typically 16). "
            "Setting it to 1 makes the hybrid pointless.",
        ],
        see_also=["quick_sort", "heap_sort", "insertion_sort", "tim_sort"],
        interview=["Why does std::sort guarantee O(n log n) when quick sort does not?"],
    ),
    # ------------------------------------------------------- non-comparison
    Topic(
        slug="counting_sort",
        name="Counting sort",
        family="Sorting / non-comparison",
        module="Sorting.non_comparison.counting_sort",
        entry="counting_sort",
        mental_model=(
            "Do not compare — count. Tally how many of each value there is, turn "
            "the tallies into running totals (so each value knows its output "
            "index), then place values from the back to keep equal ones in "
            "order. Beats the n log n comparison bound by not comparing."
        ),
        invariant=(
            "After the prefix-sum step, count[v - min] is one past the last "
            "output index reserved for value v."
        ),
        complexity=C("O(n + k)", "O(n + k)", "O(n + k)", "O(n + k)"),
        stable=True,
        in_place=False,
        adaptive=False,
        use_when="Integer keys with a small range k — ages, scores, bytes, bucket indices.",
        avoid_when="k >> n (the count array dwarfs the data), or keys are floats/strings.",
        pitfalls=[
            "Iterating the input FORWARD when placing breaks stability, which "
            "then breaks radix sort if you use this as its inner pass.",
            "Offsetting by min_val is what allows negative keys; forgetting it "
            "gives an IndexError on any negative input.",
            "k is the value *range*, not the value count: sorting [1, 1000000] "
            "allocates a million slots for two elements.",
        ],
        see_also=["radix_sort", "pigeonhole_sort", "bucket_sort"],
        interview=[
            "Sort Characters By Frequency (LC 451)",
            "H-Index (LC 274)",
            "Maximum Gap (LC 164)",
            "Relative Sort Array (LC 1122)",
        ],
    ),
    Topic(
        slug="radix_sort",
        name="Radix sort",
        family="Sorting / non-comparison",
        module="Sorting.non_comparison.radix_sort",
        entry="radix_sort",
        mental_model=(
            "Sort by the least significant digit, then the next, and so on. Each "
            "pass is a stable counting sort on one digit. Because every pass is "
            "stable, the ordering established by earlier (less significant) "
            "digits survives — that is the whole trick."
        ),
        invariant=(
            "After the pass on digit position d, the array is correctly sorted by "
            "the last d+1 digits of every key."
        ),
        complexity=C("O(d(n + b))", "O(d(n + b))", "O(d(n + b))", "O(n + b)"),
        stable=True,
        in_place=False,
        adaptive=False,
        use_when="Fixed-width integer or string keys, large n — often beats quick sort on 32-bit ints.",
        avoid_when="Variable-length or float keys without transformation; very small n (setup cost dominates).",
        pitfalls=[
            "The per-digit sort MUST be stable. Swap in a non-stable inner sort "
            "and the result is wrong in a way that passes small tests.",
            "LSD-first is for fixed-width keys. MSD-first is needed for "
            "variable-length strings and is a different algorithm.",
            "Negative numbers need separate handling: split by sign, sort the "
            "magnitudes, reverse the negatives. The implementation here takes "
            "non-negative integers only.",
        ],
        see_also=["counting_sort", "bucket_sort", "trie"],
        interview=["Maximum Gap (LC 164)", "Sort integers without comparisons"],
    ),
    Topic(
        slug="bucket_sort",
        name="Bucket sort",
        family="Sorting / non-comparison",
        module="Sorting.non_comparison.bucket_sort",
        entry="bucket_sort",
        mental_model=(
            "Scatter values into k buckets by value range, sort each bucket with "
            "something simple, then read the buckets in order. Fast only if the "
            "input is spread evenly, so that each bucket stays tiny."
        ),
        invariant=(
            "Every value in bucket i is < every value in bucket i+1, so "
            "concatenating sorted buckets in index order yields a sorted array."
        ),
        complexity=C("O(n + k)", "O(n + k)", "O(n^2)", "O(n + k)"),
        stable=True,
        in_place=False,
        adaptive=False,
        use_when="Values are roughly uniformly distributed over a known range — sampled sensor data, random floats.",
        avoid_when="The distribution is skewed or unknown: everything lands in one bucket and you get insertion sort's worst case.",
        pitfalls=[
            "Its cost depends on value *distribution*, unlike counting and radix "
            "sort which depend on value *range*. That distinction is the usual "
            "interview follow-up.",
            "The classic textbook version assumes values in [0, 1) and crashes "
            "on anything else; this implementation rescales by min/max instead.",
            "The maximum value maps to exactly index k and must be clamped to "
            "k-1, or it writes past the last bucket.",
        ],
        see_also=["counting_sort", "radix_sort", "insertion_sort", "quick_sort"],
        interview=["Top K Frequent Elements (LC 347) — bucket by frequency", "Maximum Gap (LC 164)"],
    ),
    Topic(
        slug="pigeonhole_sort",
        name="Pigeonhole sort",
        family="Sorting / non-comparison",
        module="Sorting.non_comparison.pigeonhole_sort",
        entry="pigeonhole_sort",
        mental_model=(
            "One hole per distinct value in the range. Drop each element in its "
            "hole, then walk the holes in order emptying them. Counting sort "
            "without the prefix-sum step — it reconstructs values instead of "
            "moving them."
        ),
        invariant="holes[v - min] holds exactly the count of value v present in the input.",
        complexity=C("O(n + range)", "O(n + range)", "O(n + range)", "O(range)"),
        stable=True,
        in_place=False,
        adaptive=False,
        use_when="Integer keys where the range is close to n — essentially a permutation.",
        avoid_when="Range greatly exceeds n, or keys carry attached data (see below).",
        pitfalls=[
            "Because it rebuilds values from counts rather than moving records, "
            "it cannot carry satellite data. Counting sort can. That is the real "
            "difference between the two, not the complexity.",
            "'Stable' is vacuous here: identical keys are indistinguishable "
            "once reduced to a count.",
            "Allocates max - min + 1 slots, so one outlier value blows up memory.",
        ],
        see_also=["counting_sort", "bucket_sort"],
        interview=["Missing Number (LC 268)", "First Missing Positive (LC 41) — index-as-hole trick"],
    ),
    # --------------------------------------------------------------- network
    Topic(
        slug="odd_even_sort",
        name="Odd-even transposition sort",
        family="Sorting / network",
        module="Sorting.network.odd_even_sort",
        entry="odd_even_sort",
        mental_model=(
            "Bubble sort restructured for parallel hardware. Alternate between "
            "comparing all (odd, even) neighbour pairs and all (even, odd) pairs. "
            "Within one phase no pair shares an element, so every comparison in "
            "that phase can run simultaneously."
        ),
        invariant="After n phases the array is sorted; each phase is a set of independent compare-exchanges.",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=True,
        in_place=True,
        adaptive=True,
        use_when="SIMD, GPU, or systolic arrays — n processors give O(n) depth.",
        avoid_when="Single-threaded code. It is strictly worse than bubble sort there.",
        pitfalls=[
            "The sequential version looks pointlessly slow; its value is the "
            "*dependency structure*, which is invisible in a single-threaded "
            "reading.",
            "The loop must keep alternating until a full odd AND even phase both "
            "make no swaps — stopping after one clean phase leaves it unsorted.",
            "Index bounds differ per phase: start at 1 for odd, 0 for even, and "
            "both must stop at n-1.",
        ],
        see_also=["brick_sort", "bitonic_sort", "bubble_sort"],
        interview=["How would you sort on a GPU?"],
    ),
    Topic(
        slug="brick_sort",
        name="Brick sort",
        family="Sorting / network",
        module="Sorting.network.brick_sort",
        entry="brick_sort",
        mental_model=(
            "Another name for odd-even transposition sort — the alternating "
            "comparison pairs look like a brick wall's offset courses. Kept as a "
            "separate file because both names appear in the literature and you "
            "should recognise either."
        ),
        invariant="Identical to odd-even sort: alternating independent compare-exchange phases.",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=True,
        in_place=True,
        adaptive=True,
        use_when="Same as odd-even sort. The name is the only difference.",
        avoid_when="Same as odd-even sort.",
        pitfalls=[
            "Being asked for 'brick sort' and not recognising it as odd-even "
            "sort is the only real trap here.",
        ],
        see_also=["odd_even_sort", "bitonic_sort"],
        interview=["Terminology recognition only"],
    ),
    Topic(
        slug="bitonic_sort",
        name="Bitonic sort",
        family="Sorting / network",
        module="Sorting.network.bitonic_sort",
        entry="bitonic_sort",
        mental_model=(
            "A *fixed* comparison network: which pairs get compared is decided "
            "in advance, never by the data. Build a bitonic sequence (one that "
            "rises then falls) by sorting one half up and the other down, then "
            "merge it with a recursive half-cleaner."
        ),
        invariant=(
            "After a half-cleaner on a bitonic sequence of length c, every value "
            "in the first half is <= every value in the second, and both halves "
            "are themselves bitonic."
        ),
        complexity=C("O(n log^2 n)", "O(n log^2 n)", "O(n log^2 n)", "O(log n)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when=(
            "Hardware sorting networks and GPUs: O(log^2 n) *depth* with a "
            "data-independent schedule, which is what lets it be baked into "
            "silicon or run branch-free."
        ),
        avoid_when="Sequentially — it does more comparisons than merge sort for no benefit.",
        pitfalls=[
            "The network only exists for power-of-two lengths. Feeding it n=5 "
            "used to return a silently WRONG result here; it now pads with "
            "infinities and truncates.",
            "Data-independence is the point: it performs the same comparisons on "
            "sorted and reversed input, so it cannot be adaptive.",
            "The merge direction parameter must be threaded through the "
            "recursion; hardcoding ascending makes the descending half wrong.",
        ],
        see_also=["odd_even_sort", "merge_sort"],
        interview=["Design a sorting network", "Branch-free / constant-time sorting"],
    ),
    # ----------------------------------------------------------- specialized
    Topic(
        slug="cocktail_shaker_sort",
        name="Cocktail shaker sort",
        family="Sorting / specialized",
        module="Sorting.specialized.cocktail_shaker_sort",
        entry="cocktail_shaker_sort",
        mental_model=(
            "Bidirectional bubble sort. Sweep left-to-right pushing the max to "
            "the end, then right-to-left pulling the min to the front. Fixes "
            "bubble sort's 'turtle' problem: a small value near the end needs n "
            "passes to walk home in one direction but one pass going back."
        ),
        invariant="After a full forward+backward cycle i, both arr[:i] and arr[n-i:] are final.",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=True,
        in_place=True,
        adaptive=True,
        use_when="Nowhere serious. It is the clearest illustration of why traversal direction matters.",
        avoid_when="Production. Still O(n^2); roughly 2x better constant than bubble sort at best.",
        pitfalls=[
            "Both bounds must shrink each cycle — shrinking only the upper one "
            "re-scans the finished prefix forever.",
            "The swapped flag must cover both directions, or it exits after a "
            "clean forward pass while the backward pass still had work.",
        ],
        see_also=["bubble_sort", "gnome_sort", "comb_sort"],
        interview=["Asked as 'how would you improve bubble sort?'"],
    ),
    Topic(
        slug="comb_sort",
        name="Comb sort",
        family="Sorting / specialized",
        module="Sorting.specialized.comb_sort",
        entry="comb_sort",
        mental_model=(
            "Bubble sort plus shell sort's gap idea. Compare elements a gap "
            "apart, shrinking the gap by ~1.3 each pass until it reaches 1. The "
            "large early gaps throw small values near the end a long way forward, "
            "killing bubble sort's turtles."
        ),
        invariant="After the pass with gap g, arr[i] <= arr[i+g] for all valid i.",
        complexity=C("O(n log n)", "O(n^2 / 2^p)", "O(n^2)", "O(1)"),
        stable=False,
        in_place=True,
        adaptive=True,
        use_when="You want near-quick-sort speed in ~15 lines with O(1) space and no recursion.",
        avoid_when="Stability required, or you need a provable bound.",
        pitfalls=[
            "The 1.3 shrink factor is empirical, not derived. 1.25 or 1.33 "
            "measurably degrade it.",
            "The loop must continue while gap > 1 OR a swap happened in the "
            "gap-1 pass; exiting as soon as gap hits 1 leaves it unsorted.",
            "Long-range swaps break stability, same as shell sort.",
        ],
        see_also=["shell_sort", "bubble_sort", "quick_sort"],
        interview=["Rarely asked; good answer to 'improve bubble sort without recursion'"],
    ),
    Topic(
        slug="gnome_sort",
        name="Gnome sort",
        family="Sorting / specialized",
        module="Sorting.specialized.gnome_sort",
        entry="gnome_sort",
        mental_model=(
            "A garden gnome sorting flower pots: look at the pot in front; if it "
            "is smaller, swap it back and step backwards, otherwise step "
            "forwards. One index, one loop, no nesting. Equivalent to insertion "
            "sort done with swaps."
        ),
        invariant="arr[:i] is sorted whenever the index i advances to a new maximum.",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=True,
        in_place=True,
        adaptive=True,
        use_when="Demonstrating that a single index and one loop suffice to sort.",
        avoid_when="Production. Insertion sort does the same work with fewer writes.",
        pitfalls=[
            "Forgetting to step backward after a swap turns it into a single "
            "broken bubble pass.",
            "The index guard i > 0 must come before the comparison, or the "
            "backward step indexes arr[-1] and silently compares the wrong "
            "element.",
        ],
        see_also=["insertion_sort", "bubble_sort"],
        interview=["Trivia; occasionally as 'sort with a single loop variable'"],
    ),
    Topic(
        slug="pancake_sort",
        name="Pancake sort",
        family="Sorting / specialized",
        module="Sorting.specialized.pancake_sort",
        entry="pancake_sort",
        mental_model=(
            "The only operation allowed is 'flip the top k elements' (reverse a "
            "prefix). To place the largest value: flip it to the front, then flip "
            "the whole unsorted region so it lands at the back. Two flips per "
            "element."
        ),
        invariant="After placing i elements, arr[n-i:] is sorted and final, using at most 2i flips.",
        complexity=C("O(n)", "O(n^2)", "O(n^2)", "O(1)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when=(
            "Whenever the cost model is 'prefix reversal' rather than 'swap' — "
            "the classic example of an algorithm shaped by its allowed operation."
        ),
        avoid_when="You are allowed arbitrary swaps. Then it is pointless.",
        pitfalls=[
            "The metric is flip *count*, not comparison count. Optimising "
            "comparisons here misses the point.",
            "Finding the max index then flipping twice is 2 flips per element; "
            "the known lower bound is ~15n/14, and closing that gap is an open "
            "problem (the 'pancake number').",
            "Flipping the whole array instead of the unsorted prefix undoes "
            "already-placed elements.",
        ],
        see_also=["selection_sort", "bubble_sort"],
        interview=["Pancake Sorting (LC 969)", "Reverse prefix problems"],
    ),
    Topic(
        slug="stooge_sort",
        name="Stooge sort",
        family="Sorting / specialized",
        module="Sorting.specialized.stooge_sort",
        entry="stooge_sort",
        mental_model=(
            "Swap the ends if out of order, then recursively sort the first two "
            "thirds, the last two thirds, and the first two thirds AGAIN. The "
            "repeat is load-bearing — without it the array is not sorted. "
            "Complexity O(n^2.71), worse than bubble sort."
        ),
        invariant="After the three recursive calls, arr[lo:hi+1] is sorted. The third call is what restores order disturbed by the second.",
        complexity=C("O(n^2.71)", "O(n^2.71)", "O(n^2.71)", "O(log n)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when="Demonstrating that a recurrence can be worse than the obvious quadratic loop.",
        avoid_when="Always.",
        pitfalls=[
            "Dropping the third recursive call gives a function that sorts most "
            "test inputs and fails on others — a great example of why tests "
            "must include adversarial cases.",
            "The two-thirds split must round *up* (2*(h-l+1)//3) or the "
            "recursion does not shrink and never terminates.",
        ],
        see_also=["bogosort", "bubble_sort"],
        interview=["Used to teach Master-theorem recurrence analysis"],
    ),
    Topic(
        slug="bogosort",
        name="Bogosort",
        family="Sorting / specialized",
        module="Sorting.specialized.bogosort",
        entry="bogosort",
        mental_model=(
            "Shuffle at random; check if sorted; repeat. Expected O(n * n!) "
            "comparisons. It exists to make the cost of 'generate and test' with "
            "no structure viscerally obvious."
        ),
        invariant="None. That is the lesson — the algorithm maintains nothing between iterations.",
        complexity=C("O(n)", "O(n * n!)", "unbounded", "O(1)"),
        stable=False,
        in_place=True,
        adaptive=False,
        use_when="Illustrating expected-versus-worst-case and why unbounded loops need attempt caps.",
        avoid_when="Always. n=12 already exceeds the age of the universe on average.",
        pitfalls=[
            "Worst case is genuinely unbounded, not merely large — hence the "
            "max_attempts cap in this implementation, which means it can return "
            "UNSORTED output. Check the return value.",
            "Tests must stay under ~8 elements or the suite hangs.",
        ],
        see_also=["stooge_sort", "sleep_sort"],
        interview=["Expected vs worst case analysis"],
    ),
    Topic(
        slug="sleep_sort",
        name="Sleep sort",
        family="Sorting / specialized",
        module="Sorting.specialized.sleep_sort",
        entry="sleep_sort",
        mental_model=(
            "Spawn a thread per value that sleeps proportionally to the value, "
            "then appends itself. The OS scheduler does the ordering. Running "
            "time depends on the magnitude of the values, not on how many there "
            "are — which disqualifies it as a sorting algorithm."
        ),
        invariant="None that the code enforces. Ordering is delegated to the scheduler, so there is no guarantee at all.",
        complexity=C("O(max(arr))", "O(max(arr))", "unbounded", "O(n) threads"),
        stable=False,
        in_place=False,
        adaptive=False,
        use_when="Illustrating that 'it produced sorted output' is not proof of correctness.",
        avoid_when="Always. Negative values are impossible and close values race.",
        pitfalls=[
            "A tempting 'fix' is to sort the output before returning — which "
            "makes the whole function a wrapper around the builtin. This "
            "implementation deliberately does not, so the flakiness stays "
            "visible.",
            "Values closer together than scheduler jitter can wake out of order. "
            "Raising the time unit trades latency for reliability.",
            "One OS thread per element: a few thousand values will exhaust "
            "thread limits.",
        ],
        see_also=["bogosort", "counting_sort"],
        interview=["Why is this not O(n)?"],
    ),
    # ------------------------------------------------------------ tree-based
    Topic(
        slug="tree_sort",
        name="Tree sort",
        family="Sorting / tree-based",
        module="Sorting.tree_based.tree_sort",
        entry="tree_sort",
        mental_model=(
            "Insert everything into a binary search tree, then read it back with "
            "an inorder traversal. The BST's ordering invariant does the sorting; "
            "the traversal just reports it."
        ),
        invariant="The BST property (left < node <= right) holds after every insert, so inorder yields sorted output.",
        complexity=C("O(n log n)", "O(n log n)", "O(n^2)", "O(n)"),
        stable=False,
        in_place=False,
        adaptive=False,
        use_when="You need the sorted structure to stay queryable afterwards — supports later insert, delete, predecessor, range queries.",
        avoid_when="You only need a sorted list once. The tree's pointer overhead and cache behaviour lose badly to quick sort.",
        pitfalls=[
            "Sorted input builds a degenerate linked list: O(n^2) time and O(n) "
            "recursion depth. A self-balancing tree (AVL, red-black) fixes it.",
            "Recursive inorder traversal overflows the stack on that degenerate "
            "shape; an explicit stack or Morris traversal does not.",
            "Duplicate handling must be decided explicitly — dropping them makes "
            "it a set, not a sort.",
        ],
        see_also=["bst", "cartesian_tree_sort", "traversals", "heap_sort"],
        interview=[
            "Kth Smallest Element in a BST (LC 230)",
            "Validate BST (LC 98)",
            "Count of Smaller Numbers After Self (LC 315)",
        ],
    ),
    Topic(
        slug="cartesian_tree_sort",
        name="Cartesian tree sort",
        family="Sorting / tree-based",
        module="Sorting.tree_based.cartesian_tree_sort",
        entry="cartesian_tree_sort",
        mental_model=(
            "Build a tree that is a min-heap by value AND reproduces the original "
            "array on an inorder walk. Then selection-sort through a priority "
            "queue seeded with the root, pushing a node's children when it is "
            "popped. The heap only holds the current frontier."
        ),
        invariant=(
            "Tree: heap-ordered by value, inorder == input order. Extraction: the "
            "frontier heap always contains the minimum of every not-yet-emitted "
            "subtree root."
        ),
        complexity=C("O(n)", "O(n log n)", "O(n log n)", "O(n)"),
        stable=False,
        in_place=False,
        adaptive=True,
        use_when="Input has long pre-sorted runs — cost is O(n log k) for k runs, approaching O(n) on sorted data.",
        avoid_when="Uniformly random data: tim sort is adaptive too and has far better constants.",
        pitfalls=[
            "An inorder traversal of a Cartesian tree returns the ORIGINAL "
            "array — that is its defining property. A previous version of this "
            "file did inorder then called sorted() on the result, making the "
            "whole thing theatre around the builtin.",
            "The O(n) build is amortised via the stack: each node is pushed and "
            "popped at most once. Re-scanning the spine per element makes it "
            "O(n^2).",
            "The priority queue must hold (value, tiebreak, node) so equal "
            "values never force a comparison of two nodes.",
        ],
        see_also=["tree_sort", "min_heap", "tim_sort", "quick_sort"],
        interview=[
            "Largest Rectangle in Histogram (LC 84) — same monotonic-stack build",
            "Maximum Binary Tree (LC 654) — literally a Cartesian tree",
            "Treaps: BST by key, heap by priority",
        ],
    ),
    # -------------------------------------------------------------- external
    Topic(
        slug="external_merge_sort",
        name="External merge sort",
        family="Sorting / external",
        module="Sorting.external.external_merge_sort",
        entry="external_merge_sort",
        mental_model=(
            "The data does not fit in RAM. Pass 1: read chunks that do fit, sort "
            "each in memory, write them back as sorted runs. Pass 2: k-way merge "
            "all runs with a heap holding one pending value per run. Peak memory "
            "is O(chunk + runs), independent of total size."
        ),
        invariant="Every chunk file is internally sorted, and the merge heap's root is always the globally smallest unemitted value.",
        complexity=C("O(n log n)", "O(n log n)", "O(n log n)", "O(chunk + k) in memory"),
        stable=True,
        in_place=False,
        adaptive=False,
        use_when="Input exceeds memory — log files, database sort-merge joins, ETL pipelines.",
        avoid_when="Data fits in memory. The I/O constant factor is enormous.",
        pitfalls=[
            "The merge must stream (one line per run in memory). Reading whole "
            "runs in defeats the entire purpose.",
            "Chunk files are temporary state and must be cleaned up; an earlier "
            "version wrote chunk_*.txt into the working directory and left them "
            "behind, which also made concurrent calls collide.",
            "Real systems tune chunk_size to available RAM and k to the OS file "
            "descriptor limit — k is not free.",
        ],
        see_also=["merge_sort", "polyphase_sort", "min_heap"],
        interview=[
            "Sort a 100GB file with 1GB of RAM",
            "Merge k Sorted Lists (LC 23) — the in-memory core",
            "Find the median of a file too large to load",
        ],
    ),
    Topic(
        slug="polyphase_sort",
        name="Polyphase merge sort",
        family="Sorting / external",
        module="Sorting.external.polyphase_sort",
        entry="polyphase_sort",
        mental_model=(
            "External sorting when you have a fixed, small number of tapes. "
            "Distribute runs across tapes, merge two onto the third, repeat. "
            "True polyphase splits runs in Fibonacci proportions so one tape "
            "empties exactly as a merge completes, removing the rewind pass."
        ),
        invariant="Each tape holds a sequence of internally-sorted runs; each merge pass halves the run count and at least one tape becomes empty.",
        complexity=C("O(n log n)", "O(n log n)", "O(n log n)", "O(run_size) in memory"),
        stable=False,
        in_place=False,
        adaptive=False,
        use_when="Historical interest, and any setting with a hard cap on simultaneous output streams.",
        avoid_when="Modern storage with random access — plain external merge sort is simpler and faster.",
        pitfalls=[
            "A tape holds a SEQUENCE of runs, not one sorted stream. Merging two "
            "tapes as if each were a single sorted stream produces silently "
            "unsorted output — which is what this file did before it was fixed. "
            "Run boundaries are found by detecting a descent in value.",
            "This implementation is the simpler *balanced* 3-tape merge, not "
            "true Fibonacci polyphase. The distinction is the whole point of the "
            "name, so do not claim the latter in an interview.",
            "Termination is 'one tape left holding ONE run', not 'one tape left'. "
            "Stopping at the weaker condition emits a partially sorted file.",
            "Empty input used to loop forever here: no tape ever became "
            "non-empty, so the terminating condition was unreachable.",
            "Hard-coded tape filenames in the working directory made two "
            "concurrent sorts silently corrupt each other.",
        ],
        see_also=["external_merge_sort", "merge_sort"],
        interview=["Tape-based sorting history; why Fibonacci numbers appear in it"],
    ),
]
