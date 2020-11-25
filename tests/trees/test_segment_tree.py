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


@pytest.mark.parametrize('array,kind,start,end,expected', [
    ([1, 2], 'sum', 0, 0, 1),
    ([1, 2], 'sum', 1, 1, 2),
    ([1, 2], 'sum', 0, 1, 3),
    ([1, 2], 'min', 0, 1, 1),
    ([1, 2], 'max', 0, 1, 2),
    ([4, 8, 1, 10, 2, 5, 13, 9], 'sum', 0, 2, 13),
])
def test_query_static_arrays(array, kind, start, end, expected):
    # given
    testee = SegmentTreeFactory.create(array, kind)
    # when
    actual = testee.query(start, end)
    # then
    assert actual == expected


@pytest.mark.parametrize('array,kind,start,end', [
    ([1, 2], 'sum', 0, 0),
    ([1, 2], 'sum', 1, 1),
    ([1, 2], 'sum', 0, 1),
    ([4, 8, 1, 10, 2, 5, 13, 9], 'sum', 0, 2),
])
def test_range_sum_query_for_dynamic_arrays(array, kind, start, end):
    # given
    testee = SegmentTreeFactory.create(array, kind)
    testee.update(start, 0)
    before = testee.query(start, end)
    # when
    testee.update(start, 5)
    # then
    actual = testee.query(start, end)
    assert actual == before + 5
