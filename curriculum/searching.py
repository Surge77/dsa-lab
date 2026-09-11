"""Curriculum entries for every searching algorithm in the lab."""

from curriculum.schema import Complexity, Topic

C = Complexity

SEARCHING_TOPICS = [
    # ------------------------------------------------------- linear family
    Topic(
        slug="linear_search",
        name="Linear search",
        family="Searching / linear",
        module="Searching.linear_search_family.basic_linear_search",
        entry="linear_search",
        mental_model=(
            "Look at every element until you find the target. The only search "
            "that requires nothing of the data — no ordering, no indexing, no "
            "random access. That is its entire value."
        ),
        invariant="After checking index i, the target is known not to be in arr[:i+1].",
        complexity=C("O(1)", "O(n)", "O(n)", "O(1)"),
        use_when=(
            "Unsorted data, linked lists, streams, or n small enough that "
            "sorting first costs more than scanning."
        ),
        avoid_when="The data is sorted and randomly accessible — binary search is free at that point.",
        pitfalls=[
            "Returning a boolean instead of an index throws away information the "
            "caller usually needs.",
            "linear_search_all returns every match; the single-result version "
            "returns the FIRST. Confusing the two is a classic off-by-many bug.",
            "Sorting in order to binary search costs O(n log n) — never worth it "
            "for a single lookup.",
        ],
        see_also=["sentinel_search", "bidirectional_linear_search", "binary_search"],
        interview=["Baseline for 'can you do better?' follow-ups", "Two Sum (LC 1) brute force"],
    ),
    Topic(
        slug="recursive_linear_search",
        name="Recursive linear search",
        family="Searching / linear",
        module="Searching.linear_search_family.recursive_linear_search",
        entry="recursive_linear_search",
        mental_model=(
            "Linear search written as recursion: either index i holds the target, "
            "or the answer is in the rest of the array. Pedagogically useful, "
            "practically worse — Python has no tail-call elimination."
        ),
        invariant="The call at index i has already ruled out arr[:i].",
        complexity=C("O(1)", "O(n)", "O(n)", "O(n) stack"),
        use_when="Demonstrating how an iterative loop maps to a recurrence.",
        avoid_when=(
            "Any real array. O(n) stack frames means RecursionError around "
            "n=1000 in CPython, where the loop version happily does millions."
        ),
        pitfalls=[
            "The base case must be idx >= len(arr), not idx == len(arr) — a "
            "caller passing a larger start index otherwise recurses forever.",
            "Space goes from O(1) to O(n). That is the real cost of the rewrite "
            "and the thing to say out loud in an interview.",
        ],
        see_also=["linear_search", "recursive_binary_search"],
        interview=["Convert recursion to iteration and state the space change"],
    ),
    Topic(
        slug="bidirectional_linear_search",
        name="Bidirectional linear search",
        family="Searching / linear",
        module="Searching.linear_search_family.bidirectional_linear_search",
        entry="bidirectional_linear_search",
        mental_model=(
            "Scan from both ends toward the middle. Halves the expected number "
            "of iterations but not the number of comparisons — each iteration "
            "now does two. Still O(n)."
        ),
        invariant="After iteration k, the target is known not to be in arr[:k+1] or arr[n-k-1:].",
        complexity=C("O(1)", "O(n/2) iterations, O(n) comparisons", "O(n)", "O(1)"),
        use_when="The target is likely near either end, or you want the wall-clock win from better cache prefetching in two directions.",
        avoid_when="You need the first match in index order — it may find the later one first.",
        pitfalls=[
            "It does NOT halve the work: two comparisons per iteration over n/2 "
            "iterations is the same n comparisons. The asymptotic class is "
            "unchanged.",
            "With duplicates it can return the rightmost match, breaking any "
            "caller expecting leftmost-first semantics.",
            "The loop must stop when left > right, not left == right, or the "
            "middle element is checked twice or skipped on odd lengths.",
        ],
        see_also=["linear_search", "sentinel_search"],
        interview=["Honest answer to 'how would you speed up linear search?' — you cannot, asymptotically"],
    ),
    Topic(
        slug="sentinel_search",
        name="Sentinel linear search",
        family="Searching / linear",
        module="Searching.linear_search_family.sentinel_linear_search",
        entry="sentinel_search",
        mental_model=(
            "A linear scan has two checks per step: 'found it?' and 'ran off the "
            "end?'. Plant the target in the last slot as a sentinel and the "
            "bounds check becomes unnecessary — the loop is guaranteed to stop. "
            "One comparison per iteration instead of two."
        ),
        invariant="The target is always present in the array during the scan, so the loop always terminates without a bounds test.",
        complexity=C("O(1)", "O(n)", "O(n)", "O(1)"),
        use_when="Tight inner loops in a low-level language where halving per-iteration comparisons is measurable.",
        avoid_when="Python (interpreter overhead swamps the saving), or the array is read-only/shared.",
        pitfalls=[
            "The last element MUST be saved and restored, including on the error "
            "path. Forgetting is a data-corruption bug, not a wrong answer.",
            "After restoring, the saved last element must be checked separately — "
            "otherwise a target that genuinely lived in the last slot is reported "
            "as the sentinel hit.",
            "It mutates its input. Unsafe on shared or frozen data even though "
            "the mutation is temporary.",
        ],
        see_also=["linear_search", "bidirectional_linear_search"],
        interview=["Micro-optimisation reasoning; loop-invariant removal"],
    ),
    # ------------------------------------------------------- binary family
    Topic(
        slug="binary_search",
        name="Binary search (iterative)",
        family="Searching / binary",
        module="Searching.binary_search_family.basic_binary_search",
        entry="binary_search",
        mental_model=(
            "Maintain a window that must contain the answer if it exists. Compare "
            "the middle; discard the half that cannot contain the target. Every "
            "step halves the window, so log2(n) steps suffice. The hard part is "
            "never the idea — it is the boundary arithmetic."
        ),
        invariant=(
            "If the target is present, its index lies in [left, right]. Every "
            "iteration must strictly shrink that window."
        ),
        complexity=C("O(1)", "O(log n)", "O(log n)", "O(1)"),
        use_when="Sorted, randomly-accessible data. Also any monotone predicate — see ubiquitous_binary_search.",
        avoid_when="Unsorted data, linked lists (no O(1) indexing), or a single lookup on unsorted input.",
        pitfalls=[
            "left + (right - left) // 2 rather than (left + right) // 2 avoids "
            "integer overflow. Irrelevant in Python, but it is the canonical "
            "answer and the reason is worth knowing.",
            "while left <= right with right = mid - 1 is the closed-interval "
            "form. Mixing it with the half-open form (right = mid, while left < "
            "right) gives an off-by-one or an infinite loop.",
            "It returns SOME matching index, not the first. Leftmost/rightmost "
            "bounds need the variant that keeps searching after a hit.",
            "Requires the array to actually be sorted. It fails silently, not "
            "loudly, on unsorted input.",
        ],
        see_also=[
            "recursive_binary_search",
            "ubiquitous_binary_search",
            "exponential_search",
            "rotated_binary_search",
            "interpolation_search",
        ],
        interview=[
            "Binary Search (LC 704)",
            "First Bad Version (LC 278)",
            "Search Insert Position (LC 35)",
            "Find First and Last Position (LC 34)",
        ],
    ),
    Topic(
        slug="recursive_binary_search",
        name="Binary search (recursive)",
        family="Searching / binary",
        module="Searching.binary_search_family.recursive_binary_search",
        entry="recursive_binary_search",
        mental_model=(
            "The same halving, expressed as a recurrence: T(n) = T(n/2) + O(1). "
            "Reads closer to the proof than the loop does, at the cost of "
            "O(log n) stack frames."
        ),
        invariant="Each call is handed a window that contains the target if it exists anywhere.",
        complexity=C("O(1)", "O(log n)", "O(log n)", "O(log n) stack"),
        use_when="When the recurrence makes the argument clearer — teaching, or proving correctness.",
        avoid_when="Hot paths. log n frames is cheap but not free, and the loop form is no harder to read.",
        pitfalls=[
            "A mutable default like right=None must be resolved on the first "
            "call only; re-deriving len(arr) every call is harmless here but the "
            "habit breaks other recursions.",
            "The base case is left > right, returning -1. Using left == right "
            "misses single-element windows.",
            "Must return the recursive call's value. Calling without returning "
            "yields None, which is falsy like -1 and so passes sloppy tests.",
        ],
        see_also=["binary_search", "recursive_linear_search"],
        interview=["Same problems as binary search; state the O(log n) space cost"],
    ),
    Topic(
        slug="exponential_search",
        name="Exponential search",
        family="Searching / binary",
        module="Searching.binary_search_family.exponential_search",
        entry="exponential_search",
        mental_model=(
            "Find a bound before you bisect. Double the index (1, 2, 4, 8, ...) "
            "until you overshoot the target, then binary search the last doubled "
            "range. Total O(log i) where i is the answer's index — independent of "
            "the array's total length."
        ),
        invariant="When the doubling stops at bound b, the target (if present) lies in [b//2, min(b, n-1)].",
        complexity=C("O(1)", "O(log i)", "O(log n)", "O(1)"),
        use_when=(
            "Unbounded or unknown-length sorted input (a sorted stream, an API "
            "that 404s past the end), or when the target is expected near the "
            "front."
        ),
        avoid_when="Plain bounded arrays where the target is uniformly distributed — plain binary search is simpler.",
        pitfalls=[
            "Check arr[0] first. The doubling loop starts at index 1 and would "
            "otherwise never test index 0.",
            "The upper bound must be clamped to n-1 before the binary search, or "
            "it indexes past the end.",
            "It is O(log i), not O(log n). That is the whole selling point and "
            "the thing interviewers are listening for.",
        ],
        see_also=["binary_search", "jump_search", "fibonacci_search"],
        interview=[
            "Search in a Sorted Array of Unknown Size (LC 702)",
            "Find the length of an unbounded sorted stream",
        ],
    ),
    Topic(
        slug="fibonacci_search",
        name="Fibonacci search",
        family="Searching / binary",
        module="Searching.binary_search_family.fibonacci_search",
        entry="fibonacci_search",
        mental_model=(
            "Binary search that splits by Fibonacci numbers instead of halving. "
            "The split points only ever move forward by addition and subtraction "
            "— no division — and each probe is nearer the previous one, which "
            "suited tape and drum storage."
        ),
        invariant="The remaining window length is always a Fibonacci number, and probe offsets are computed by subtraction alone.",
        complexity=C("O(1)", "O(log n)", "O(log n)", "O(1)"),
        use_when="Hardware without division, or non-uniform access cost where probe locality matters (tape, spinning disk).",
        avoid_when="Ordinary RAM. Binary search is simpler and identical asymptotically.",
        pitfalls=[
            "The comparison count is marginally WORSE than binary search — the "
            "win is arithmetic simplicity and probe locality, not fewer probes.",
            "The Fibonacci numbers must be generated up to >= n before the search "
            "starts; generating them lazily inside the loop loses the point.",
            "The probe index must be clamped with min(offset + fib, n-1).",
        ],
        see_also=["binary_search", "exponential_search", "ternary_search"],
        interview=["Trivia; good answer to 'search without using division'"],
    ),
    Topic(
        slug="interpolation_search",
        name="Interpolation search",
        family="Searching / binary",
        module="Searching.binary_search_family.interpolation_search",
        entry="interpolation_search",
        mental_model=(
            "How a human uses a phone book: looking for 'Aaron', you open near "
            "the front, not the middle. Estimate the position by linear "
            "interpolation between the window's endpoint values. On uniformly "
            "distributed data this gives O(log log n)."
        ),
        invariant="Same window invariant as binary search; only the choice of probe position differs.",
        complexity=C("O(1)", "O(log log n) if uniform", "O(n)", "O(1)"),
        use_when="Sorted AND approximately uniformly distributed numeric keys — timestamps, sequential IDs, sensor readings.",
        avoid_when="Skewed or clustered distributions. Exponentially-spaced values degrade it to O(n), worse than binary search.",
        pitfalls=[
            "Division by zero when arr[high] == arr[low] — must be guarded "
            "before computing the probe.",
            "The probe position must be bounds-checked: interpolation can point "
            "outside [low, high] when the target is out of range.",
            "Its advantage is entirely distribution-dependent. On adversarial "
            "input it is strictly worse than binary search, which is the "
            "trade-off to name out loud.",
        ],
        see_also=["binary_search", "bucket_sort", "jump_search"],
        interview=["When does binary search lose to something else?", "Searching uniformly distributed keys"],
    ),
    Topic(
        slug="rotated_binary_search",
        name="Rotated array binary search",
        family="Searching / binary",
        module="Searching.binary_search_family.rotated_binary_search",
        entry="rotated_binary_search",
        mental_model=(
            "A sorted array rotated at an unknown pivot. Crucially, at least one "
            "half of any window is still properly sorted. Identify which half "
            "that is, test whether the target falls inside its range, and discard "
            "one half as usual."
        ),
        invariant=(
            "For any window, arr[low] <= arr[mid] implies the left half is "
            "sorted; otherwise the right half is. The target's membership in the "
            "sorted half is then a simple range test."
        ),
        complexity=C("O(1)", "O(log n)", "O(log n)", "O(1)"),
        use_when="Circular buffers, sorted data with an unknown offset, any 'sorted then rotated' problem.",
        avoid_when="Duplicates are present — they break the sorted-half test and force O(n) worst case.",
        pitfalls=[
            "Duplicates are the killer: with [1,1,1,0,1] you cannot tell which "
            "half is sorted, and the worst case becomes O(n). That is LC 81 "
            "versus LC 33.",
            "The range test on the sorted half must be inclusive at both ends, "
            "or boundary targets are missed.",
            "Using arr[low] <= arr[mid] (not <) matters for two-element windows.",
        ],
        see_also=["binary_search", "ubiquitous_binary_search"],
        interview=[
            "Search in Rotated Sorted Array (LC 33)",
            "Search in Rotated Sorted Array II (LC 81) — with duplicates",
            "Find Minimum in Rotated Sorted Array (LC 153)",
        ],
    ),
    # ----------------------------------------------------------- advanced
    Topic(
        slug="jump_search",
        name="Jump search",
        family="Searching / advanced",
        module="Searching.advanced.jump_search",
        entry="jump_search",
        mental_model=(
            "Step forward in fixed blocks of size sqrt(n) until you overshoot, "
            "then linear-scan back through that one block. Optimal block size is "
            "sqrt(n), giving O(sqrt n) — worse than binary search but with only "
            "forward jumps."
        ),
        invariant="When the jump stops at block boundary b, the target (if present) lies in (b - step, b].",
        complexity=C("O(1)", "O(sqrt n)", "O(sqrt n)", "O(1)"),
        use_when=(
            "Jumping backwards is expensive or impossible — tape, a singly "
            "linked skip structure, or paged storage where a seek costs far more "
            "than a sequential read."
        ),
        avoid_when="Ordinary arrays. O(sqrt n) loses badly to O(log n).",
        pitfalls=[
            "Block size sqrt(n) is derived by minimising n/m + m; any other "
            "constant is worse. Knowing *why* sqrt is the answer is the point.",
            "The backward scan must stop at the previous block boundary, not "
            "run to index 0 — otherwise it degrades to linear search.",
            "min(step, n) clamping is needed or the last partial block is read "
            "out of bounds.",
        ],
        see_also=["binary_search", "exponential_search", "linear_search"],
        interview=["Search with only forward traversal", "Why sqrt(n)? Derive the optimum"],
    ),
    Topic(
        slug="ternary_search",
        name="Ternary search",
        family="Searching / advanced",
        module="Searching.advanced.ternary_search",
        entry="ternary_search",
        mental_model=(
            "Split into three parts with two probes instead of two parts with "
            "one. Fewer iterations (log base 3) but more comparisons per "
            "iteration, so for *sorted array lookup* it is strictly worse than "
            "binary search. Its real home is finding the extremum of a unimodal "
            "function."
        ),
        invariant="Array form: the target lies in one of the three sub-ranges. Unimodal form: the maximum lies in the retained two-thirds.",
        complexity=C("O(1)", "O(log3 n) iterations, ~2 log3 n comparisons", "O(log n)", "O(1)"),
        use_when="Maximising or minimising a unimodal function over a range — that is the legitimate use.",
        avoid_when=(
            "Sorted array lookup. 2*log3(n) ≈ 1.26*log2(n) comparisons means it "
            "does about 26% MORE work than binary search."
        ),
        pitfalls=[
            "Believing 'three parts beats two'. Count comparisons, not "
            "iterations — binary search wins. This is the classic trap.",
            "For unimodal optimisation the function must be strictly unimodal; "
            "a flat plateau makes the comparison ambiguous and the search can "
            "discard the answer.",
            "Both mid points must be recomputed each iteration from the current "
            "window, not carried over.",
        ],
        see_also=["binary_search", "fibonacci_search", "ubiquitous_binary_search"],
        interview=[
            "Peak Index in a Mountain Array (LC 852)",
            "Find Peak Element (LC 162)",
            "Why is ternary search slower than binary search?",
        ],
    ),
    Topic(
        slug="ubiquitous_binary_search",
        name="Ubiquitous binary search (predicate form)",
        family="Searching / advanced",
        module="Searching.advanced.ubiquitous_binary_search",
        entry="ubiquitous_binary_search",
        mental_model=(
            "The general form, and the one worth memorising. Given a monotone "
            "predicate over a range (false...false, true...true), find the first "
            "true. No array is required — the 'array' can be any answer space. "
            "This single shape solves most binary-search interview problems."
        ),
        invariant=(
            "predicate(lo - 1) is false and predicate(hi) is true at all times, "
            "so the boundary is always inside [lo, hi]."
        ),
        complexity=C("O(1)", "O(log(hi - lo)) predicate calls", "O(log(hi - lo))", "O(1)"),
        use_when=(
            "Anything phrased as 'minimum X such that condition holds' — "
            "capacity, speed, threshold, or 'binary search on the answer'."
        ),
        avoid_when="The predicate is not monotone. Then the whole method is invalid, not merely slow.",
        pitfalls=[
            "Monotonicity must be verified, not assumed. It is the entire "
            "precondition and the usual source of wrong answers.",
            "Use the half-open form: while lo < hi, mid = lo + (hi-lo)//2, then "
            "hi = mid or lo = mid + 1. Mixing in right = mid - 1 loops forever.",
            "The initial hi must be a value where the predicate is known true — "
            "an upper bound on the answer, not the array length.",
        ],
        see_also=["binary_search", "rotated_binary_search", "ternary_search"],
        interview=[
            "Koko Eating Bananas (LC 875)",
            "Capacity To Ship Packages (LC 1011)",
            "Split Array Largest Sum (LC 410)",
            "Minimum Number of Days to Make m Bouquets (LC 1482)",
            "Median of Two Sorted Arrays (LC 4)",
        ],
    ),
    Topic(
        slug="sublist_search",
        name="Sublist search (pattern in list)",
        family="Searching / advanced",
        module="Searching.advanced.sublist_search",
        entry="sublist_search",
        mental_model=(
            "Does this sequence appear contiguously inside that one? Anchor at "
            "each position in the main list and walk both forward together. The "
            "naive O(n*m) version — which is what makes KMP and Rabin-Karp worth "
            "learning."
        ),
        invariant="If a match exists starting at index i, the walk from i compares equal for all m pattern elements.",
        complexity=C("O(m)", "O(n*m)", "O(n*m)", "O(1)"),
        use_when="Short patterns, or linked lists where the clever algorithms' index arithmetic does not apply.",
        avoid_when="Long patterns over long text — KMP is O(n+m), Rabin-Karp is O(n+m) expected.",
        pitfalls=[
            "The empty pattern should match at index 0 by convention; deciding "
            "that explicitly prevents an ambiguous -1.",
            "The outer loop must stop at n - m, not n, or the inner walk runs "
            "off the end.",
            "Naive matching re-compares characters the previous attempt already "
            "examined. Recognising that waste is exactly the insight KMP's "
            "failure function exploits.",
        ],
        see_also=["linear_search", "trie"],
        interview=[
            "Implement strStr() (LC 28)",
            "Repeated Substring Pattern (LC 459)",
            "Follow-up: now do it in O(n+m) — KMP",
        ],
    ),
    # --------------------------------------------------------- tree search
    Topic(
        slug="astar",
        name="A* tree search",
        family="Searching / tree",
        module="Searching.tree_search_family.astar",
        entry="astar_tree_search",
        mental_model=(
            "Best-first search ordered by f = g + h: g is the cost already paid, "
            "h is an estimate of the cost remaining. Pure g is Dijkstra; pure h "
            "is greedy best-first; A* is the combination, and the heuristic is "
            "what lets it ignore most of the search space."
        ),
        invariant=(
            "If h never overestimates the true remaining cost (admissible), the "
            "first time the goal is popped, its path is optimal."
        ),
        complexity=C("O(b*d)", "O(b^d) worst", "O(b^d)", "O(b^d) frontier"),
        use_when="Pathfinding with a usable distance estimate — grids, maps, games, puzzle solving.",
        avoid_when="No meaningful heuristic exists (then it is just Dijkstra with overhead), or the graph is tiny.",
        pitfalls=[
            "An inadmissible heuristic (one that overestimates) breaks the "
            "optimality guarantee — you still get an answer, just not the best "
            "one, silently.",
            "Heap entries must carry a tiebreaker counter so equal f-scores never "
            "force a comparison of two node objects (TypeError in Python 3).",
            "On a general graph A* also needs consistency/monotonicity of h, or a "
            "closed set with re-opening. On a tree each node has one path, which "
            "is why this tree-only version is simpler.",
            "h = 0 reduces it to Dijkstra. Useful sanity check when debugging a "
            "suspicious heuristic.",
        ],
        see_also=["min_heap", "directed_weighted_graph", "undirected_weighted_graph", "traversals"],
        interview=[
            "Network Delay Time (LC 743) — Dijkstra",
            "Shortest Path in Binary Matrix (LC 1091)",
            "Sliding Puzzle (LC 773)",
            "When does A* degenerate to Dijkstra or to BFS?",
        ],
    ),
]
