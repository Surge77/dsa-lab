import unittest

from Non_Linear.heaps.max_heap import MaxHeap  # Adjust path if needed


class TestMaxHeap(unittest.TestCase):

    def setUp(self):
        self.heap = MaxHeap()

    def test_empty_heap(self):
        self.assertEqual(len(self.heap), 0)
        self.assertIsNone(self.heap.get_max())
        self.assertIsNone(self.heap.extract_max())

    def test_single_insert(self):
        self.heap.insert(42)
        self.assertEqual(self.heap.get_max(), 42)
        self.assertEqual(len(self.heap), 1)
        self.assertEqual(self.heap.extract_max(), 42)
        self.assertEqual(len(self.heap), 0)

    def test_multiple_insert_extract(self):
        values = [10, 20, 5, 15, 30]
        for v in values:
            self.heap.insert(v)
        result = []
        while len(self.heap):
            result.append(self.heap.extract_max())
        self.assertEqual(result, sorted(values, reverse=True))

    def test_replace(self):
        vals = [5, 9, 3, 8]
        for v in vals:
            self.heap.insert(v)
        old_max = self.heap.replace(7)
        self.assertEqual(old_max, 9)
        self.assertEqual(self.heap.get_max(), 8)
        self.assertIn(7, self.heap.data)

        empty_heap = MaxHeap()
        old_max = empty_heap.replace(100)
        self.assertIsNone(old_max)
        self.assertEqual(empty_heap.get_max(), 100)

    def test_heapify(self):
        vals = [2, 7, 1, 8, 3]
        self.heap.heapify(vals)
        # Root should be max
        self.assertEqual(self.heap.get_max(), max(vals))
        # The array should satisfy the max-heap property
        def is_max_heap(arr):
            n = len(arr)
            for i in range(n // 2):
                left = 2 * i + 1
                right = 2 * i + 2
                if left < n and arr[i] < arr[left]:
                    return False
                if right < n and arr[i] < arr[right]:
                    return False
            return True
        self.assertTrue(is_max_heap(self.heap.data))

    def test_negative_and_duplicate(self):
        vals = [0, -2, -2, 5, 5, 3]
        for v in vals:
            self.heap.insert(v)
        result = [self.heap.extract_max() for _ in range(len(vals))]
        self.assertEqual(result, sorted(vals, reverse=True))

    def test_get_max_consistency(self):
        vals = [4, 1, 9]
        for v in vals:
            self.heap.insert(v)
        self.assertEqual(self.heap.get_max(), max(vals))

if __name__ == "__main__":
    unittest.main()
