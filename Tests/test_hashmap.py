import unittest

from Hash.hashmap import HashMap


class TestHashMap(unittest.TestCase):

    def setUp(self):
        self.hm = HashMap()

    def test_put_and_get(self):
        self.hm.put("name", "Alice")
        self.hm.put("age", 25)
        self.hm.put("name", "Bob")  # Overwrite
        self.assertEqual(self.hm.get("name"), "Bob")
        self.assertEqual(self.hm.get("age"), 25)

    def test_get_key_error(self):
        with self.assertRaises(KeyError):
            self.hm.get("missing")

    def test_remove(self):
        self.hm.put("key", "value")
        self.hm.remove("key")
        self.assertEqual(len(self.hm), 0)
        with self.assertRaises(KeyError):
            self.hm.get("key")

    def test_remove_key_error(self):
        with self.assertRaises(KeyError):
            self.hm.remove("ghost")

    def test_contains(self):
        self.hm.put("x", 100)
        self.assertTrue(self.hm.contains("x"))
        self.hm.remove("x")
        self.assertFalse(self.hm.contains("x"))

    def test_len(self):
        self.hm.put("a", 1)
        self.hm.put("b", 2)
        self.assertEqual(len(self.hm), 2)
        self.hm.remove("a")
        self.assertEqual(len(self.hm), 1)

    def test_str(self):
        self.hm.put("k1", "v1")
        self.hm.put("k2", "v2")
        output = str(self.hm)
        self.assertIn("HashMap →", output)
        self.assertIn("'k1': 'v1'", output)
        self.assertIn("'k2': 'v2'", output)

    def test_resize_trigger(self):
        initial_capacity = self.hm.capacity
        for i in range(10):  # Enough to trigger resize
            self.hm.put(f"k{i}", i)
        self.assertGreaterEqual(self.hm.capacity, initial_capacity * 2)
        self.assertEqual(len(self.hm), 10)

if __name__ == "__main__":
    unittest.main()
