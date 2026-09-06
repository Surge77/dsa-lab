# 📚 Doubly Linked List — Python Implementation

A **Doubly Linked List** is a linear data structure where each node points both **forward** and **backward**, enabling efficient two-way traversal.

This implementation is part of the `dsa-lab` project and focuses on clean code, performance, and interview-readiness.

---

## 📌 Features

- Two-way navigation (`next` and `prev`)
- Constant-time insertion/removal at head or tail
- Optimized indexing from head/tail
- Full support for list-like operations

---

## 🧱 Node Structure

Each node stores:
- `value`: The actual data
- `next`: Pointer to the next node
- `prev`: Pointer to the previous node

---

## ✅ Supported Operations

| Method            | Description                                | Time Complexity |
|-------------------|--------------------------------------------|-----------------|
| `append(value)`   | Add to end                                  | O(1)            |
| `prepend(value)`  | Add to front                                | O(1)            |
| `insert(index, v)`| Insert at specific index                    | O(n)            |
| `delete(index)`   | Remove node at index                        | O(n)            |
| `get(index)`      | Get value at index                          | O(n)            |
| `set(index, v)`   | Update value at index                       | O(n)            |
| `search(value)`   | Find first index of value                  | O(n)            |
| `reverse()`       | Reverse list in place                       | O(n)            |
| `__len__()`       | Get number of elements                      | O(1)            |
| `__str__()`       | Human-readable representation               | O(n)            |
| `__repr__()`      | Developer representation                    | O(n)            |

---

## 🧪 Example Usage

```python
dll = DoublyLinkedList()
dll.append("a")
dll.append("b")
dll.prepend("start")
dll.insert(2, "x")
print(dll)        # start <-> a <-> x <-> b <-> None

dll.delete(1)
print(dll.get(1)) # x
print(len(dll))   # 3

dll.reverse()
print(dll)        # b <-> x <-> start <-> None
