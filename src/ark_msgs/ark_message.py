from ark_msgs.registry import msgs
from .ark_message_pb2 import ArkMessage

msgs.register_item(ArkMessage)

__all__ = ["ArkMessage"]
