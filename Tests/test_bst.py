# test_bst.py

from Non_Linear.trees.bst import (
    BST,  # Change 'your_bst_file' to your actual BST implementation file name
)


def test_insert_and_inorder():
    bst = BST()
    for v in [10, 5, 20, 15, 2, 7]:
        bst.insert(v)
    assert bst.inorder() == [2, 5, 7, 10, 15, 20]

def test_search_and_contains():
    bst = BST()
    for v in [10, 5, 20]:
        bst.insert(v)
    assert bst.search(5).key == 5
    assert bst.search(100) is None
    assert bst.contains(10)
    assert not bst.contains(99)

def test_min_max():
    bst = BST()
    for v in [10, 5, 20]:
        bst.insert(v)
    assert bst.min().key == 5
    assert bst.max().key == 20

def test_delete():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    bst.delete(5)
    assert bst.inorder() == [2, 7, 10, 20]
    bst.delete(10)
    assert bst.inorder() == [2, 7, 20]

def test_traversals():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.preorder() == [10, 5, 2, 7, 20]
    assert bst.postorder() == [2, 7, 5, 20, 10]
    assert bst.level_order() == [10, 5, 20, 2, 7]

def test_height_and_count():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.height() == 2
    assert bst.count_nodes() == 5

def test_is_empty():
    bst = BST()
    assert bst.is_empty()
    bst.insert(10)
    assert not bst.is_empty()

def test_find_parent():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.find_parent(5).key == 10
    assert bst.find_parent(2).key == 5
    assert bst.find_parent(10) is None
    assert bst.find_parent(99) is None

def test_leaf_count():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.leaf_count() == 3  # 2, 7, 20 are leaves

def test_sum_nodes():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.sum_nodes() == 44

def test_node_depth():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.node_depth(10) == 0
    assert bst.node_depth(5) == 1
    assert bst.node_depth(2) == 2
    assert bst.node_depth(99) == -1

def test_path_to_node():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.path_to_node(2) == [10, 5, 2]
    assert bst.path_to_node(20) == [10, 20]
    assert bst.path_to_node(99) == []

def test_is_balanced():
    bst = BST()
    for v in [10, 5, 20, 2, 7]:
        bst.insert(v)
    assert bst.is_balanced()
    bst2 = BST()
    for v in [1, 2, 3, 4, 5]:
        bst2.insert(v)
    assert not bst2.is_balanced()

def test_lowest_common_ancestor():
    bst = BST()
    for v in [10, 5, 20, 2, 7, 15]:
        bst.insert(v)
    lca = bst.lowest_common_ancestor(2, 7)
    assert lca and lca.key == 5
    lca = bst.lowest_common_ancestor(15, 7)
    assert lca and lca.key == 10
    lca = bst.lowest_common_ancestor(2, 100)
    assert lca is None

def test_diameter():
    bst = BST()
    for v in [10, 5, 20, 15, 2, 7]:
        bst.insert(v)
    assert bst.diameter() == 4

def test_serialize_deserialize():
    bst = BST()
    for v in [10, 5, 20, 2, 15]:
        bst.insert(v)
    arr = bst.serialize()
    bst2 = BST.deserialize(arr)
    assert bst2.inorder() == bst.inorder()

def run_all_tests():
    test_insert_and_inorder()
    test_search_and_contains()
    test_min_max()
    test_delete()
    test_traversals()
    test_height_and_count()
    test_is_empty()
    test_find_parent()
    test_leaf_count()
    test_sum_nodes()
    test_node_depth()
    test_path_to_node()
    test_is_balanced()
    test_lowest_common_ancestor()
    test_diameter()
    test_serialize_deserialize()
    print("✅ All BST tests passed successfully!")

if __name__ == "__main__":
    run_all_tests()
