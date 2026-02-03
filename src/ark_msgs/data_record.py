from ark_msgs.registry import msgs

# data_record_pb2.py is generated from data_record.proto
from .data_record_pb2 import DataRecord

msgs.register_item(DataRecord)

__all__ = ["DataRecord"]
