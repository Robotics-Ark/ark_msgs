from ark_msgs.registry import msgs

from .bool_pb2 import Bool


def __bool__(self):
    return self.data


Bool.__bool__ = __bool__


msgs.register_item(Bool)

__all__ = ["Bool"]
