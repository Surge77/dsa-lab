# 🌳 Binary Tree Implementation 

This module provides a full implementation of a **Binary Tree** from scratch in Python, without using built-in data structures beyond lists. It's part of the `dsa-lab` project under `non_linear/trees/`.

---

## 📦 File: `binary_tree.py`

### 🔹 Classes

---

### `class Node`
Represents a single node in the binary tree.

#### Attributes:
- `value (int)`: Value stored at the node.
- `left (Node)`: Reference to the left child.
- `right (Node)`: Reference to the right child.

---

### `class BinaryTree`
Encapsulates the tree and provides all core operations.

---

## 🔹 Methods

### ✅ `insert(value: int) -> None`
Inserts a node using **level-order** (BFS-like) strategy to keep tree balanced.
- ⏱ Time: O(n)
- 💾 Space: O(n)

---

### ✅ `level_order_traversal() -> list[int]`
Returns a list of node values in **level-order** (BFS).
- ⏱ Time: O(n)
- 💾 Space: O(n)

---

### ✅ `inorder() -> list[int]`
Returns **inorder traversal** (Left → Root → Right).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `preorder() -> list[int]`
Returns **preorder traversal** (Root → Left → Right).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `postorder() -> list[int]`
Returns **postorder traversal** (Left → Right → Root).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `search(target: int) -> bool`
Performs level-order search for a node with the given value.
- ⏱ Time: O(n)
- 💾 Space: O(n)

---

### ✅ `height() -> int`
Calculates the **height** (depth) of the binary tree.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `count_leaf_nodes() -> int`
Counts total **leaf nodes** (nodes with no children).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `delete(target: int) -> bool`
Deletes a node by replacing it with the **deepest rightmost node**.
- ⏱ Time: O(n)
- 💾 Space: O(n)

---

### ✅ `diameter() -> int`
Computes the **longest path** (in number of nodes) between any two nodes.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `mirror() -> None`
Modifies the tree to be its **mirror image**, in-place.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `is_symmetric() -> bool`
Checks if the tree is **symmetric** (mirror around center).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `lowest_common_ancestor(p_val: int, q_val: int) -> int`
Finds the **lowest common ancestor** of two nodes.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `path_to_node(target: int) -> list[int]`
Returns the **path** from root to a node (if exists).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `max_path_sum() -> int`
Finds the **maximum path sum** (any node to any node).
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `max_root_to_leaf_sum() -> int`
Finds the **maximum sum** from root to any leaf.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `min_root_to_leaf_sum() -> int`
Finds the **minimum sum** from root to any leaf.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---

### ✅ `min_root_to_leaf_path() -> list[int]`
Returns the actual **minimum path (values)** from root to leaf.
- ⏱ Time: O(n)
- 💾 Space: O(h)

---


## 🧪 Test File

Use `Tests/test_binary_tree.py` with `unittest`:
```bash
python -m unittest Tests.test_binary_tree
```

Or discover all:
```bash
python -m unittest discover -s Tests
```

---

