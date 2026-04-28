from .envelope_pb2 import Envelope
from ark_msgs.registry import msgs
from google.protobuf.message import Message


def extract_message(self: Envelope) -> Message:
    msg_cls = msgs.get(self.msg_type)
    msg = msg_cls()
    msg.ParseFromString(self.payload)
    return msg


if not hasattr(Envelope, "extract_message"):
    Envelope.extract_message = extract_message

msgs.register_item(Envelope)

__all__ = ["Envelope"]
