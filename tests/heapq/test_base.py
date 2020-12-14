import unittest

from parameterized import parameterized

from adt.heapq.base import MaxHeap


class MaxHeapTestCase(unittest.TestCase):
    @parameterized.expand([
        ([12, 8, 6], [12, 12, 12]),
        ([8, 6, 12], [8, 8, 12]),
        ([6, 8, 12], [6, 8, 12]),
    ])
    def test_insert_inserts_element_in_proper_order(self, elts, roots):
        heap = MaxHeap()
        for index, elt in enumerate(elts):
            heap.insert(elt)
            self.assertEqual(heap.peek(), roots[index])
