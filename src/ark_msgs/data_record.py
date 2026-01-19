from .data_record_pb2 import DataRecord
from ark_msgs.registry import msgs

msgs.register_item(DataRecord)

__all__ = ["DataRecord"]
