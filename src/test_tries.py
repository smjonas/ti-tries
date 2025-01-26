import os
import unittest
from typing import Callable


def test_scenario_for_project(self, variant, project_name: str, build_trie: Callable):
    from base import run

    self.assertTrue(os.path.exists("../output/example-expected-output.txt"))
    run(
        variant,
        "../input/example-input.txt",
        "../input/example-queries.txt",
        f"../output/results-{project_name}.txt",
        build_trie,
    )
    with open("../output/example-expected-output.txt") as expected_file, open(
        f"../output/results-{project_name}.txt"
    ) as actual_file:
        self.assertListEqual(list(expected_file), list(actual_file))


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

    def test_scenario(self):
        from balanced_search_tree_trie import Trie

        test_scenario_for_project(self, 3, "balanced-search-tree-trie", lambda: Trie())


class TestFixedSizeArraysTrie(unittest.TestCase):
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

    def test_scenario(self):
        from fixed_size_arrays_trie import Trie

        test_scenario_for_project(self, 1, "fixed-size-arrays-trie", lambda: Trie())


class TestHashTablesTrie(unittest.TestCase):
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

    def test_scenario(self):
        from hash_tables_trie import Trie

        test_scenario_for_project(self, 2, "hash-tables-trie", lambda: Trie())
