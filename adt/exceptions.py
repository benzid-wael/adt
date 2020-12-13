class AdtException(Exception):
    pass


class DoesNotExist(AdtException):
    pass


class TreeException(AdtException):
    pass


class InvalidChild(TreeException):
    pass


class NodeNotFound(DoesNotExist, TreeException):
    pass
