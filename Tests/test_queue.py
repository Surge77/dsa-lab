import unittest

from Linear.queue import Queue


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.q = Queue()

    def test_enqueue_and_len(self):
        self.assertEqual(len(self.q), 0)
        self.q.enqueue(1)
        self.q.enqueue(2)
        self.assertEqual(len(self.q), 2)
        self.assertEqual(str(self.q), "Front → [1, 2] ← Rear")

    def test_dequeue(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.assertEqual(self.q.dequeue(), "a")
        self.assertEqual(self.q.dequeue(), "b")
        self.assertTrue(self.q.is_empty())
        with self.assertRaises(IndexError):
            self.q.dequeue()

    def test_peek(self):
        self.q.enqueue("x")
        self.q.enqueue("y")
        self.assertEqual(self.q.peek(), "x")
        self.q.dequeue()
        self.assertEqual(self.q.peek(), "y")
        self.q.dequeue()
        with self.assertRaises(IndexError):
            self.q.peek()

    def test_is_empty(self):
        self.assertTrue(self.q.is_empty())
        self.q.enqueue(99)
        self.assertFalse(self.q.is_empty())
        self.q.dequeue()
        self.assertTrue(self.q.is_empty())

    def test_str(self):
        self.assertEqual(str(self.q), "Front → [] ← Rear")
        self.q.enqueue("first")
        self.q.enqueue("second")
        self.assertEqual(str(self.q), "Front → ['first', 'second'] ← Rear")


if __name__ == "__main__":
    unittest.main()
