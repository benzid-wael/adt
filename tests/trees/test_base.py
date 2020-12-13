import copy
import random
import unittest
import logging

from parameterized import parameterized

from adt.visualizer import DigraphVisualizer
from adt.trees.base import BinarySearchTree
from adt.trees.base import NodeNotFound


logger = logging.getLogger(__name__)


class BinarySearchTreeTestCase(unittest.TestCase):

    @staticmethod
    def create_bst(data, name=None):
        name = name or '_'.join(str(elt) for elt in data)
        logger.debug(f'Creating BST {name} with given data: {data}')
        tree = BinarySearchTree(data[0])
        for elt in data[1:]:
            tree.insert(elt)
        graph = DigraphVisualizer.from_data(tree)
        DigraphVisualizer.render(graph, name, directory='.debug/bst')
        return tree

    @staticmethod
    def create_bst_with_random_insertion(data):
        data = copy.copy(data)
        k = len(data)
        tree = []
        while k > 0:
            idx = random.choice(range(k))
            tree.append(data.pop(idx))
            k -= 1
        return BinarySearchTreeTestCase.create_bst(tree)

    @parameterized.expand([
        (2,),
        (4,),
        (7,),
        (0,),
    ])
    def test_init_creates_binary_search_tree(self, elt):
        # when
        tree = BinarySearchTree(elt)
        # then
        self.assertEqual(tree.value, elt)
        self.assertIsNone(tree.parent)
        self.assertIsNone(tree.left)
        self.assertIsNone(tree.right)

    @parameterized.expand([
        ([12, 4, 2, 8, 7, 20, 14, 33, 31], 4, 2),
        ([12, 4, 2, 8, 7, 20, 14, 33, 31], 12, 8),
        ([12, 4, 2, 7, 8, 20, 14, 33, 31], 12, 8),
        ([12, 4, 2, 8, 7, 20, 14, 33, 31], 33, 31),
        ([12, 4, 2, 8, 7, 20, 14, 33, 31], 2, None),
        ([12, 4, 2, 8, 7, 20, 14, 33, 31], 20, 14),
    ])
    def test_predecessor(self, data, elt, expected):
        tree = self.create_bst(data)
        node = tree.search(elt)
        if expected:
            self.assertEqual(expected, node.predecessor.value)
        else:
            self.assertIsNone(node.predecessor)

    @parameterized.expand([
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], ),
        (['a', 'c', 'e', 'g', 'h', 'j', 'm', 'u', 'w'], ),
    ])
    def test_insert_inserts_node_while_respecting_bst_property(self, expected):
        # Given / When
        tree = self.create_bst_with_random_insertion(expected)
        # Then
        self.assertEqual(tree.inorder(), expected)

    @parameterized.expand([
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 4, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 12, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 33, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 2, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 9, False),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 0, False),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 1, False),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 50, False),
    ])
    def test_search_returns_element_if_found_or_raises_exception(self, data, elt, found):
        tree = self.create_bst_with_random_insertion(data)
        if found:
            self.assertIsNotNone(tree.search(elt))
        else:
            self.assertRaises(NodeNotFound, tree.search, elt)

    @parameterized.expand([
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 4, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 12, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 33, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 2, True),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 9, False),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 0, False),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 1, False),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 50, False),
    ])
    def test_delete_removes_node_or_raises_exception(self, data, elt, removed):
        tree = self.create_bst_with_random_insertion(data)
        if removed:
            self.assertIsNotNone(tree.delete(elt))
        else:
            self.assertRaises(NodeNotFound, tree.search, elt)

    @parameterized.expand([
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 4),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 12),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 33),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 2),
        ([2, 4, 7, 8, 12, 14, 20, 31, 33], 20),
    ])
    def test_search_after_removing_node_raises_exception(self, data, elt):
        tree = self.create_bst_with_random_insertion(data)
        tree.delete(elt)
        self.assertRaises(NodeNotFound, tree.search, elt)
