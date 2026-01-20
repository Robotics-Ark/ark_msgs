import numpy as np
from ark_msgs.registry import msgs

# image_pb2.py is generated from image.proto
from .image_pb2 import Image

@classmethod
def from_array(cls, array: np.ndarray, encoding: str = "rgb8") -> Image:
    """
    Initialize from a numpy array (e.g. from OpenCV).
    Assumes encoding matches array shape/type.
    """
    array = np.asarray(array)
    height, width = array.shape[:2]
    step = array.strides[0]
    data = array.tobytes()
    return cls(
        height=height,
        width=width,
        encoding=encoding,
        step=step,
        data=data
    )

def as_array(self: Image, dtype=np.uint8) -> np.ndarray:
    """
    Convert to a numpy array.
    """
    shape = (self.height, self.width, -1)
    if self.encoding == "mono8":
         shape = (self.height, self.width)
    return np.frombuffer(self.data, dtype=dtype).reshape(shape)

if not hasattr(Image, "from_array"):
    Image.from_array = from_array
if not hasattr(Image, "as_array"):
    Image.as_array = as_array

msgs.register_item(Image)

__all__ = ["Image"]
