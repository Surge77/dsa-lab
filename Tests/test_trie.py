import unittest

# Import your Trie and TrieNode classes here if in another file:
from Non_Linear.trie.trie import Trie


class TestTrie(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()
        self.words = ["cat", "car", "cart", "dog", "door", "doom"]
        for word in self.words:
            self.trie.insert(word)

    def test_insert_and_search(self):
        for word in self.words:
            self.assertTrue(self.trie.search(word), f"Should find word: {word}")
        self.assertFalse(self.trie.search("can"))
        self.assertFalse(self.trie.search("ca"))
        self.assertFalse(self.trie.search("do"))
        self.assertFalse(self.trie.search(""))

    def test_starts_with(self):
        self.assertTrue(self.trie.starts_with("ca"))
        self.assertTrue(self.trie.starts_with("car"))
        self.assertTrue(self.trie.starts_with("do"))
        self.assertTrue(self.trie.starts_with("d"))
        self.assertFalse(self.trie.starts_with("z"))
        self.assertTrue(self.trie.starts_with(""))  # Every word starts with empty prefix

    def test_words_with_prefix(self):
        self.assertCountEqual(self.trie.words_with_prefix("ca"), ["cat", "car", "cart"])
        self.assertCountEqual(self.trie.words_with_prefix("car"), ["car", "cart"])
        self.assertCountEqual(self.trie.words_with_prefix("do"), ["dog", "door", "doom"])
        self.assertEqual(self.trie.words_with_prefix("z"), [])
        self.assertCountEqual(self.trie.words_with_prefix(""), self.words)

    def test_count_words_with_prefix(self):
        self.assertEqual(self.trie.count_words_with_prefix("ca"), 3)
        self.assertEqual(self.trie.count_words_with_prefix("car"), 2)
        self.assertEqual(self.trie.count_words_with_prefix("do"), 3)
        self.assertEqual(self.trie.count_words_with_prefix("dog"), 1)
        self.assertEqual(self.trie.count_words_with_prefix("z"), 0)
        self.assertEqual(self.trie.count_words_with_prefix(""), len(self.words))

    def test_delete(self):
        self.assertTrue(self.trie.delete("car"))
        self.assertFalse(self.trie.search("car"))
        self.assertTrue(self.trie.search("cart"))  # 'cart' should still exist
        self.assertTrue(self.trie.delete("cart"))
        self.assertFalse(self.trie.search("cart"))
        self.assertTrue(self.trie.delete("cat"))
        self.assertFalse(self.trie.search("cat"))
        # Delete non-existent word
        self.assertFalse(self.trie.delete("can"))
        # Delete previously deleted word
        self.assertFalse(self.trie.delete("car"))

    def test_longest_prefix_match(self):
        self.assertEqual(self.trie.longest_prefix_match("cartoon"), "cart")
        self.assertEqual(self.trie.longest_prefix_match("carpet"), "car")
        self.assertEqual(self.trie.longest_prefix_match("caterpillar"), "cat")
        self.assertEqual(self.trie.longest_prefix_match("dogged"), "dog")
        self.assertEqual(self.trie.longest_prefix_match("doorman"), "door")
        self.assertEqual(self.trie.longest_prefix_match("zebra"), "")
        self.assertEqual(self.trie.longest_prefix_match(""), "")

    def test_serialize_and_deserialize(self):
        serialized = self.trie.serialize()
        new_trie = Trie()
        new_trie.deserialize(serialized)
        for word in self.words:
            self.assertTrue(new_trie.search(word))
        self.assertFalse(new_trie.search("can"))
        self.assertTrue(new_trie.starts_with("ca"))
        self.assertEqual(new_trie.longest_prefix_match("cartoon"), "cart")

    def test_edge_cases(self):
        # Insert empty string (if you want to allow, otherwise skip/test this as False)
        empty_trie = Trie()
        empty_trie.insert("")
        self.assertTrue(empty_trie.search(""))
        self.assertTrue(empty_trie.starts_with(""))
        self.assertEqual(empty_trie.words_with_prefix(""), [""])
        self.assertEqual(empty_trie.count_words_with_prefix(""), 1)
        self.assertTrue(empty_trie.delete(""))
        self.assertFalse(empty_trie.search(""))

        # Insert word with repeated letters
        self.trie.insert("aaaaa")
        self.assertTrue(self.trie.search("aaaaa"))
        self.assertEqual(self.trie.longest_prefix_match("aaaaabbb"), "aaaaa")
        self.assertTrue(self.trie.delete("aaaaa"))
        self.assertFalse(self.trie.search("aaaaa"))

if __name__ == "__main__":
    unittest.main()
