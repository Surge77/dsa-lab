import unittest

from Linear.circular_queue import CircularQueue


class TestCircularQueue(unittest.TestCase):

    def setUp(self):
        self.q = CircularQueue(3)

    def test_enqueue_and_str(self):
        self.q.enqueue(1)
        self.q.enqueue(2)
        self.assertEqual(str(self.q), "Front → [1, 2] ← Rear")

    def test_dequeue_and_peek(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.assertEqual(self.q.peek(), "a")
        self.assertEqual(self.q.dequeue(), "a")
        self.assertEqual(self.q.dequeue(), "b")
        self.assertTrue(self.q.is_empty())

    def test_wrap_around_behavior(self):
        self.q.enqueue(10)
        self.q.enqueue(20)
        self.q.enqueue(30)
        self.q.dequeue()
        self.q.enqueue(40)  # This should wrap rear
        self.assertEqual(str(self.q), "Front → [20, 30, 40] ← Rear")

    def test_is_full(self):
        self.q.enqueue("x")
        self.q.enqueue("y")
        self.q.enqueue("z")
        self.assertTrue(self.q.is_full())

    def test_len(self):
        self.assertEqual(len(self.q), 0)
        self.q.enqueue(99)
        self.assertEqual(len(self.q), 1)

    def test_errors(self):
        with self.assertRaises(IndexError):
            self.q.dequeue()
        with self.assertRaises(IndexError):
            self.q.peek()
        self.q.enqueue(1)
        self.q.enqueue(2)
        self.q.enqueue(3)
        with self.assertRaises(OverflowError):
            self.q.enqueue(4)


if __name__ == "__main__":
    unittest.main()
