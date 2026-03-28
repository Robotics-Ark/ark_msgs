from ark_msgs.registry import msgs

from .string_pb2 import String


def __str__(self):
    return self.data


String.__str__ = __str__

msgs.register_item(String)

__all__ = ["String"]
