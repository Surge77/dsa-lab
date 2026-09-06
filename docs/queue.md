# 📦 Queue — Python Implementation (Scratch)

A **Queue** is a linear data structure that follows the **FIFO** principle — *First In, First Out*.  
It’s used where order matters, and the first element added should be the first one processed.

This implementation is written **from scratch using Python lists**, as part of the `dsa-lab` learning project.

---

## 🧠 Key Concepts

- **FIFO**: Items are added at the **rear** and removed from the **front**
- **Use Cases**: Scheduling, buffering, BFS (Breadth-First Search), etc.
- **Limitation**: `dequeue()` is `O(n)` due to list shifting — can be optimized later

---

## ✅ Supported Operations

| Method          | Description                              | Time Complexity |
|------------------|------------------------------------------|-----------------|
| `enqueue(value)` | Add element to the **rear**              | O(1) amortized  |
| `dequeue()`      | Remove and return element from **front** | O(n) ⚠️         |
| `peek()`         | View element at the **front**            | O(1)            |
| `is_empty()`     | Check whether the queue is empty         | O(1)            |
| `__len__()`      | Return number of elements in queue       | O(1)            |
| `__str__()`      | Print the queue (front → rear)           | O(n)            |

---

## 🧪 Example Usage

```python
from Linear.queue import Queue

q = Queue()
q.enqueue(10)
q.enqueue(20)
q.enqueue(30)

print(q)         # Front → [10, 20, 30] ← Rear
print(q.peek())  # 10
print(q.dequeue())  # 10
print(len(q))    # 2
print(q.is_empty())  # False
