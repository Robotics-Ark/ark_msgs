from ark_msgs.registry import msgs

# parallel_gripper_command_pb2.py is generated from parallel_gripper_command.proto
from .parallel_gripper_command_pb2 import ParallelGripperCommand

msgs.register_item(ParallelGripperCommand)

__all__ = ["ParallelGripperCommand"]
