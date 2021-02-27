class AlreadyUnified(ValueError):
    pass


class SimpleUnionFind:
    """
    Generic Union-Find Disjoint Set container.

    This class can be initialized with any iterable.
    The iterable should contain hashable items.

    >>> UnionFind([1, 2, "hello", True, "a", 2.2])
    """

    def __init__(self, items):
        self.to_index = {item: i for i, item in enumerate(items)}
        self.from_index = {i: item for i, item in enumerate(items)}
        self.parent = [i for i in range(len(items))]
        self.size = [0 for _ in range(len(items))]

    def find(self, item):
        """ Return set's representative of set to which the given item belongs. """
        index = self.to_index[item]
        while self.parent[index] != index:
            self.parent[index] = self.parent[self.parent[index]]
            index = self.parent[index]
        return self.from_index[index]

    def union(self, item1, item2):
        """ Join sets containing item1 and item2. """
        head1 = self.find(item1)
        head2 = self.find(item2)

        if head1 == head2:
            raise AlreadyUnified('items already belongs to the same set')

        if self.size[head1] <= self.size[head2]:
            self.parent[head2] = head1
            self.size[head1] += 1
            return head1
        else:
            self.parent[head1] = head2
            self.size[head2] += 1
            return head2


class UnionFind(SimpleUnionFind):
    """ Implementation of weighted union-find with path compression. """

    def find(self, item):
        """ Return set's representative of set to which the given item belongs. """
        current = self.to_index[item]
        root = current
        while self.parent[root] != root:
            self.parent[root] = self.parent[self.parent[root]]
            root = self.parent[root]

        # 2nd loop to flat the tree
        next = self.parent[current]
        while next != current:
            self.parent[current] = root
            current = next
            next = self.parent[next]
        return self.from_index[root]
