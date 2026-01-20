from ark_msgs.registry import msgs

# joystick_pb2.py is generated from joystick.proto
from .joystick_pb2 import Joystick

msgs.register_item(Joystick)

__all__ = ["Joystick"]
