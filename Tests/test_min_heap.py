import unittest

from Non_Linear.heaps.min_heap import MinHeap  # Adjust import path as needed for your project


class TestMinHeap(unittest.TestCase):

    def setUp(self):
        self.heap = MinHeap()

    def test_empty_heap(self):
        self.assertEqual(len(self.heap), 0)
        self.assertIsNone(self.heap.get_min())
        self.assertIsNone(self.heap.extract_min())

    def test_single_element(self):
        self.heap.insert(10)
        self.assertEqual(self.heap.get_min(), 10)
        self.assertEqual(len(self.heap), 1)
        self.assertEqual(self.heap.extract_min(), 10)
        self.assertEqual(len(self.heap), 0)
        self.assertIsNone(self.heap.get_min())

    def test_multiple_insert_extract(self):
        elements = [5, 3, 8, 1, 7]
        for el in elements:
            self.heap.insert(el)
        result = [self.heap.extract_min() for _ in range(len(elements))]
        self.assertEqual(result, sorted(elements))

    def test_duplicates(self):
        elements = [2, 2, 1, 1, 3]
        for el in elements:
            self.heap.insert(el)
        result = [self.heap.extract_min() for _ in range(len(elements))]
        self.assertEqual(result, sorted(elements))

    def test_negative_numbers(self):
        elements = [0, -10, -3, 5, -1]
        for el in elements:
            self.heap.insert(el)
        result = [self.heap.extract_min() for _ in range(len(elements))]
        self.assertEqual(result, sorted(elements))

    def test_heap_property_after_insert(self):
        # After each insert, get_min should always be the smallest
        elements = [7, 3, 5, 1, 9]
        expected_mins = []
        for el in elements:
            self.heap.insert(el)
            expected_mins.append(min(elements[:elements.index(el)+1]))
        actual_mins = []
        heap2 = MinHeap()
        for i, el in enumerate(elements):
            heap2.insert(el)
            actual_mins.append(heap2.get_min())
        self.assertEqual(actual_mins, [7, 3, 3, 1, 1])

if __name__ == '__main__':
    unittest.main()
