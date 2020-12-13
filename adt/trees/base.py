from adt.exceptions import NodeNotFound
from adt.exceptions import InvalidChild


class BinarySearchTree:
    """
    Generic binary search tree.
    This class will wrap any collection into BST data structure.
    """

    def __init__(self, elt, parent=None):
        self.value = elt
        self.left = None
        self.right = None
        self.parent = parent

    @property
    def is_leaf(self):
        return not (self.left or self.right)

    @property
    def is_root(self):
        return self.parent is None

    @property
    def successor(self):
        """ Returns inorder successor. """
        return self.right.predecessor or self.right if self.right else None

    @property
    def predecessor(self):
        """ Returns inorder predecessor. """
        return self.left.successor or self.left if self.left else None

    def insert(self, elt):
        """ Insert new element into the BST. """
        if elt < self.value and self.left:
            return self.left.insert(elt)
        elif elt < self.value:
            self.left = BinarySearchTree(elt, parent=self)
            return self.left
        elif elt > self.value and self.right:
            return self.right.insert(elt)
        elif elt > self.value:
            self.right = BinarySearchTree(elt, parent=self)
            return self.right

    def search(self, elt):
        curr = self
        while curr:
            if elt < curr.value:
                curr = curr.left
            elif elt > curr.value:
                curr = curr.right
            else:
                return curr
        raise NodeNotFound('Node not found')

    def replace_child_with(self, child, value):
        """
        Update node to point to new child.

        :raise InvalidChild: Iff node is not pointing to the old child
        """
        if child is self.left:
            self.left = value
        elif child is self.right:
            self.right = value
        else:
            raise InvalidChild(f'Node {self} does not have child: {child}')
        if value:
            value.parent = self

    def delete(self, elt):
        node = self.search(elt)
        if node.is_leaf:
            node.parent.replace_child_with(node, None)
        elif node.left and node.right:
            # replace node with its inorder predecessor
            node.left.parent = node.predecessor
            node.right.parent = node.predecessor
            node.predecessor.parent.replace_child_with(node.predecessor, None)
            node.parent.replace_child_with(node, node.predecessor)
        elif node.left:
            node.parent.replace_child_with(node, node.left)
        elif node.right:
            node.parent.replace_child_with(node, node.right)
        return node

    def inorder(self):
        data = []
        if self.left:
            data.extend(self.left.inorder())
        data.append(self.value)
        if self.right:
            data.extend(self.right.inorder())
        return data
