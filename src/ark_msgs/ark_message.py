import zenoh
from ark.clock import Clock
from ark_msgs import msgs
from google.protobuf.message import Message
from ark_msgs.ark_message_pb2 import ArkMessage


@classmethod
def pack(cls: type[ArkMessage], clock: Clock, msg: Message) -> ArkMessage:
    return cls(
        timestamp=clock.now(),
        payload_msg_type=msg.DESCRIPTOR.full_name,
        payload=msg.SerializeToString(),
    )


@classmethod
def from_sample(cls: type[ArkMessage], sample: zenoh.Sample) -> ArkMessage:
    ark_msg = cls()
    ark_msg.ParseFromString(bytes(sample.payload))
    return ark_msg


if not hasattr(ArkMessage, "pack"):
    ArkMessage.pack = pack
if not hasattr(ArkMessage, "from_sample"):
    ArkMessage.from_sample = from_sample

msgs.register_item(ArkMessage)

__all__ = ["ArkMessage"]
