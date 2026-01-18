import numpy as np
from ark_msgs.translation import Translation
from ark_msgs.rotation import Rotation
from .transform_pb2 import Transform


def _as_matrix(t: Transform | np.ndarray) -> np.ndarray:
    """Convert to a 4x4 homogenous transformation matrix with dtype float32."""
    if isinstance(t, np.ndarray):
        return t.astype(np.float32).reshape(4, 4)
    m = np.eye(4, dtype=np.float32)
    m[:3, :3] = t.rotation.as_matrix()
    m[:3, 3] = t.translation.as_array()
    return m


def _as_proto(m: Transform | np.ndarray, *, child_id: str, parent_id: str) -> Transform:
    """Represent a 4x4 matrix as a Transform."""
    if isinstance(m, Transform):
        return m
    m = np.asarray(m, dtype=np.float32).reshape(4, 4)
    return Transform(
        translation=Translation.from_array(m[:3, 3]),
        rotation=Rotation.from_matrix(m[:3, :3]),
        child_id=child_id,
        parent_id=parent_id,
    )


@classmethod
def from_matrix(
    cls,
    matrix: np.ndarray,
    child_id: str = "child",
    parent_id: str = "parent",
) -> Transform:
    return _as_proto(
        matrix,
        child_id=child_id,
        parent_id=parent_id,
    )


def as_matrix(self: Transform) -> np.ndarray:
    return _as_matrix(self)


def __mul__(self: Transform, other: Transform | np.ndarray) -> Transform:
    """Compose rigid transforms. Note, you need to assign the child_id and parent_id manually."""
    m = _as_matrix(self) @ _as_matrix(other)
    return Transform(
        translation=Translation.from_array(m[:3, 3]),
        rotation=Rotation.from_matrix(m[:3, :3]),
    )


def __rmul__(self: Transform, other: Transform | np.ndarray) -> Transform:
    """Right-hand transform composition. Note, you need to assign the child_id and parent_id manually."""
    m = _as_matrix(other) @ _as_matrix(self)
    return Transform(
        translation=Translation.from_array(m[:3, 3]),
        rotation=Rotation.from_matrix(m[:3, :3]),
    )


def inv(self: Transform) -> Transform:
    """Invert this transform."""
    R = self.rotation.as_matrix()  # (3, 3)
    t = self.translation.as_array()  # (3,)

    R_inv = R.T
    t_inv = -R_inv @ t

    m = np.eye(4, dtype=np.float32)
    m[:3, :3] = R_inv
    m[:3, 3] = t_inv

    return _as_proto(
        m,
        parent_id=self.child_id,
        child_id=self.parent_id,
    )


if not hasattr(Transform, "from_matrix"):
    Transform.from_matrix = from_matrix
if not hasattr(Transform, "as_matrix"):
    Transform.as_matrix = as_matrix
if not hasattr(Transform, "__mul__"):
    Transform.__mul__ = __mul__
if not hasattr(Transform, "__rmul__"):
    Transform.__rmul__ = __rmul__
if not hasattr(Transform, "inv"):
    Transform.inv = inv


__all__ = ["Transform"]
