# 🧱 Stack — Python Implementation

A **Stack** is a linear data structure that follows the **LIFO** principle — **Last In, First Out**. The last element added is the first one to be removed.

This implementation is part of the `dsa-lab` project and emphasizes clean design, performance, and interview-readiness.

---

## 📌 Features

- Built on top of Python's dynamic array (`list`)
- Constant time operations for `push`, `pop`, `peek`, and `is_empty`
- Fully unit-tested with `unittest`
- Clean string representation via `__str__()`

---

## ✅ Supported Operations

| Method        | Description                                 | Time Complexity |
|---------------|---------------------------------------------|-----------------|
| `push(value)` | Add item to the top                         | O(1)            |
| `pop()`       | Remove and return top item                  | O(1)            |
| `peek()`      | View top item without removing              | O(1)            |
| `is_empty()`  | Check whether stack is empty                | O(1)            |
| `__len__()`   | Return the number of elements               | O(1)            |
| `__str__()`   | Print stack from bottom → top               | O(n)            |

---

## 🧪 Example Usage

```python
s = Stack()
s.push("a")
s.push("b")
s.push("c")

print(s)        # Bottom → ['a', 'b', 'c'] ← Top
print(s.pop())  # c
print(s.peek()) # b
print(len(s))   # 2
print(s.is_empty())  # False
