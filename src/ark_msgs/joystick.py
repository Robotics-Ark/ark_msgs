from ark_msgs.registry import msgs

# joystick_pb2.py is generated from joystick.proto
from .joystick_pb2 import Joystick

def get(self: Joystick, name: str):
    """
    Get axis or button value by name.
    Returns the value if found in axis_name or button_name arrays.
    """
    # Check axis names
    for i, axis_name in enumerate(self.axis_name):
        if axis_name == name:
            if i < len(self.axis):
                return self.axis[i]
    
    # Check button names
    for i, button_name in enumerate(self.button_name):
        if button_name == name:
            if i < len(self.button):
                return self.button[i]
    
    raise KeyError(f"Name '{name}' not found in axis_name or button_name")

if not hasattr(Joystick, "get"):
    Joystick.get = get

msgs.register_item(Joystick)

__all__ = ["Joystick"]
