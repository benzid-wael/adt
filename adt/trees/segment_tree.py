"""
The segment tree is a highly versatile data structure, based upon the divide-and-conquer paradigm.
Segment trees is a tree where internal nodes represents ranges for an original array. Hence, it can be used to answer
range queries.
"""

import operator
import warnings


RANGE_MAX_QUERY = 'max'
RANGE_MIN_QUERY = 'min'
RANGE_SUM_QUERY = 'sum'
SUPPORTED_QUERIES_CONFIGURATION = {
    RANGE_SUM_QUERY: {
        'merge': operator.add,
        'default': 0,
    },
    RANGE_MIN_QUERY: {
        'merge': min,
        'default': float('inf'),
    },
    RANGE_MAX_QUERY: {
        'merge': max,
        'default': float('-inf'),
    }
}


class SegmentTree:
    """
    Base Implementation of Segment Tree. The segment tree is store in a zero-indexed array.

    To create a segment tree, you need to instantiate it with the original array and a callable that specify the merge
    function to be used. The merge function will be used to merge siblings in the segment tree.

    The merge function is a callable that takes two argument and return the reduced result. The merge function
    determines which kind of queries your segment tree can answer.

    |------------------------|------------------|------------------|
    | Query                  | Merge function   | Default          |
    |------------------------|------------------|------------------|
    | Range Sum Queries      | operator.add     | 0                |
    |------------------------|------------------|------------------|
    | Range Minimum Queries  | min              | float('inf')     |
    |------------------------|------------------|------------------|
    | Range Maximum Queries  | max              | float('-inf')    |
    |------------------------|------------------|------------------|

    For example, the below code show how to create a segment tree to answer sum queries:

    >>> import operator
    >>> SegmentTree(array, merge=operator.add, default=0)
    """

    def __init__(self, array, merge, default):
        """
        Creates segment tree from the given array.

        :param array: original array
        :param merge: function to be used to merge two siblings in the segment tree
        :return: segment tree as an array
        """
        self.length = len(array)
        self.merge = merge
        self.default = default
        # Typically, we need only to reserve 3n+3 slots in the array
        self.tree = [None for _ in range(2 * self.length - 1)]
        if self.tree:
            self.build_tree(array, 0, 0, self.length - 1)

    def build_tree(self, array, index, low, high):
        """
        Recursively build the segment tree from the given array.

        :param array: original array
        :param index:
        :param low:
        :param high:
        """
        if low == high:
            self.tree[index] = array[low]
        else:
            mid = (low + high) // 2
            left = index * 2 + 1
            right = left + 1
            self.build_tree(array, left, low, mid)
            self.build_tree(array, right, mid + 1, high)
            self.tree[index] = self.merge(self.tree[left], self.tree[right])

    def _update(self, index, low, high, pos, value):
        """
        Recursively updates intervals containing pos to reflect the update of the element at position pos with the new
        value.

        :param index:
        :param low:
        :param high:
        :param pos:
        :param value:
        """
        mid = (low + high) // 2
        if low == high:
            self.tree[index] = value
            return

        left = index * 2 + 1
        right = left + 1
        if pos <= mid:
            self._update(left, low, mid, pos, value)
        else:
            self._update(right, mid + 1, high, pos, value)
        self.tree[index] = self.merge(self.tree[right], self.tree[left])

    def update(self, pos, new_value):
        """ Updates element at the given position in the original array to the given new value. """
        self._update(0, 0, self.length - 1, pos, new_value)

    def _query(self, start, end, index, low, high):
        if start == low and end == high:
            return self.tree[index]
        elif low >= high:
            return self.default
        mid = (low + high) // 2
        left = index * 2 + 1
        right = left + 1
        return self.merge(
            self._query(start, min(end, mid), left, low, mid),
            self._query(max(start, mid + 1), end, right, mid + 1, high),
        )

    def query(self, start, end):
        """
        Answer the given range query.

        :param start: range's start
        :param end: range's end
        """
        if start < 0 or start >= self.length or start > end:
            raise ValueError(f'Invalid interval: start should belongs to [0, {self.length})')
        elif end < 0 or end >= self.length:
            raise ValueError(f'Invalid interval: end should belongs to [0, {self.length})')

        return self._query(start, end, 0, 0, self.length - 1)


class SegmentTreeFactory:
    """
    Factory class to initialize segment tree based on the type.
    The type determine which kind of queries the segment tree is able to answer.

    ... note:
        If you need to support more than one query type, you need to to create multiple segment tree for the same array.
    """

    @classmethod
    def create(cls, array, kind: str) -> SegmentTree:
        if kind == RANGE_SUM_QUERY:
            # For range sum queries, Segment tree is superseded by BIT, which simpler, faster and take less space
            warnings.warn('For range sum queries, it is recommended to use `adt.trees.bit.BIT` instead')
        if kind not in SUPPORTED_QUERIES_CONFIGURATION:
            supported = ', '.join(SUPPORTED_QUERIES_CONFIGURATION)
            raise ValueError(f'Unknown range query type. Supported types are: {supported}')
        return SegmentTree(array, **SUPPORTED_QUERIES_CONFIGURATION[kind])
