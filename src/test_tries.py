import unittest


class TestBalancedSearchTreeTrie(unittest.TestCase):
    def setUp(self):
        from balanced_search_tree_trie import Trie

        self.trie = Trie()

    def test_insert_and_contains(self):
        self.assertFalse(self.trie.contains("apple"))
        self.assertTrue(self.trie.insert("apple"))
        self.assertTrue(self.trie.contains("apple"))
        self.assertFalse(self.trie.insert("apple"))  # Duplicate insert

    def test_delete(self):
        self.assertFalse(self.trie.delete("apple"))  # Deleting non-existent word
        self.trie.insert("apple")
        self.assertTrue(self.trie.delete("apple"))
        self.assertFalse(self.trie.contains("apple"))


class TestFixedSizeArrayTrie(unittest.TestCase):
    def setUp(self):
        from fixed_size_arrays_trie import Trie

        self.trie = Trie()

    def test_insert_and_contains(self):
        self.assertFalse(self.trie.contains("banana"))
        self.assertTrue(self.trie.insert("banana"))
        self.assertTrue(self.trie.contains("banana"))
        self.assertFalse(self.trie.insert("banana"))  # Duplicate insert

    def test_delete(self):
        self.assertFalse(self.trie.delete("banana"))  # Deleting non-existent word
        self.trie.insert("banana")
        self.assertTrue(self.trie.delete("banana"))
        self.assertFalse(self.trie.contains("banana"))


class TestHashTableTrie(unittest.TestCase):
    def setUp(self):
        from hash_tables_trie import Trie

        self.trie = Trie()

    def test_insert_and_contains(self):
        self.assertFalse(self.trie.contains("cherry"))
        self.assertTrue(self.trie.insert("cherry"))
        self.assertTrue(self.trie.contains("cherry"))
        self.assertFalse(self.trie.insert("cherry"))  # Duplicate insert

    def test_delete(self):
        self.assertFalse(self.trie.delete("cherry"))  # Deleting non-existent word
        self.trie.insert("cherry")
        self.assertTrue(self.trie.delete("cherry"))
        self.assertFalse(self.trie.contains("cherry"))
