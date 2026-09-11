# Binary search tree

Implementation: `Non_Linear/trees/bst.py` · Tests: `Tests/test_bst.py`

A binary tree plus one rule. That rule turns search into a sequence of binary
decisions and makes sorted output fall out of a traversal for free.

---

## The invariant — and the way people get it wrong

```
for every node:   max(left subtree) < node.value < min(right subtree)
```

Read that again: it constrains entire **subtrees**, not just direct children.

This is the single most common BST bug. The following tree passes a
"compare each node to its two children" check and is **not** a BST:

```
        10
       /  \
      5    15
          /  \
         6    20      <- 6 < 15 locally, but 6 < 10 so it must be LEFT of 10
```

Validating correctly means carrying bounds down the recursion:

```python
def is_bst(node, low=-inf, high=+inf):
    if node is None:
        return True
    if not (low < node.value < high):
        return False
    return is_bst(node.left, low, node.value) and is_bst(node.right, node.value, high)
```

That is LeetCode 98, and the bounds are the whole answer.

---

## Complexity depends entirely on shape

| | Balanced | Degenerate |
|---|---|---|
| search / insert / delete | O(log n) | O(n) |
| space (recursion) | O(log n) | O(n) |

Inserting **sorted** data produces the degenerate case: every value goes right,
and the tree is a linked list with extra pointers.

```
insert 1,2,3,4,5   ->   1
                         \
                          2
                           \
                            3
                             \
                              4
                               \
                                5
```

That is both O(n) per operation *and* O(n) recursion depth — a stack overflow,
not just slowness. It is the entire motivation for AVL trees, red-black trees,
and treaps.

---

## Inorder traversal is the superpower

An inorder walk of a BST emits values in sorted order. Many "hard" BST problems
collapse once you see that:

- **Kth smallest** (LC 230) — inorder, stop at k. No need to traverse the rest.
- **Validate BST** — inorder must be strictly increasing.
- **Two Sum in a BST** — inorder into a list, then two pointers.
- **BST to sorted list** — inorder, done.

This is also why tree sort works: insert everything, walk inorder. See
`Sorting/tree_based/tree_sort.py`.

---

## Deletion: three cases

| Children | Action |
|---|---|
| none | remove the node |
| one | replace the node with that child |
| two | replace the value with the **inorder successor**, then delete the successor |

The two-child case is where people go wrong by promoting a child directly —
that breaks the ordering. The inorder successor (smallest value in the right
subtree) is the only value that can sit in that slot and keep the invariant, and
it is guaranteed to have at most one child itself, so the recursion terminates.

The inorder predecessor works equally well; pick one and be consistent.

---

## Predecessor and successor without a traversal

Walk down from the root tracking the best candidate seen so far:

- **successor of x**: go left when `node.value > x` (recording the node), right
  otherwise
- **predecessor of x**: mirror image

O(h), no recursion, no extra space. The same descending-walk shape answers
lowest common ancestor in a BST: walk down while both targets are on the same
side, and stop the moment they split.

---

## When to reach for a BST

Over a hash map when you need **order**: range queries, kth smallest,
predecessor/successor, sorted iteration. A hash map gives you none of those.

Over a sorted array when the data **changes**: insertion into a sorted array is
O(n); into a balanced BST it is O(log n).

Over a heap when you need more than the extremum. A heap gives you the min or
max cheaply and nothing else.

Avoid it when insertion order may be sorted and you cannot balance — that is the
degenerate case above.

---

## Interview problems

- Validate Binary Search Tree (LC 98) — the bounds technique
- Kth Smallest Element in a BST (LC 230)
- Lowest Common Ancestor of a BST (LC 235) — the descending walk
- Convert Sorted Array to BST (LC 108) — build balanced by taking the midpoint
- Delete Node in a BST (LC 450) — the three cases
- Insert into a BST (LC 701)

Related: [binary_tree.md](binary_tree.md) · [trie.md](trie.md) ·
[heaps.md](heaps.md)

Drill it: `python drill.py --topic bst`
