from ark_msgs.registry import msgs

# joint_array_command_pb2.py is generated from joint_array_command.proto
from .joint_array_command_pb2 import JointArrayCommand

msgs.register_item(JointArrayCommand)

__all__ = ["JointArrayCommand"]
