import unittest

from Non_Linear.trees.binary_tree import BinaryTree, Node
from Non_Linear.trees.traversals import TreeTraversals


class TestIterativeTraversals(unittest.TestCase):

    def setUp(self):
        # Build a known tree:
        #         1
        #       /   \
        #      2     3
        #     / \   / \
        #    4  5  6  7
        self.bt = BinaryTree()
        self.bt.root = Node(1)
        self.bt.root.left = Node(2)
        self.bt.root.right = Node(3)
        self.bt.root.left.left = Node(4)
        self.bt.root.left.right = Node(5)
        self.bt.root.right.left = Node(6)
        self.bt.root.right.right = Node(7)

    def test_iterative_inorder(self):
        expected = [4, 2, 5, 1, 6, 3, 7]
        self.assertEqual(TreeTraversals.iterative_inorder(self.bt.root), expected)

    def test_iterative_preorder(self):
        expected = [1, 2, 4, 5, 3, 6, 7]
        self.assertEqual(TreeTraversals.iterative_preorder(self.bt.root), expected)

    def test_iterative_postorder(self):
        expected = [4, 5, 2, 6, 7, 3, 1]
        self.assertEqual(TreeTraversals.iterative_postorder(self.bt.root), expected)


if __name__ == "__main__":
    unittest.main()
