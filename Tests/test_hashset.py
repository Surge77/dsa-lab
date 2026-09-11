import unittest

from Hash.hashset import HashSet


class TestHashSet(unittest.TestCase):

    def setUp(self):
        self.hs = HashSet()

    def test_add_and_len(self):
        self.hs.add("apple")
        self.hs.add("banana")
        self.hs.add("apple")  # Duplicate, should not increase size
        self.assertEqual(len(self.hs), 2)

    def test_contains(self):
        self.hs.add("apple")
        self.assertTrue(self.hs.contains("apple"))
        self.assertFalse(self.hs.contains("banana"))

    def test_remove(self):
        self.hs.add("apple")
        self.hs.add("banana")
        self.hs.remove("banana")
        self.assertFalse(self.hs.contains("banana"))
        self.assertEqual(len(self.hs), 1)

    def test_remove_key_error(self):
        with self.assertRaises(KeyError):
            self.hs.remove("ghost")

    def test_str(self):
        self.hs.add("one")
        self.hs.add("two")
        output = str(self.hs)
        self.assertIn("HashSet →", output)
        self.assertIn("'one'", output)
        self.assertIn("'two'", output)

    def test_resize_trigger(self):
        initial_capacity = self.hs.capacity
        for i in range(10):  # Should trigger resize
            self.hs.add(f"k{i}")
        self.assertGreaterEqual(self.hs.capacity, initial_capacity * 2)
        self.assertEqual(len(self.hs), 10)

if __name__ == "__main__":
    unittest.main()
