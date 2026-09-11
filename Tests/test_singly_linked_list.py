import unittest

from Linear.singly_linked_list import SinglyLinkedList


class TestSinglyLinkedList(unittest.TestCase):

    def setUp(self):
        self.ll = SinglyLinkedList()
        self.ll.append(10)
        self.ll.append(20)
        self.ll.append(30)

    def test_append(self):
        self.ll.append(40)
        self.assertEqual(str(self.ll), "10 -> 20 -> 30 -> 40 -> None")

    def test_prepend(self):
        self.ll.prepend(5)
        self.assertEqual(str(self.ll), "5 -> 10 -> 20 -> 30 -> None")

    def test_len(self):
        self.assertEqual(len(self.ll), 3)

    def test_get(self):
        self.assertEqual(self.ll.get(1), 20)
        with self.assertRaises(IndexError):
            self.ll.get(5)

    def test_set(self):
        self.ll.set(0, 99)
        self.assertEqual(self.ll.get(0), 99)
        with self.assertRaises(IndexError):
            self.ll.set(4, 111)

    def test_delete(self):
        self.ll.delete(1)  # Delete 20
        self.assertEqual(str(self.ll), "10 -> 30 -> None")
        with self.assertRaises(IndexError):
            self.ll.delete(5)

    def test_insert(self):
        self.ll.insert(1, 15)
        self.assertEqual(str(self.ll), "10 -> 15 -> 20 -> 30 -> None")
        self.ll.insert(0, 5)
        self.assertEqual(str(self.ll), "5 -> 10 -> 15 -> 20 -> 30 -> None")
        self.ll.insert(5, 35)
        self.assertEqual(str(self.ll), "5 -> 10 -> 15 -> 20 -> 30 -> 35 -> None")
        with self.assertRaises(IndexError):
            self.ll.insert(10, 99)

    def test_search(self):
        self.assertEqual(self.ll.search(30), 2)
        self.assertEqual(self.ll.search(99), -1)

    def test_reverse(self):
        self.ll.reverse()
        self.assertEqual(str(self.ll), "30 -> 20 -> 10 -> None")
        self.assertEqual(self.ll.head.value, 30)
        self.assertEqual(self.ll.tail.value, 10)


if __name__ == "__main__":
    unittest.main()
