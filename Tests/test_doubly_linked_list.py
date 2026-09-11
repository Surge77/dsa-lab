import unittest

from Linear.doubly_linked_list import DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):

    def setUp(self):
        self.dll = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            self.dll.append(val)

    def test_append(self):
        self.dll.append("d")
        self.assertEqual(str(self.dll), "a <-> b <-> c <-> d <-> None")
        self.assertEqual(len(self.dll), 4)

    def test_prepend(self):
        self.dll.prepend("start")
        self.assertEqual(str(self.dll), "start <-> a <-> b <-> c <-> None")
        self.assertEqual(len(self.dll), 4)

    def test_get(self):
        self.assertEqual(self.dll.get(0), "a")
        self.assertEqual(self.dll.get(2), "c")
        with self.assertRaises(IndexError):
            self.dll.get(5)

    def test_set(self):
        self.dll.set(1, "z")
        self.assertEqual(self.dll.get(1), "z")
        with self.assertRaises(IndexError):
            self.dll.set(5, "x")

    def test_insert(self):
        self.dll.insert(1, "x")
        self.assertEqual(str(self.dll), "a <-> x <-> b <-> c <-> None")
        self.dll.insert(0, "start")
        self.dll.insert(len(self.dll), "end")
        self.assertEqual(str(self.dll), "start <-> a <-> x <-> b <-> c <-> end <-> None")

    def test_delete(self):
        self.dll.delete(1)
        self.assertEqual(str(self.dll), "a <-> c <-> None")
        self.dll.delete(0)
        self.assertEqual(str(self.dll), "c <-> None")
        with self.assertRaises(IndexError):
            self.dll.delete(5)

    def test_len(self):
        self.assertEqual(len(self.dll), 3)
        self.dll.append("d")
        self.assertEqual(len(self.dll), 4)

    def test_search(self):
        self.assertEqual(self.dll.search("b"), 1)
        self.assertEqual(self.dll.search("z"), -1)

    def test_reverse(self):
        self.dll.reverse()
        self.assertEqual(str(self.dll), "c <-> b <-> a <-> None")
        self.dll.reverse()
        self.assertEqual(str(self.dll), "a <-> b <-> c <-> None")


if __name__ == "__main__":
    unittest.main()
