import pytest

from adt.trees.segment_tree import SegmentTreeFactory


@pytest.mark.parametrize('array,kind,expected', [
    ([], 'sum', []),  # empty array
    ([1], 'sum', [1]),  # array of ONE element
    ([1, 3], 'sum', [4, 1, 3]),
    ([1, 3], 'min', [1, 1, 3]),
    ([1, 3], 'max', [3, 1, 3]),
    # array of length power of 2
    ([1, 3, 8, 2, 5, 6, 10, 2], 'sum', [37, 14, 23, 4, 10, 11, 12, 1, 3, 8, 2, 5, 6, 10, 2]),
    ([1, 3, 8, 2, 5, 6, 10], 'sum', [35, 14, 21, 4, 10, 11, 10, 1, 3, 8, 2, 5, 6]),  # array of random length
])
def test_init_creates_segment_tree_from_given_array(array, kind, expected):
    # when
    actual = SegmentTreeFactory.create(array, kind)
    # then
    assert actual.tree == expected
