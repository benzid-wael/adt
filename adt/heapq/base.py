import abc
import math

__all__ = ['MaxHeap', 'MinHeap']


class Heap(abc.ABC):
    """
    This class defines interface of the base heap data structure.
    """

    def __init__(self, data=None):
        self.data = data or []

    @abc.abstractmethod
    def cmp(self, parent, child):
        # TODO rename this function to: is_heap_property_violated
        """ Returns boolean indicating whether the heap property is violated or not. """
        pass

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.size = len(value)
        if value:
            self.heapify_in_place()

    def heapify_in_place(self):
        """ Transform a list into a heap. """
        i = math.floor((self.size + 1) // 2) - 1
        while i >= 0:
            self.sift_down(i)
            i -= 1

    @classmethod
    def heapify(cls, data):
        return cls(data)

    def insert(self, elt):
        """ Inserts a new element into the heap. """
        if self.size < len(self.data):
            self.data[self.size] = elt
        else:
            self.data.append(elt)
        self.size += 1
        self.sift_up(self.size - 1)

    def sift_up(self, index):
        parent = math.floor((index + 1) // 2) - 1
        while index > parent >= 0 and self.cmp(self.data[parent], self.data[index]):
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index = parent
            parent = math.floor((index + 1) // 2) - 1

    def _promote_child(self, index):
        left = index * 2 + 1
        right = left + 1
        if self.cmp(self.data[index], self.data[left]):
            return left
        if self.cmp(self.data[index], self.data[right]):
            return right
        return index

    def sift_down(self, index):
        child = self._promote_child(index)
        while child != index:
            self.data[index], self.data[child] = self.data[child], self.data[index]
            index = child
            child = self._promote_child(index)

    def peek(self):
        """ Returns root element. """
        return self.data[0]

    def extract(self):
        """ Extract head element. """
        self.size -= 1
        self.data[0], self.data[self.size] = self.data[self.size], self.data[0]
        self.sift_down(0)


class MinHeap(Heap):
    def cmp(self, x, y):
        return bool(x > y)


class MaxHeap(Heap):
    def cmp(self, x, y):
        return bool(x < y)
