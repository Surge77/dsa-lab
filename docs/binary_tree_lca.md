## Lowest common ancestor

### Goal:

Given a binary tree and two node values p_val and q_val, find the lowest (deepest i.e closer to the leaves), node in the tree that is an ancestor of both nodes.

LCA in simple words:

- The node must be an ancestor of both p and q

- Among all such ancestors, we want the one closest to the leaves

- Which also means it's farthest from the root

## 🪓 First Principles Breakdown

## ✅ Principle 1: A node is an ancestor if both p and q exist in its subtree.

A node is an ancestor of p and q if:

One is found in its left subtree and the other in the right, or

The node itself is p or q, and the other exists in one of its subtrees.

## ✅ Principle 2: Recursive Tree Traversal is optimal

Binary trees are naturally recursive structures.

We can recursively search both subtrees to find p and q.

## ✅ Principle 3: Decision logic at each node

At every node:

If the node is None, return None (base case).

If the node’s value is p_val or q_val, return this node.

Otherwise:

Recurse on left and right subtrees.

If both sides return non-None, current node is LCA.

If one side is non-None, bubble it up.

### Term Used	Meaning in LCA Trees

- "Lower" means	Deeper in the tree (farther from root)
- "Higher" means	Closer to the root