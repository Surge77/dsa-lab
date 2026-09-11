import unittest

from Linear.stack import Stack


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_push_and_len(self):
        self.assertEqual(len(self.stack), 0)
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(len(self.stack), 2)

    def test_pop(self):
        self.stack.push("a")
        self.stack.push("b")
        self.assertEqual(self.stack.pop(), "b")
        self.assertEqual(self.stack.pop(), "a")
        self.assertTrue(self.stack.is_empty())
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.peek(), 20)
        self.stack.pop()
        self.assertEqual(self.stack.peek(), 10)
        self.stack.pop()
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_str(self):
        self.assertEqual(str(self.stack), "Bottom → [] ← Top")
        self.stack.push("x")
        self.stack.push("y")
        self.assertEqual(str(self.stack), "Bottom → ['x', 'y'] ← Top")


if __name__ == "__main__":
    unittest.main()
