import numpy as np
from ark_msgs.translation import Translation
from ark_msgs.rotation import Rotation
from scipy.spatial.transform import (
    RigidTransform as ScipyRigidTransform,
    Rotation as ScipyRotation,
)
from ark_msgs.registry import msgs

# rigid_transform_pb2.py is generated from rigid_transform.proto
from .rigid_transform_pb2 import RigidTransform

ProtoOrScipyRigidTransform = RigidTransform | ScipyRigidTransform


def _as_scipy(t: ProtoOrScipyRigidTransform) -> ScipyRigidTransform:
    """Convert to scipy.spatial.transform.RigidTransform."""
    if isinstance(t, ScipyRigidTransform):
        return t
    m = np.eye(4, dtype=np.float32)
    m[:3, :3] = t.rotation.as_matrix()
    m[:3, 3] = t.translation.as_array()
    return ScipyRigidTransform.from_matrix(m)


def _as_proto(
    t: ProtoOrScipyRigidTransform, *, child_id: str = "child", parent_id: str = "parent"
) -> RigidTransform:
    """Convert to ark_msgs.rigid_transform.RigidTransform."""
    if isinstance(t, RigidTransform):
        return t
    return RigidTransform(
        translation=Translation.from_array(t.translation),
        rotation=Rotation.from_matrix(t.rotation.as_matrix()),
        child_id=child_id,
        parent_id=parent_id,
    )


@classmethod
def from_matrix(
    cls,
    matrix: np.ndarray,
    child_id: str = "child",
    parent_id: str = "parent",
) -> RigidTransform:
    matrix = np.asarray(matrix, dtype=np.float32).reshape(4, 4)
    t = ScipyRigidTransform.from_matrix(matrix)
    return _as_proto(t, child_id=child_id, parent_id=parent_id)


@classmethod
def from_rotation(
    cls,
    rotation: Rotation | ScipyRotation,
    child_id: str = "child",
    parent_id: str = "parent",
) -> RigidTransform:
    t = ScipyRigidTransform.from_rotation(ScipyRotation.from_quat(rotation.as_quat()))
    return _as_proto(t, child_id=child_id, parent_id=parent_id)


@classmethod
def from_translation(
    cls,
    translation: Translation | np.ndarray,
    child_id: str = "child",
    parent_id: str = "parent",
) -> RigidTransform:
    t = ScipyRigidTransform.from_translation(
        translation.as_array() if isinstance(translation, Translation) else translation
    )
    return _as_proto(t, child_id=child_id, parent_id=parent_id)


@classmethod
def from_components(
    cls,
    translation: Translation | np.ndarray,
    rotation: Rotation | ScipyRotation,
    child_id: str = "child",
    parent_id: str = "parent",
) -> RigidTransform:
    tr = translation.as_array() if isinstance(translation, Translation) else translation
    r = rotation.as_matrix() if isinstance(rotation, Rotation) else rotation
    t = ScipyRigidTransform.from_components(translation=tr, rotation=r)
    return _as_proto(t, child_id=child_id, parent_id=parent_id)


@classmethod
def from_exp_coords(
    cls, exp_coords: np.ndarray, child_id: str = "child", parent_id: str = "parent"
) -> RigidTransform:
    """Initialize from exponential coordinates (6,)."""
    exp_coords = np.asarray(exp_coords, dtype=np.float32).reshape(6)
    t = ScipyRigidTransform.from_exp(exp_coords)
    return _as_proto(t, child_id=child_id, parent_id=parent_id)


@classmethod
def from_dual_quat(
    cls,
    dual_quat: np.ndarray,
    *,
    scalar_first: bool = True,
    child_id: str = "child",
    parent_id: str = "parent",
) -> RigidTransform:
    """Initialize from dual quaternion (8,)."""
    dual_quat = np.asarray(dual_quat, dtype=np.float32).reshape(8)
    t = ScipyRigidTransform.from_dual_quat(dual_quat, scalar_first=scalar_first)
    return _as_proto(t, child_id=child_id, parent_id=parent_id)


def as_matrix(self: RigidTransform) -> np.ndarray:
    return _as_scipy(self).as_matrix()


def as_components(self: RigidTransform, proto: bool = False) -> tuple:
    """Return translation and rotation components. If proto is True, return ark_msgs types."""
    t = _as_scipy(self)
    if proto:
        translation = Translation.from_array(t.translation)
        rotation = Rotation.from_matrix(t.rotation.as_matrix())
        return translation, rotation
    return t.translation, t.rotation.as_matrix()


def as_exp_coords(self: RigidTransform) -> np.ndarray:
    """Return exponential coordinates (6,)."""
    return _as_scipy(self).as_exp()


def as_dual_quat(self: RigidTransform, *, scalar_first: bool = True) -> np.ndarray:
    """Return dual quaternion (8,)."""
    return _as_scipy(self).as_dual_quat(scalar_first=scalar_first)


def __mul__(self: RigidTransform, other: RigidTransform | np.ndarray) -> RigidTransform:
    """Compose rigid transforms. Note, you need to assign the child_id and parent_id manually."""
    t = _as_scipy(self) @ _as_scipy(other)
    return _as_proto(t)


def __rmul__(
    self: RigidTransform, other: RigidTransform | np.ndarray
) -> RigidTransform:
    """Right-hand transform composition. Note, you need to assign the child_id and parent_id manually."""
    t = _as_scipy(other) @ _as_scipy(self)
    return _as_proto(t)


def inv(self: RigidTransform) -> RigidTransform:
    """Invert this transform."""
    t = _as_scipy(self).inv()
    return _as_proto(t, parent_id=self.child_id, child_id=self.parent_id)


if not hasattr(RigidTransform, "from_matrix"):
    RigidTransform.from_matrix = from_matrix
if not hasattr(RigidTransform, "from_rotation"):
    RigidTransform.from_rotation = from_rotation
if not hasattr(RigidTransform, "from_translation"):
    RigidTransform.from_translation = from_translation
if not hasattr(RigidTransform, "from_components"):
    RigidTransform.from_components = from_components
if not hasattr(RigidTransform, "from_exp_coords"):
    RigidTransform.from_exp_coords = from_exp_coords
if not hasattr(RigidTransform, "from_dual_quat"):
    RigidTransform.from_dual_quat = from_dual_quat

if not hasattr(RigidTransform, "as_matrix"):
    RigidTransform.as_matrix = as_matrix
if not hasattr(RigidTransform, "as_components"):
    RigidTransform.as_components = as_components
if not hasattr(RigidTransform, "as_exp_coords"):
    RigidTransform.as_exp_coords = as_exp_coords
if not hasattr(RigidTransform, "as_dual_quat"):
    RigidTransform.as_dual_quat = as_dual_quat

if not hasattr(RigidTransform, "__mul__"):
    RigidTransform.__mul__ = __mul__
if not hasattr(RigidTransform, "__rmul__"):
    RigidTransform.__rmul__ = __rmul__
if not hasattr(RigidTransform, "inv"):
    RigidTransform.inv = inv

msgs.register_item(RigidTransform)

__all__ = ["RigidTransform"]
