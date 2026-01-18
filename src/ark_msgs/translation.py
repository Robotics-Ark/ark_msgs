import numpy as np
from typing import Iterable
from .translation_pb2 import Translation

ProtoOrIterableTranslation = Translation | Iterable[float]


def _as_array(t: ProtoOrIterableTranslation) -> np.ndarray:
    """Convert to numpy array of shape (3,)."""
    if isinstance(t, Translation):
        return np.array([t.x, t.y, t.z], dtype=np.float32)
    return np.asarray(t, dtype=np.float32).reshape(3)


def _as_proto(t: ProtoOrIterableTranslation) -> Translation:
    """Convert to ark_msgs.Translation."""
    if isinstance(t, Translation):
        return t
    t = np.asarray(t, dtype=np.float32).reshape(3)
    return Translation(x=float(t[0]), y=float(t[1]), z=float(t[2]))


@classmethod
def from_array(cls, array: Iterable[float]) -> Translation:
    """Initialize from an array-like of three floats."""
    return _as_proto(array)


def as_array(self: Translation) -> np.ndarray:
    """Convert to a numpy array of shape (3,)."""
    return _as_array(self)


def __add__(
    self: Translation | Iterable[float], other: Translation | Iterable[float]
) -> Translation:
    """
    Add translations.

    Supports:
      - Translation + Translation
      - Translation + array-like (3,)
    """
    return _as_proto(_as_array(self) + _as_array(other))


def __radd__(
    self: Translation | Iterable[float], other: Translation | Iterable[float]
) -> Translation:
    """
    Right-add support for array-like + Translation.
    """
    return _as_proto(_as_array(other) + _as_array(self))


def __sub__(
    self: Translation | Iterable[float], other: Translation | Iterable[float]
) -> Translation:
    """
    Subtract translations.

    Supports:
      - Translation - Translation
      - Translation - array-like (3,)
    """
    return _as_proto(_as_array(self) - _as_array(other))


def __rsub__(
    self: Translation | Iterable[float], other: Translation | Iterable[float]
) -> Translation:
    """
    Right-subtract support for array-like - Translation.
    """
    return _as_proto(_as_array(other) - _as_array(self))


if not hasattr(Translation, "from_array"):
    Translation.from_array = from_array
if not hasattr(Translation, "as_array"):
    Translation.as_array = as_array
if not hasattr(Translation, "__add__"):
    Translation.__add__ = __add__
if not hasattr(Translation, "__radd__"):
    Translation.__radd__ = __radd__
if not hasattr(Translation, "__sub__"):
    Translation.__sub__ = __sub__
if not hasattr(Translation, "__rsub__"):
    Translation.__rsub__ = __rsub__


__all__ = ["Translation"]
