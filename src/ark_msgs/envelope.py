from .envelope_pb2 import Envelope
from ark_msgs.registry import msgs
from google.protobuf.message import Message


def _extract_message(msg: Envelope) -> Message:
    msg_cls = msgs.get(msg.msg_type)
    inner_msg = msg_cls()
    inner_msg.ParseFromString(msg.payload)
    return inner_msg


def extract_message(self: Envelope) -> Message:
    return _extract_message(self)


def extract_request_message(self: Envelope) -> Message:
    return _extract_message(self.req_msg)


if not hasattr(Envelope, "extract_message"):
    Envelope.extract_message = extract_message
if not hasattr(Envelope, "extract_request_message"):
    Envelope.extract_request_message = extract_request_message

msgs.register_item(Envelope)

__all__ = ["Envelope"]
