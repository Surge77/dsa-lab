import unittest

from Linear.deque import Deque


class TestDeque(unittest.TestCase):

    def setUp(self):
        self.dq = Deque()

    def test_append_and_peek(self):
        self.dq.append_left("a")
        self.dq.append_right("b")
        self.assertEqual(self.dq.peek_left(), "a")
        self.assertEqual(self.dq.peek_right(), "b")

    def test_pop_operations(self):
        self.dq.append_right(1)
        self.dq.append_right(2)
        self.dq.append_right(3)

        self.assertEqual(self.dq.pop_left(), 1)
        self.assertEqual(self.dq.pop_right(), 3)
        self.assertEqual(self.dq.pop_left(), 2)

        self.assertTrue(self.dq.is_empty())

    def test_len_and_empty(self):
        self.assertEqual(len(self.dq), 0)
        self.assertTrue(self.dq.is_empty())

        self.dq.append_left(10)
        self.assertEqual(len(self.dq), 1)
        self.assertFalse(self.dq.is_empty())

    def test_str_output(self):
        self.dq.append_left(3)
        self.dq.append_left(2)
        self.dq.append_left(1)
        self.assertEqual(str(self.dq), "Front → [1, 2, 3] ← Rear")

    def test_exceptions(self):
        with self.assertRaises(IndexError):
            self.dq.pop_left()
        with self.assertRaises(IndexError):
            self.dq.pop_right()
        with self.assertRaises(IndexError):
            self.dq.peek_left()
        with self.assertRaises(IndexError):
            self.dq.peek_right()

if __name__ == "__main__":
    unittest.main()
