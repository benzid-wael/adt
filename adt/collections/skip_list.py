import random
from collections import namedtuple
from functools import total_ordering


class DoublyLinkedList:
    """
    Base class to represent sorted linked list.
    """

    def __init__(self, value, next=None, previous=None):
        self.value = value
        self.next = next
        self.previous = previous

    @classmethod
    def create(cls, *items):
        sorted_items = sorted(items)
        head = cls(sorted_items[0])
        parent = head
        for item in sorted_items[1:]:
            parent.next = cls(item, previous=parent)
            parent = parent.next
        return head

    def _find_predecessor(self, item):
        prev = self
        while prev.next and prev.next.value < item:
            prev = prev.next
        return prev

    def add(self, item):
        prev = self._find_predecessor(item)
        node = self.__class__(item, next=prev.next)
        prev.next = node
        return node

    def find(self, item):
        prev = self._find_predecessor(item)
        return prev.next if prev.next and prev.next.value == item else None

    def delete(self, item):
        node = self._find_predecessor(item)
        if node.next and node.next.value == item:
            # delete node.next
            to_delete = node.next
            successor = node.next.next
            node.next = successor
            return to_delete


@total_ordering
class SkipList:
    Position = namedtuple('Position', 'node,index')
    header = float('-inf')
    sentinel = float('inf')

    def __init__(self, item):
        self.value = item
        self.pointers = []

    @classmethod
    def new(cls):
        head = SkipList(cls.header)
        sentinel = SkipList(cls.sentinel)
        head.pointers = [sentinel, sentinel]  # express and normal lanes
        return head

    ####################################################################
    #                            Public APIs                           #
    ####################################################################

    def add(self, item):
        p, index = self._find_item(item)

        # node already exist
        if item == p:
            p.value = item
            return p

        # insert new node
        new_node = SkipList(item)
        index = max(0, index - 1)
        new_node._add_pointer(p, index)
        p.pointers[index] = new_node

        self._adjust_height(p, index, new_node)
        return new_node

    def find(self, item):
        p, index = self._find_item(item)
        return p if p == item else None

    ####################################################################
    #                            Private APIs                          #
    ####################################################################

    def _add_pointer(self, node: 'SkipList', index):
        self.pointers.append(node.pointers[index])
        node.pointers[index] = self

    def _adjust_height(self, parent: 'SkipList', index: int, new_node: 'SkipList'):
        # flip coins to add new level
        flip = random.random() >= 0.5 and self.value > self.header
        index -= 1
        levels = 0
        while flip and index >= 0:
            new_node._add_pointer(parent, index)
            # next iteration
            flip = random.random() >= 0.5
            index -= 1
            levels += 1
        return levels

    def _find_item(self, item):
        p = self
        index = 0
        while index < len(p.pointers):
            if item < p.pointers[index]:
                index += 1
            else:
                p = p.pointers[index]
                index = 0
        return p, index

    def __lt__(self, other):
        if isinstance(other, SkipList):
            return self.value < other.value
        return self.value < other

    def __eq__(self, other):
        if isinstance(other, SkipList):
            return self.value == other.value
        return self.value == other

    ####################################################################
    #                       BEGIN Visualizer API                       #
    ####################################################################
    def nodes(self):
        frontier = [self]
        discovered = set()
        while frontier:
            next_frontier = []
            for item in frontier:
                yield item
                for node in item.pointers:
                    if node not in discovered:
                        discovered.add(node)
                        next_frontier.append(node)
            frontier = next_frontier

    def edges(self):
        frontier = [self]
        discovered = set()
        while frontier:
            next_frontier = []
            for item in frontier:
                for node in item.pointers:
                    yield item, node
                    if node not in discovered:
                        discovered.add(node)
                        next_frontier.append(node)
            frontier = next_frontier

    ####################################################################
    #                        END Visualizer API                        #
    ####################################################################

