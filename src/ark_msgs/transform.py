import numpy as np
from ark_msgs.translation import Translation
from ark_msgs.rotation import Rotation
from .transform_pb2 import Transform


@classmethod
def from_matrix(
    cls,
    matrix: np.ndarray,
    child_id: str = "child",
    parent_id: str = "parent",
) -> Transform:
    """Create a Transform message from a 4x4 transformation matrix.

    Args:
        matrix (np.ndarray): A 4x4 transformation matrix.
        child_id (str, optional): The child frame ID. Defaults to "child".
        parent_id (str, optional): The parent frame ID. Defaults to "parent".

    Returns:
        Transform: The corresponding Transform message.
    """
    matrix = np.asarray(matrix, dtype=np.float32).reshape(4, 4)
    translation = Translation.from_array(matrix[:3, 3])
    rotation = Rotation.from_matrix(matrix[:3, :3])
    return cls(
        translation=translation,
        rotation=rotation,
        child_id=child_id,
        parent_id=parent_id,
    )


def as_matrix(self: Transform) -> np.ndarray:
    """Convert the Transform message to a 4x4 transformation matrix.

    Returns:
        np.ndarray: A 4x4 transformation matrix.
    """
    matrix = np.eye(4, dtype=np.float32)
    matrix[:3, :3] = self.rotation.as_matrix()
    matrix[:3, 3] = self.translation.as_array()
    return matrix


if not hasattr(Transform, "from_matrix"):
    Transform.from_matrix = from_matrix

if not hasattr(Transform, "as_matrix"):
    Transform.as_matrix = as_matrix


__all__ = ["Transform"]
