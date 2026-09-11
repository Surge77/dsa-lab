"""Curriculum entries for the data structures in the lab."""

from curriculum.schema import Complexity, Topic

C = Complexity

STRUCTURE_TOPICS = [
    # ----------------------------------------------------------- linear
    Topic(
        slug="my_array",
        name="Dynamic array",
        family="Structures / linear",
        module="Linear.arrays",
        entry="MyArray",
        doc="docs/array.md",
        mental_model=(
            "Contiguous memory with spare capacity at the end. Appending is O(1) "
            "until the buffer fills, at which point you allocate a bigger one and "
            "copy everything across. Doubling the capacity makes that copy cost "
            "amortise to O(1) per append."
        ),
        invariant="0 <= size <= capacity, and elements occupy exactly slots [0, size).",
        complexity=C("O(1) index", "O(1) amortised append", "O(n) insert/delete at front", "O(n)"),
        use_when="You index by position, iterate in order, or care about cache locality. The default sequence.",
        avoid_when="Frequent insertion or deletion in the middle or at the front — that is a linked list's job.",
        pitfalls=[
            "Growing by a constant (+1, +10) instead of a factor makes n appends "
            "cost O(n^2). Doubling is what buys the amortised O(1).",
            "Amortised O(1) is not worst-case O(1): one unlucky append pays O(n). "
            "That distinction matters for real-time systems.",
            "Deleting from the middle must shift the tail left; forgetting to "
            "decrement size leaves a stale duplicate of the last element.",
        ],
        see_also=["singly_linked_list", "stack", "queue"],
        interview=["Design a dynamic array", "Why is append amortised O(1)?", "Remove Element (LC 27)"],
    ),
    Topic(
        slug="stack",
        name="Stack (LIFO)",
        family="Structures / linear",
        module="Linear.stack",
        entry="Stack",
        doc="docs/stack.md",
        mental_model=(
            "A pile where you can only touch the top. Last in, first out. The "
            "reason it appears everywhere is that it mirrors nesting — function "
            "calls, brackets, undo history, and any 'most recent unmatched thing' "
            "question."
        ),
        invariant="The only accessible element is the one most recently pushed and not yet popped.",
        complexity=C("O(1) push", "O(1) pop", "O(1) peek", "O(n)"),
        use_when="Anything with nesting or backtracking: expression parsing, DFS, undo, monotonic-stack problems.",
        avoid_when="You need access to the oldest element — that is a queue.",
        pitfalls=[
            "Pop and peek on an empty stack must raise, not return None: None is "
            "a legitimate stored value and silently conflating them hides bugs.",
            "Array-backed pop from the END is O(1); popping from index 0 is O(n) "
            "and turns the structure into a slow queue.",
            "Recursion IS an implicit stack. Converting recursion to iteration "
            "means making that stack explicit, which is the usual follow-up.",
        ],
        see_also=["queue", "my_array", "traversals", "singly_linked_list"],
        interview=[
            "Valid Parentheses (LC 20)",
            "Min Stack (LC 155)",
            "Daily Temperatures (LC 739) — monotonic stack",
            "Largest Rectangle in Histogram (LC 84)",
            "Evaluate Reverse Polish Notation (LC 150)",
        ],
    ),
    Topic(
        slug="queue",
        name="Queue (FIFO)",
        family="Structures / linear",
        module="Linear.queue",
        entry="Queue",
        doc="docs/queue.md",
        mental_model=(
            "A line at a counter. First in, first out. Where a stack explores "
            "depth-first, a queue explores breadth-first — which is exactly why "
            "BFS finds shortest paths in unweighted graphs and DFS does not."
        ),
        invariant="Elements leave in the order they arrived; enqueue touches only the tail, dequeue only the head.",
        complexity=C("O(1) enqueue", "O(1) dequeue (with proper backing)", "O(1) peek", "O(n)"),
        use_when="BFS, level-order traversal, task scheduling, rate limiting, producer/consumer buffers.",
        avoid_when="You need the most recent item (stack) or access at both ends (deque).",
        pitfalls=[
            "A naive list-backed queue using pop(0) is O(n) per dequeue, making "
            "BFS O(n^2). Use a head index, a linked list, or a ring buffer.",
            "Using a plain list and never reclaiming the consumed prefix leaks "
            "memory for long-running queues.",
            "BFS must mark a node visited when it is ENQUEUED, not when dequeued, "
            "or nodes get added multiple times.",
        ],
        see_also=["circular_queue", "deque", "stack", "traversals"],
        interview=[
            "Implement Queue using Stacks (LC 232)",
            "Binary Tree Level Order Traversal (LC 102)",
            "Rotting Oranges (LC 994) — multi-source BFS",
            "Number of Islands (LC 200)",
        ],
    ),
    Topic(
        slug="circular_queue",
        name="Circular queue (ring buffer)",
        family="Structures / linear",
        module="Linear.circular_queue",
        entry="CircularQueue",
        doc="docs/circular_queue.md",
        mental_model=(
            "A fixed array where the head and tail indices wrap around with "
            "modulo. Nothing is ever shifted and nothing is ever reallocated, so "
            "both ends are genuinely O(1) in constant memory."
        ),
        invariant="tail == (head + size) % capacity, and the live elements are the `size` slots starting at head.",
        complexity=C("O(1) enqueue", "O(1) dequeue", "O(1) peek", "O(capacity) fixed"),
        use_when="Bounded buffers with fixed memory: audio/video streaming, device drivers, sliding windows, logging.",
        avoid_when="The maximum size is genuinely unknown — a full ring must either reject or overwrite.",
        pitfalls=[
            "head == tail is ambiguous: it means both empty and full. Resolve it "
            "by tracking size explicitly or by leaving one slot permanently "
            "unused. Picking neither is the classic bug.",
            "Every index advance needs the % capacity; one missing modulo breaks "
            "only after the first wrap, so small tests pass.",
            "Overwrite-when-full versus reject-when-full is a product decision, "
            "not a detail — it must be stated in the API.",
        ],
        see_also=["queue", "deque", "my_array"],
        interview=[
            "Design Circular Queue (LC 622)",
            "Design Circular Deque (LC 641)",
            "Design Hit Counter (LC 362)",
            "Moving Average from Data Stream (LC 346)",
        ],
    ),
    Topic(
        slug="deque",
        name="Deque (double-ended queue)",
        family="Structures / linear",
        module="Linear.deque",
        entry="Deque",
        doc="docs/deque.md",
        mental_model=(
            "Push and pop at both ends in O(1). Backed here by a doubly linked "
            "list, so no shifting is ever needed. It is a superset of both stack "
            "and queue, and the engine behind sliding-window maximum."
        ),
        invariant="head.prev is None and tail.next is None; every interior node's links are mutual.",
        complexity=C("O(1) both ends", "O(1) both ends", "O(n) search", "O(n)"),
        use_when="Sliding windows, undo/redo with both histories, work-stealing schedulers, palindrome checks.",
        avoid_when="You index by position — that is O(n) here, O(1) in an array.",
        pitfalls=[
            "Removing the last remaining node must set BOTH head and tail to "
            "None. Updating only one leaves a dangling reference that survives "
            "until the next operation corrupts it.",
            "Each link is two pointers. Setting next without prev creates a "
            "structure that traverses forward correctly and backward wrongly — "
            "so forward-only tests pass.",
            "The monotonic-deque trick stores INDICES, not values, so you can "
            "tell when an element has left the window.",
        ],
        see_also=["doubly_linked_list", "queue", "circular_queue"],
        interview=[
            "Sliding Window Maximum (LC 239)",
            "Design Circular Deque (LC 641)",
            "Shortest Subarray with Sum at Least K (LC 862)",
        ],
    ),
    Topic(
        slug="singly_linked_list",
        name="Singly linked list",
        family="Structures / linear",
        module="Linear.singly_linked_list",
        entry="SinglyLinkedList",
        doc="docs/singly_linked_list.md",
        mental_model=(
            "Nodes scattered in memory, each pointing to the next. O(1) insertion "
            "and deletion *given a pointer to the node*, but O(n) to find it. You "
            "trade random access for cheap structural edits."
        ),
        invariant="Following .next from head reaches every element exactly once and terminates at None.",
        complexity=C("O(1) insert at head", "O(n) search", "O(n) insert at tail (no tail pointer)", "O(n)"),
        use_when="Unknown size with frequent front insertion, hash-table chaining, or when you must not move existing elements.",
        avoid_when="You index by position or iterate hot loops — pointer chasing destroys cache locality.",
        pitfalls=[
            "Deletion needs the PREVIOUS node. Either track it while traversing "
            "or copy the next node's value over the current one.",
            "A dummy head node removes almost every special case around "
            "empty-list and delete-first. Not using one doubles the branch count.",
            "Reversal needs three pointers (prev, curr, next). Two is the most "
            "common interview mistake and loses the rest of the list.",
            "Cycles make length and traversal non-terminating — Floyd's "
            "tortoise-and-hare detects them in O(1) space.",
        ],
        see_also=["doubly_linked_list", "my_array", "hashmap"],
        interview=[
            "Reverse Linked List (LC 206)",
            "Linked List Cycle (LC 141) — Floyd's algorithm",
            "Merge Two Sorted Lists (LC 21)",
            "Remove Nth Node From End (LC 19)",
            "Reorder List (LC 143)",
        ],
    ),
    Topic(
        slug="doubly_linked_list",
        name="Doubly linked list",
        family="Structures / linear",
        module="Linear.doubly_linked_list",
        entry="DoublyLinkedList",
        doc="docs/doubly_linked_list.md",
        mental_model=(
            "Each node points both ways. That extra pointer buys O(1) deletion "
            "given only the node itself — no predecessor search — which is the "
            "property that makes LRU caches work."
        ),
        invariant="For every node n: n.next.prev is n and n.prev.next is n, with None terminating both ends.",
        complexity=C("O(1) insert/delete at either end", "O(n) search", "O(1) delete given node", "O(n) + 2 pointers/node"),
        use_when="Bidirectional traversal, O(1) removal from the middle, LRU caches, browser history, text editors.",
        avoid_when="Memory is tight — two pointers per node is real overhead — or you never traverse backwards.",
        pitfalls=[
            "Every structural edit must fix FOUR pointers. Fixing three leaves a "
            "list that reads correctly in one direction only.",
            "Sentinel head and tail nodes eliminate every null check in "
            "insert/delete. This is the standard professional implementation and "
            "it is strictly simpler than handling the edge cases.",
            "HashMap + doubly linked list is the canonical O(1) LRU cache: the "
            "map finds the node, the list reorders it.",
        ],
        see_also=["singly_linked_list", "deque", "hashmap"],
        interview=[
            "LRU Cache (LC 146) — the canonical use",
            "Flatten a Multilevel Doubly Linked List (LC 430)",
            "Design Browser History (LC 1472)",
        ],
    ),
    # ------------------------------------------------------------- hashing
    Topic(
        slug="hashmap",
        name="Hash map",
        family="Structures / hashing",
        module="Hash.hashmap",
        entry="HashMap",
        doc="docs/hashmap.md",
        mental_model=(
            "Turn a key into an array index with a hash function, then store the "
            "pair there. Collisions are inevitable (pigeonhole principle), so "
            "every bucket holds a small chain. Resize when the load factor gets "
            "high, because chain length is what decides the real cost."
        ),
        invariant="A key is always found in the bucket at hash(key) % capacity, and each key appears at most once overall.",
        complexity=C("O(1)", "O(1) average", "O(n) all-collide", "O(n)"),
        use_when="Membership, counting, de-duplication, memoisation, indexing — the single most useful structure in practice.",
        avoid_when="You need ordered iteration, range queries, or worst-case guarantees (use a balanced tree).",
        pitfalls=[
            "O(1) is average, not worst case. Adversarial keys that all collide "
            "degrade to O(n) — this is a real denial-of-service vector, and why "
            "production hash functions are randomly seeded.",
            "Resizing must REHASH every key: the bucket index depends on "
            "capacity, so copying buckets across is silently wrong.",
            "Mutating a key after insertion makes its entry unreachable. Keys "
            "must be immutable, which is why Python forbids list keys.",
            "Equal keys must hash equally. Overriding __eq__ without __hash__ "
            "breaks the structure's core assumption.",
        ],
        see_also=["hashset", "singly_linked_list", "trie", "counting_sort"],
        interview=[
            "Two Sum (LC 1)",
            "Group Anagrams (LC 49)",
            "LRU Cache (LC 146)",
            "Subarray Sum Equals K (LC 560)",
            "Design HashMap (LC 706)",
        ],
    ),
    Topic(
        slug="hashset",
        name="Hash set",
        family="Structures / hashing",
        module="Hash.hashset",
        entry="HashSet",
        doc="docs/hashset.md",
        mental_model=(
            "A hash map that stores only keys. Answers 'have I seen this?' in "
            "O(1) average. Converting an O(n^2) scan into an O(n) pass by "
            "remembering what you have already seen is one of the highest-value "
            "moves in all of algorithms."
        ),
        invariant="Each distinct value appears at most once; membership is decided by hash bucket plus equality.",
        complexity=C("O(1)", "O(1) average", "O(n) all-collide", "O(n)"),
        use_when="De-duplication, visited-sets in graph traversal, fast membership, set algebra.",
        avoid_when="You need ordering or counts — use a sorted structure or a map to counts.",
        pitfalls=[
            "A visited-set is what stops graph traversal looping forever. "
            "Omitting it is the most common cause of infinite DFS.",
            "Set iteration order is an implementation detail and must never be "
            "relied on for correctness.",
            "Needs the same immutable-key and __eq__/__hash__ consistency rules "
            "as a hash map.",
        ],
        see_also=["hashmap", "undirected_graph", "trie"],
        interview=[
            "Contains Duplicate (LC 217)",
            "Longest Consecutive Sequence (LC 128)",
            "Longest Substring Without Repeating Characters (LC 3)",
            "Happy Number (LC 202)",
        ],
    ),
    # ------------------------------------------------------------- trees
    Topic(
        slug="binary_tree",
        name="Binary tree",
        family="Structures / trees",
        module="Non_Linear.trees.binary_tree",
        entry="BinaryTree",
        doc="docs/binary_tree.md",
        mental_model=(
            "Each node has at most two children and no ordering constraint. "
            "Almost every operation is 'solve it for the left subtree, solve it "
            "for the right subtree, combine'. Recursion is not a technique here, "
            "it is the shape of the data."
        ),
        invariant="Exactly one root; every other node has exactly one parent; no cycles.",
        complexity=C("O(1) root access", "O(n) search", "O(n) most operations", "O(h) recursion"),
        use_when="Hierarchies without ordering: expression trees, decision trees, Huffman coding, file systems.",
        avoid_when="You need ordered lookup (BST) or the heap property (heap). An unordered tree gives neither.",
        pitfalls=[
            "Height versus depth: height is measured from the node down to a "
            "leaf, depth from the root down. Half of all tree bugs are this "
            "confusion.",
            "Recursive solutions use O(h) stack, which is O(n) for a degenerate "
            "tree. Deep trees need an explicit stack.",
            "Level-order insertion (used here) keeps the tree complete; it does "
            "NOT order the values. Do not expect BST behaviour from it.",
            "The empty tree is a valid tree. Base cases must handle None first.",
        ],
        see_also=["bst", "traversals", "min_heap", "binary_tree_lca"],
        interview=[
            "Maximum Depth of Binary Tree (LC 104)",
            "Invert Binary Tree (LC 226)",
            "Diameter of Binary Tree (LC 543)",
            "Binary Tree Maximum Path Sum (LC 124)",
            "Lowest Common Ancestor (LC 236)",
        ],
    ),
    Topic(
        slug="bst",
        name="Binary search tree",
        family="Structures / trees",
        module="Non_Linear.trees.bst",
        entry="BST",
        doc="docs/bst.md",
        mental_model=(
            "A binary tree with an ordering rule: everything in the left subtree "
            "is smaller, everything in the right is larger. That single rule "
            "turns search into a sequence of binary decisions, and makes inorder "
            "traversal emit sorted output for free."
        ),
        invariant=(
            "For every node: max(left subtree) < node.value < min(right subtree). "
            "It is a constraint on entire SUBTREES, not just on direct children."
        ),
        complexity=C("O(log n) balanced", "O(log n) balanced", "O(n) degenerate", "O(h)"),
        use_when="Ordered data with dynamic insert/delete plus range queries, predecessor/successor, or kth-smallest.",
        avoid_when="Insertion order may be sorted and you cannot balance — use a heap, hash map, or AVL/red-black tree.",
        pitfalls=[
            "Validating a BST by comparing each node only to its children is "
            "WRONG. The constraint spans subtrees, so you must carry min/max "
            "bounds down the recursion.",
            "Inserting sorted data builds a linked list: O(n) operations and O(n) "
            "stack depth. This is the motivation for every self-balancing tree.",
            "Deleting a node with two children requires replacing it with its "
            "inorder successor (or predecessor) — not with either child.",
            "Inorder traversal yields sorted order. Many 'hard' BST problems are "
            "one-line once you see that.",
        ],
        see_also=["binary_tree", "traversals", "tree_sort", "trie"],
        interview=[
            "Validate Binary Search Tree (LC 98)",
            "Kth Smallest Element in a BST (LC 230)",
            "Lowest Common Ancestor of a BST (LC 235)",
            "Convert Sorted Array to BST (LC 108)",
            "Delete Node in a BST (LC 450)",
        ],
    ),
    Topic(
        slug="traversals",
        name="Tree traversals",
        family="Structures / trees",
        module="Non_Linear.trees.traversals",
        entry="TreeTraversals",
        mental_model=(
            "Four orders, each suited to a different job. Preorder (root first) "
            "copies or serialises. Inorder (root in the middle) sorts a BST. "
            "Postorder (root last) frees or evaluates bottom-up. Level-order "
            "(breadth-first) measures distance from the root."
        ),
        invariant="Every node is visited exactly once; the order is fixed by where the root is processed relative to its subtrees.",
        complexity=C("O(n)", "O(n)", "O(n)", "O(h) DFS / O(w) BFS"),
        use_when="Choose by what you need: inorder for sorted output, postorder for bottom-up aggregation, level-order for depth.",
        avoid_when="Never — but picking the wrong order turns an easy problem into a hard one.",
        pitfalls=[
            "Postorder is required whenever a node's answer depends on its "
            "children's answers (height, diameter, subtree sums). Using preorder "
            "there forces redundant recomputation.",
            "DFS uses O(h) space, BFS uses O(w) where w is the widest level. For "
            "a balanced tree that is O(log n) versus O(n) — BFS is the expensive "
            "one, which surprises people.",
            "Iterative inorder needs an explicit stack and a 'go left as far as "
            "possible' loop. Morris traversal does it in O(1) space by "
            "temporarily rewiring the tree.",
        ],
        see_also=["binary_tree", "bst", "stack", "queue", "undirected_graph"],
        interview=[
            "Binary Tree Inorder Traversal (LC 94) — iterative",
            "Binary Tree Level Order Traversal (LC 102)",
            "Serialize and Deserialize Binary Tree (LC 297)",
            "Construct Tree from Preorder and Inorder (LC 105)",
        ],
    ),
    Topic(
        slug="binary_tree_lca",
        name="Lowest common ancestor",
        family="Structures / trees",
        module="Non_Linear.trees.binary_tree",
        entry="BinaryTree.lowest_common_ancestor",
        doc="docs/binary_tree_lca.md",
        mental_model=(
            "The deepest node that has both targets in its subtree. Recurse down; "
            "if one target comes back from the left and the other from the right, "
            "the current node is the answer. If both come from the same side, "
            "bubble that result up."
        ),
        invariant="A node is the LCA exactly when both targets lie in its subtree but not together in any single child's subtree.",
        complexity=C("O(1)", "O(n)", "O(n)", "O(h)"),
        use_when="Tree distance, path-between-two-nodes, version-control merge bases, taxonomy queries.",
        avoid_when="Repeated queries on a static tree — then preprocess with binary lifting or Euler tour + sparse table for O(log n) or O(1) per query.",
        pitfalls=[
            "'Lower' means deeper, farther from the root. The naming inverts most "
            "people's intuition and is the usual source of off-by-one-level "
            "answers.",
            "The standard solution assumes both targets EXIST. If one may be "
            "absent you must verify presence or you return a wrong ancestor "
            "confidently.",
            "In a BST you do not need this algorithm: walk down while both "
            "targets are on the same side and stop when they split. O(h) with no "
            "recursion needed.",
        ],
        see_also=["binary_tree", "bst", "traversals"],
        interview=[
            "Lowest Common Ancestor of a Binary Tree (LC 236)",
            "LCA of a BST (LC 235)",
            "LCA with parent pointers (LC 1650)",
        ],
    ),
    # ------------------------------------------------------------- heaps
    Topic(
        slug="min_heap",
        name="Min heap",
        family="Structures / heaps",
        module="Non_Linear.heaps.min_heap",
        entry="MinHeap",
        doc="docs/heaps.md",
        mental_model=(
            "A complete binary tree flattened into an array, where every parent is "
            "<= its children. That weaker-than-BST ordering is exactly enough to "
            "keep the minimum at index 0, and weak enough to maintain in "
            "O(log n) with no pointers at all."
        ),
        invariant="For every index i > 0: data[(i-1)//2] <= data[i]. Children of i are 2i+1 and 2i+2.",
        complexity=C("O(1) peek min", "O(log n) insert/extract", "O(log n)", "O(n)"),
        use_when="Priority queues, kth-smallest, merging k sorted streams, Dijkstra, A*, scheduling, streaming medians.",
        avoid_when="You need sorted iteration or arbitrary search — a heap gives you the extremum and nothing else cheaply.",
        pitfalls=[
            "A heap is NOT sorted. Only index 0 is guaranteed. Printing the "
            "backing array and expecting order is the classic misconception.",
            "Heapifying an existing array bottom-up is O(n); inserting n items "
            "one at a time is O(n log n). Do not confuse the two.",
            "Child indices are 2i+1 / 2i+2 for 0-based arrays and 2i / 2i+1 for "
            "1-based. Mixing them corrupts the heap without raising.",
            "For kth LARGEST keep a min-heap of size k (not a max-heap of "
            "everything) — that is O(n log k) space-bounded.",
        ],
        see_also=["max_heap", "heap_sort", "cartesian_tree_sort", "astar", "external_merge_sort"],
        interview=[
            "Kth Largest Element in an Array (LC 215)",
            "Merge k Sorted Lists (LC 23)",
            "Find Median from Data Stream (LC 295) — two heaps",
            "Task Scheduler (LC 621)",
            "K Closest Points to Origin (LC 973)",
        ],
    ),
    Topic(
        slug="max_heap",
        name="Max heap",
        family="Structures / heaps",
        module="Non_Linear.heaps.max_heap",
        entry="MaxHeap",
        doc="docs/heaps.md",
        mental_model=(
            "The mirror image of a min heap: every parent is >= its children, so "
            "the maximum sits at index 0. The engine inside heap sort, and the "
            "half of a two-heap median tracker that holds the lower values."
        ),
        invariant="For every index i > 0: data[(i-1)//2] >= data[i].",
        complexity=C("O(1) peek max", "O(log n) insert/extract", "O(log n)", "O(n)"),
        use_when="Largest-first priority, heap sort, bounded 'k smallest' (max-heap of size k), median maintenance.",
        avoid_when="Same as min heap — no ordered iteration, no cheap arbitrary search.",
        pitfalls=[
            "Python's heapq is min-only. The standard trick is to push negated "
            "values, which breaks on non-numeric keys and is easy to forget to "
            "undo on pop.",
            "replace() (pop-then-push in one sift) is cheaper than separate "
            "extract and insert — one O(log n) pass instead of two.",
            "Same 0-based versus 1-based child index trap as the min heap.",
        ],
        see_also=["min_heap", "heap_sort", "selection_sort"],
        interview=[
            "Last Stone Weight (LC 1046)",
            "Find Median from Data Stream (LC 295)",
            "K Closest Points to Origin (LC 973) — max-heap of size k",
        ],
    ),
    # -------------------------------------------------------------- tries
    Topic(
        slug="trie",
        name="Trie (prefix tree)",
        family="Structures / tries",
        module="Non_Linear.trie.trie",
        entry="Trie",
        doc="docs/trie.md",
        mental_model=(
            "One node per character, so a shared prefix is stored exactly once. "
            "Lookup cost depends on the length of the key, not on how many keys "
            "are stored — and unlike a hash map, the structure itself answers "
            "prefix questions."
        ),
        invariant="The path from the root to a node spells that node's prefix; a terminal flag marks where a complete word ends.",
        complexity=C("O(m) insert", "O(m) search", "O(m) prefix query", "O(total characters * alphabet)"),
        use_when="Autocomplete, spell-check, IP routing tables, word games, any 'all strings starting with…' query.",
        avoid_when="Exact-match only — a hash map is smaller and faster. Tries trade memory for prefix power.",
        pitfalls=[
            "A terminal flag is mandatory. Without it 'car' cannot be "
            "distinguished from a prefix of 'card', so search returns true for "
            "words never inserted.",
            "Deletion must only remove nodes with no remaining children and no "
            "terminal flag, walking back up. Deleting the whole path destroys "
            "other words.",
            "Memory is the real cost: a dict per node is flexible but heavy. "
            "Radix/compressed tries collapse single-child chains.",
            "The empty string is a valid key — it marks the root as terminal.",
        ],
        see_also=["hashmap", "bst", "radix_sort", "sublist_search"],
        interview=[
            "Implement Trie (LC 208)",
            "Word Search II (LC 212) — trie + backtracking",
            "Design Add and Search Words (LC 211)",
            "Longest Common Prefix (LC 14)",
            "Replace Words (LC 648)",
        ],
    ),
    # ------------------------------------------------------- disjoint set
    Topic(
        slug="disjoint_set",
        name="Disjoint set (union-find)",
        family="Structures / disjoint set",
        module="Non_Linear.disjoint_set.disjoint_set_base",
        entry="DisjointSet",
        also_covers=["Non_Linear.disjoint_set.disjoint_set_algorithms"],
        mental_model=(
            "Track which elements are in the same group, supporting only two "
            "questions: 'same group?' and 'merge these groups'. Each group is a "
            "tree whose root names it. Two optimisations — path compression and "
            "union by rank — flatten those trees until the cost is "
            "indistinguishable from constant."
        ),
        invariant="Every element points toward its set's root; find() returns that root and the root points to itself.",
        complexity=C("O(1)", "O(alpha(n)) ~ O(1) amortised", "O(log n) without optimisations", "O(n)"),
        use_when="Connectivity under incremental edge addition, Kruskal's MST, cycle detection in undirected graphs, grid percolation.",
        avoid_when="You need to DELETE edges or split sets — union-find is merge-only by design.",
        pitfalls=[
            "Without BOTH path compression and union by rank the trees can become "
            "chains and find() degrades to O(n). Either alone gives O(log n); "
            "together they give near-constant.",
            "Union must link ROOT to ROOT. Linking the passed-in elements instead "
            "silently creates a structure where find() still works but the depth "
            "bound is lost.",
            "It cannot answer 'are these in different groups *as of step k*' — "
            "there is no history. Offline reverse processing is the usual trick.",
            "Cycle detection only works for UNDIRECTED graphs. Directed cycles "
            "need DFS colouring or Kahn's algorithm.",
        ],
        see_also=["undirected_weighted_graph", "hashset", "undirected_graph"],
        interview=[
            "Number of Connected Components (LC 323)",
            "Redundant Connection (LC 684)",
            "Accounts Merge (LC 721)",
            "Number of Islands II (LC 305)",
            "Satisfiability of Equality Equations (LC 990)",
        ],
    ),
    # ------------------------------------------------------------- graphs
    Topic(
        slug="undirected_graph",
        name="Undirected graph",
        family="Structures / graphs",
        module="Non_Linear.graphs.undirected.undirected_graph_base",
        entry="Graph",
        doc="docs/undirected_graph.md",
        also_covers=[
            "Non_Linear.graphs.undirected.undirected_graph_algorithms",
            "Non_Linear.graphs.undirected.undirected_graph_utils",
        ],
        mental_model=(
            "Vertices joined by symmetric edges — if a connects to b then b "
            "connects to a. Stored as an adjacency list. BFS gives shortest paths "
            "in edge count; DFS reveals structure (cycles, bridges, articulation "
            "points)."
        ),
        invariant="Edge membership is symmetric: v in adj[u] if and only if u in adj[v].",
        complexity=C("O(1) add edge", "O(V + E) traversal", "O(V + E) traversal", "O(V + E)"),
        use_when="Social networks, road maps, mesh topologies, mutual relationships, grid connectivity.",
        avoid_when="Relationships are one-way — use a directed graph; the symmetry assumption silently produces wrong answers.",
        pitfalls=[
            "Adding an edge means updating BOTH adjacency lists. Updating one "
            "gives a directed graph that behaves undirected only for some "
            "queries.",
            "Undirected cycle detection via DFS must ignore the edge you arrived "
            "on, or every single edge looks like a 2-cycle.",
            "An adjacency MATRIX is O(V^2) space regardless of edge count — fine "
            "for dense graphs, wasteful for sparse ones. The representation "
            "choice is the first design decision.",
            "Bridges and articulation points both come from Tarjan's low-link "
            "values; the difference between them is one comparison (<= versus <).",
        ],
        see_also=["undirected_weighted_graph", "directed_graph", "disjoint_set", "queue", "traversals"],
        interview=[
            "Number of Islands (LC 200)",
            "Clone Graph (LC 133)",
            "Is Graph Bipartite? (LC 785)",
            "Critical Connections / bridges (LC 1192)",
            "Word Ladder (LC 127) — BFS shortest path",
        ],
    ),
    Topic(
        slug="directed_graph",
        name="Directed graph",
        family="Structures / graphs",
        module="Non_Linear.graphs.directed.directed_graph",
        entry="DirectedGraph",
        doc="docs/directed_graph.md",
        mental_model=(
            "Edges have direction, so reachability is asymmetric. This unlocks "
            "dependency questions: topological ordering needs acyclicity, and "
            "strong connectivity means mutual reachability rather than mere "
            "connection."
        ),
        invariant="v in adj[u] means an edge u -> v exists; it implies nothing about u in adj[v].",
        complexity=C("O(1) add edge", "O(V + E) traversal", "O(V + E) traversal", "O(V + E)"),
        use_when="Dependencies, build systems, task scheduling, state machines, web links, data-flow graphs.",
        avoid_when="The relation is genuinely symmetric — storing both directions doubles the work and invites inconsistency.",
        pitfalls=[
            "Directed cycle detection needs THREE colours (white/grey/black) or a "
            "recursion-stack set. A plain visited set finds false cycles on any "
            "diamond-shaped DAG.",
            "Topological sort exists only for a DAG. Running it on a cyclic graph "
            "returns a partial order with no error unless you check the output "
            "length against V.",
            "In-degree and out-degree are different questions and Kahn's "
            "algorithm needs in-degree specifically.",
            "Strongly connected is not the same as connected. Kosaraju and "
            "Tarjan compute SCCs; the transpose graph is central to Kosaraju.",
        ],
        see_also=["directed_weighted_graph", "undirected_graph", "traversals", "disjoint_set"],
        interview=[
            "Course Schedule (LC 207) — cycle detection",
            "Course Schedule II (LC 210) — topological sort",
            "Alien Dictionary (LC 269)",
            "Find Eventual Safe States (LC 802)",
        ],
    ),
    Topic(
        slug="undirected_weighted_graph",
        name="Undirected weighted graph",
        family="Structures / graphs",
        module="Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_base",
        entry="UndirectedWeightedGraph",
        also_covers=[
            "Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_algorithms",
            "Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_advanced",
            "Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_matrix",
            "Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_mst",
            "Non_Linear.graphs.undirected.weighted.undirected_weighted_graph_utils",
        ],
        mental_model=(
            "Edges carry costs, so 'shortest' stops meaning 'fewest edges' and BFS "
            "stops working. Dijkstra with a priority queue replaces it. The other "
            "headline problem here is the minimum spanning tree: connect "
            "everything as cheaply as possible."
        ),
        invariant="Weights are symmetric: weight(u, v) == weight(v, u). An MST has exactly V-1 edges and no cycle.",
        complexity=C("O(1) add edge", "Dijkstra O((V+E) log V)", "Floyd-Warshall O(V^3)", "O(V + E)"),
        use_when="Road networks with distances, network design, clustering, circuit layout.",
        avoid_when="All weights are equal — then BFS is simpler and faster than Dijkstra.",
        pitfalls=[
            "Dijkstra is WRONG with negative weights — it finalises a node on "
            "first pop and never revisits. Bellman-Ford handles negatives and "
            "detects negative cycles.",
            "Kruskal sorts edges and uses union-find; Prim grows one tree with a "
            "priority queue. Kruskal suits sparse graphs, Prim dense ones.",
            "MST is not the same as shortest paths. The MST path between two "
            "nodes is frequently not the shortest path between them.",
            "With equal weights Dijkstra still works but wastes a heap — the "
            "interview answer is 'use BFS'.",
        ],
        see_also=["directed_weighted_graph", "disjoint_set", "min_heap", "astar", "undirected_graph"],
        interview=[
            "Min Cost to Connect All Points (LC 1584) — MST",
            "Network Delay Time (LC 743) — Dijkstra",
            "Path With Minimum Effort (LC 1631)",
            "Swim in Rising Water (LC 778)",
        ],
    ),
    Topic(
        slug="directed_weighted_graph",
        name="Directed weighted graph",
        family="Structures / graphs",
        module="Non_Linear.graphs.directed.weighted.directed_weighted_graph_base",
        entry="DirectedWeightedGraph",
        also_covers=[
            "Non_Linear.graphs.directed.weighted.directed_weighted_graph_algorithms",
            "Non_Linear.graphs.directed.weighted.directed_weighted_graph_advanced",
            "Non_Linear.graphs.directed.weighted.directed_weighted_graph_matrix",
            "Non_Linear.graphs.directed.weighted.directed_weighted_graph_utils",
        ],
        mental_model=(
            "Direction plus cost. This is the most general of the four graph "
            "shapes and where the heavyweight algorithms live: Bellman-Ford for "
            "negative edges, Floyd-Warshall for all-pairs, DAG relaxation in "
            "topological order, and max-flow."
        ),
        invariant="weight(u, v) is independent of weight(v, u). Relaxation: dist[v] <= dist[u] + weight(u, v) holds at termination.",
        complexity=C("O(1) add edge", "Bellman-Ford O(VE)", "Floyd-Warshall O(V^3)", "O(V + E)"),
        use_when="Currency arbitrage, one-way road networks with tolls, flow networks, PERT/critical-path scheduling.",
        avoid_when="Edges are symmetric — the undirected form halves the storage and the bookkeeping.",
        pitfalls=[
            "A negative CYCLE means no shortest path exists (you can loop "
            "forever). Bellman-Ford's extra Vth pass is what detects it — "
            "skipping that pass returns nonsense confidently.",
            "On a DAG, relaxing edges in topological order gives shortest paths "
            "in O(V+E), beating Dijkstra and tolerating negative weights.",
            "Floyd-Warshall's loop order must be k (intermediate) OUTERMOST. Any "
            "other nesting computes something that is not all-pairs shortest "
            "paths.",
            "Max-flow needs the RESIDUAL graph including backward edges; "
            "forgetting them makes Ford-Fulkerson stop at a non-maximal flow.",
        ],
        see_also=["undirected_weighted_graph", "directed_graph", "min_heap", "astar"],
        interview=[
            "Cheapest Flights Within K Stops (LC 787) — Bellman-Ford",
            "Network Delay Time (LC 743)",
            "Find the City With the Smallest Number of Neighbors (LC 1334) — Floyd-Warshall",
            "Maximum Flow / bipartite matching",
        ],
    ),
]
