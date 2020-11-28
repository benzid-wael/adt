import unittest

from parameterized import parameterized

from adt.trees.segment_tree import SegmentTree
from adt.trees.segment_tree import SegmentTreeFactory


class SegmentTreeTestCase(unittest.TestCase):
    @parameterized.expand([
        ([], 'sum', []),  # empty array
        ([1], 'sum', [1]),  # array of ONE element
        ([1, 3], 'sum', [4, 1, 3]),
        ([1, 3], 'min', [1, 1, 3]),
        ([1, 3], 'max', [3, 1, 3]),
        # array of length power of 2
        ([1, 3, 8, 2, 5, 6, 10, 2], 'sum', [37, 14, 23, 4, 10, 11, 12, 1, 3, 8, 2, 5, 6, 10, 2]),
        ([1, 3, 8, 2, 5, 6, 10], 'sum', [35, 14, 21, 4, 10, 11, 10, 1, 3, 8, 2, 5, 6]),  # array of random length
    ])
    def test_init_creates_segment_tree(self, array, kind, expected):
        # when
        actual = SegmentTreeFactory.create(array, kind)
        # then
        self.assertEqual(actual.tree, expected)

    @parameterized.expand(([
        ([1, 2], 'sum', 0, 0, 1),
        ([1, 2], 'sum', 1, 1, 2),
        ([1, 2], 'sum', 0, 1, 3),
        ([1, 2], 'min', 0, 1, 1),
        ([1, 2], 'max', 0, 1, 2),
        ([4, 8, 1, 10, 2, 5, 13, 9], 'sum', 0, 2, 13),
    ]))
    def test_query_queries_static_arrays(self, array, kind, start, end, expected):
        # given
        testee = SegmentTreeFactory.create(array, kind)
        # when
        actual = testee.query(start, end)
        # then
        self.assertEqual(actual, expected)

    @parameterized.expand([
        ([1, 2], 'sum', 0, 0),
        ([1, 2], 'sum', 1, 1),
        ([1, 2], 'sum', 0, 1),
        ([4, 8, 1, 10, 2, 5, 13, 9], 'sum', 0, 2),
    ])
    def test_SegmentTree_range_sum_query_for_dynamic_arrays(self, array, kind, start, end):
        # given
        testee = SegmentTreeFactory.create(array, kind)
        testee.update(start, 0)
        before = testee.query(start, end)
        # when
        testee.update(start, 5)
        # then
        actual = testee.query(start, end)
        self.assertEqual(actual, before + 5)


class SegmentTreeFactoryTestCase(unittest.TestCase):
    @parameterized.expand([
        ([], 'sum', []),  # empty array
        ([1], 'sum', [1]),  # array of ONE element
        ([1, 3], 'sum', [4, 1, 3]),
        ([1, 3], 'min', [1, 1, 3]),
        ([1, 3], 'max', [3, 1, 3]),
        # array of length power of 2
        ([1, 3, 8, 2, 5, 6, 10, 2], 'sum', [37, 14, 23, 4, 10, 11, 12, 1, 3, 8, 2, 5, 6, 10, 2]),
        ([1, 3, 8, 2, 5, 6, 10], 'sum', [35, 14, 21, 4, 10, 11, 10, 1, 3, 8, 2, 5, 6]),  # array of random length
    ])
    def test_create_initialize_segment_tree(self, array, kind, expected):
        # when
        actual = SegmentTreeFactory.create(array, kind)
        # then
        self.assertIsInstance(actual, SegmentTree)
        self.assertEqual(actual.tree, expected)

    @parameterized.expand([
        'product',
        'gcd',
        'gcd',
    ])
    def test_create_raises_value_error_for_unsupported_queries(self, kind):
        # when / then
        self.assertRaises(ValueError, SegmentTreeFactory.create, [1, 2], kind)
