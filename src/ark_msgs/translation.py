import numpy as np
from typing import Iterable
from ._generated.translation_pb2 import Translation


@classmethod
def from_array(cls, array: Iterable[float]) -> Translation:
    """Initialize from an array-like of three floats."""
    arr = np.asarray(array, dtype=np.float32).reshape(3)
    return cls(x=float(arr[0]), y=float(arr[1]), z=float(arr[2]))


def as_array(self: Translation) -> np.ndarray:
    """Represent as a numpy array of shape (3,)."""
    return np.array([self.x, self.y, self.z], dtype=np.float32)


if not hasattr(Translation, "from_array"):
    Translation.from_array = from_array

if not hasattr(Translation, "as_array"):
    Translation.as_array = as_array

__all__ = ["Translation"]
