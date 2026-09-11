import unittest

from Non_Linear.trees.binary_tree import BinaryTree, Node


class TestBinaryTree(unittest.TestCase):

    def setUp(self):
        self.bt = BinaryTree()
        self.bt.root = Node(1)
        self.bt.root.left = Node(2)
        self.bt.root.right = Node(3)
        self.bt.root.left.left = Node(4)
        self.bt.root.left.right = Node(5)
        self.bt.root.right.left = Node(6)
        self.bt.root.right.right = Node(7)

    def test_insertion_and_level_order(self):
        bt = BinaryTree()
        for i in range(1, 8):
            bt.insert(i)
        self.assertEqual(bt.level_order_traversal(), [1, 2, 3, 4, 5, 6, 7])

    def test_traversals(self):
        self.assertEqual(self.bt.inorder(), [4, 2, 5, 1, 6, 3, 7])
        self.assertEqual(self.bt.preorder(), [1, 2, 4, 5, 3, 6, 7])
        self.assertEqual(self.bt.postorder(), [4, 5, 2, 6, 7, 3, 1])

    def test_search(self):
        self.assertTrue(self.bt.search(4))
        self.assertFalse(self.bt.search(100))

    def test_height(self):
        self.assertEqual(self.bt.height(), 3)

    def test_leaf_count(self):
        self.assertEqual(self.bt.count_leaf_nodes(), 4)  # 4, 5, 6, 7

    def test_diameter(self):
        self.assertEqual(self.bt.diameter(), 5)  # longest path: 4-2-1-3-7

    def test_symmetry_true(self):
        tree = BinaryTree()
        tree.root = Node(1)
        tree.root.left = Node(2)
        tree.root.right = Node(2)
        tree.root.left.left = Node(3)
        tree.root.left.right = Node(4)
        tree.root.right.left = Node(4)
        tree.root.right.right = Node(3)
        self.assertTrue(tree.is_symmetric())

    def test_symmetry_false(self):
        self.bt.root.right.right.value = 99  # break symmetry
        self.assertFalse(self.bt.is_symmetric())

    def test_delete_existing_node(self):
        bt = BinaryTree()
        for i in range(1, 8):
            bt.insert(i)
        self.assertTrue(bt.delete(3))
        self.assertNotIn(3, bt.level_order_traversal())

    def test_delete_nonexistent_node(self):
        self.assertFalse(self.bt.delete(100))

    def test_lowest_common_ancestor(self):
        self.assertEqual(self.bt.lowest_common_ancestor(4, 5), 2)
        self.assertEqual(self.bt.lowest_common_ancestor(4, 6), 1)
        self.assertEqual(self.bt.lowest_common_ancestor(6, 7), 3)

    def test_path_to_node(self):
        self.assertEqual(self.bt.path_to_node(5), [1, 2, 5])
        self.assertEqual(self.bt.path_to_node(7), [1, 3, 7])
        self.assertEqual(self.bt.path_to_node(100), [])

    def test_max_path_sum(self):
        bt = BinaryTree()
        bt.root = Node(-10)
        bt.root.left = Node(9)
        bt.root.right = Node(20)
        bt.root.right.left = Node(15)
        bt.root.right.right = Node(7)
        self.assertEqual(bt.max_path_sum(), 42)

    def test_max_root_to_leaf_sum(self):
        bt = BinaryTree()
        bt.root = Node(10)
        bt.root.left = Node(5)
        bt.root.right = Node(12)
        bt.root.left.left = Node(4)
        bt.root.left.right = Node(7)
        self.assertEqual(bt.max_root_to_leaf_sum(), 22)

    def test_min_root_to_leaf_sum(self):
        bt = BinaryTree()
        bt.root = Node(10)
        bt.root.left = Node(5)
        bt.root.right = Node(12)
        bt.root.left.left = Node(4)
        bt.root.left.right = Node(1)
        self.assertEqual(bt.min_root_to_leaf_sum(), 16)

    def test_min_root_to_leaf_path(self):
        bt = BinaryTree()
        bt.root = Node(10)
        bt.root.left = Node(5)
        bt.root.right = Node(12)
        bt.root.left.left = Node(4)
        bt.root.left.right = Node(1)
        self.assertEqual(bt.min_root_to_leaf_path(), [10, 5, 1])


if __name__ == '__main__':
    unittest.main()
