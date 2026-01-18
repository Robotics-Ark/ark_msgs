import numpy as np
from typing import Iterable, Any
from scipy.spatial.transform import Rotation as Rot

from ._generated.rotation_pb2 import Rotation


def _to_rot(self: Rotation) -> Rot:
    # Protobuf stores [x, y, z, w] (scalar-last), same as SciPy default.
    return Rot.from_quat([float(self.x), float(self.y), float(self.z), float(self.w)])


@classmethod
def from_quat(cls, quat: Iterable[float], *, scalar_first: bool = False) -> Rotation:
    """
    Initialize from quaternions.

    Parameters match SciPy's Rotation.from_quat with scalar_first support.
    """
    q = np.asarray(quat, dtype=np.float64).reshape(4)
    if scalar_first:
        # input is [w, x, y, z] -> convert to [x, y, z, w]
        w, x, y, z = map(float, q)
        return cls(x=x, y=y, z=z, w=w)
    else:
        # input is [x, y, z, w]
        x, y, z, w = map(float, q)
        return cls(x=x, y=y, z=z, w=w)


@classmethod
def from_matrix(cls, matrix: Iterable[Iterable[float]]) -> Rotation:
    """Initialize from rotation matrix."""
    m = np.asarray(matrix, dtype=np.float64).reshape(3, 3)
    r = Rot.from_matrix(m)
    x, y, z, w = map(float, r.as_quat())
    return cls(x=x, y=y, z=z, w=w)


@classmethod
def from_rotvec(cls, rotvec: Iterable[float], degrees: bool = False) -> Rotation:
    """Initialize from rotation vectors."""
    v = np.asarray(rotvec, dtype=np.float64).reshape(3)
    r = Rot.from_rotvec(v, degrees=degrees)
    x, y, z, w = map(float, r.as_quat())
    return cls(x=x, y=y, z=z, w=w)


@classmethod
def from_mrp(cls, mrp: Iterable[float]) -> Rotation:
    """Initialize from Modified Rodrigues Parameters (MRPs)."""
    p = np.asarray(mrp, dtype=np.float64).reshape(3)
    r = Rot.from_mrp(p)
    x, y, z, w = map(float, r.as_quat())
    return cls(x=x, y=y, z=z, w=w)


@classmethod
def from_euler(cls, seq: str, angles: Any, degrees: bool = False) -> Rotation:
    """Initialize from Euler angles."""
    r = Rot.from_euler(seq, angles, degrees=degrees)
    x, y, z, w = map(float, r.as_quat())
    return cls(x=x, y=y, z=z, w=w)


@classmethod
def from_davenport(
    cls,
    axes: Any,
    order: Any,
    angles: Any,
    degrees: bool = False,
    **kwargs: Any,
) -> Rotation:
    """
    Initialize from Davenport angles.

    This passes through to scipy.spatial.transform.Rotation.from_davenport if present.
    """
    if not hasattr(Rot, "from_davenport"):
        raise NotImplementedError(
            "scipy.spatial.transform.Rotation.from_davenport is not available "
            "in your installed SciPy version."
        )
    r = Rot.from_davenport(axes, order, angles, degrees=degrees, **kwargs)
    x, y, z, w = map(float, r.as_quat())
    return cls(x=x, y=y, z=z, w=w)


def as_quat(
    self: Rotation, canonical: bool = False, *, scalar_first: bool = False
) -> np.ndarray:
    """
    Represent as quaternions.

    Matches SciPy's Rotation.as_quat with canonical and scalar_first support.
    """
    r = _to_rot(self)
    q = r.as_quat(canonical=canonical)  # SciPy returns scalar-last [x, y, z, w]
    if scalar_first:
        # [x, y, z, w] -> [w, x, y, z]
        q = np.asarray([q[3], q[0], q[1], q[2]], dtype=q.dtype)
    return q


def as_matrix(self: Rotation) -> np.ndarray:
    """Represent as rotation matrix."""
    return _to_rot(self).as_matrix()


def as_rotvec(self: Rotation, degrees: bool = False) -> np.ndarray:
    """Represent as rotation vectors."""
    return _to_rot(self).as_rotvec(degrees=degrees)


def as_mrp(self: Rotation) -> np.ndarray:
    """Represent as Modified Rodrigues Parameters (MRPs)."""
    return _to_rot(self).as_mrp()


def as_euler(self: Rotation, seq: str, degrees: bool = False) -> np.ndarray:
    """Represent as Euler angles."""
    return _to_rot(self).as_euler(seq, degrees=degrees)


def as_davenport(
    self: Rotation, axes: Any, order: Any, degrees: bool = False, **kwargs: Any
) -> np.ndarray:
    """
    Represent as Davenport angles.

    This passes through to scipy.spatial.transform.Rotation.as_davenport if present.
    """
    r = _to_rot(self)
    if not hasattr(r, "as_davenport"):
        raise NotImplementedError(
            "scipy.spatial.transform.Rotation.as_davenport is not available "
            "in your installed SciPy version."
        )
    return r.as_davenport(axes, order, degrees=degrees, **kwargs)


def inv(self: Rotation) -> Rotation:
    """Invert this rotation."""
    r_inv = _to_rot(self).inv()
    x, y, z, w = map(float, r_inv.as_quat())
    return Rotation(x=x, y=y, z=z, w=w)


def magnitude(self: Rotation) -> float:
    """Get the magnitude of the rotation (in radians)."""
    return float(_to_rot(self).magnitude())


def approx_equal(
    self: Rotation, other: Rotation, atol: float = 1e-8, **kwargs: Any
) -> bool:
    """
    Determine if another rotation is approximately equal to this one.

    Uses SciPy's approx_equal when available; otherwise falls back to comparing
    the relative rotation magnitude against atol (radians).
    """
    r1 = _to_rot(self)
    r2 = _to_rot(other)
    if hasattr(r1, "approx_equal"):
        return bool(r1.approx_equal(r2, atol=atol, **kwargs))
    rel = r1.inv() * r2
    return bool(rel.magnitude() <= atol)


@classmethod
def identity(cls, num: int | None = None) -> Rotation | list[Rotation]:
    """
    Get identity rotation(s).

    If num is None: returns a single Rotation message.
    If num is an int: returns a list of Rotation messages of length num.
    """
    r = Rot.identity(num=num)
    q = r.as_quat()
    if num is None:
        x, y, z, w = map(float, q)
        return cls(x=x, y=y, z=z, w=w)
    out: list[Rotation] = []
    for qi in np.asarray(q):
        x, y, z, w = map(float, qi)
        out.append(cls(x=x, y=y, z=z, w=w))
    return out


@classmethod
def random(cls, num: int | None = None, rng: Any = None) -> Rotation | list[Rotation]:
    """
    Generate uniformly distributed rotations.

    Mimics SciPy's Rotation.random; `rng` is passed as SciPy's `random_state`.
    """
    r = Rot.random(num=num, random_state=rng)
    q = r.as_quat()
    if num is None:
        x, y, z, w = map(float, q)
        return cls(x=x, y=y, z=z, w=w)
    out: list[Rotation] = []
    for qi in np.asarray(q):
        x, y, z, w = map(float, qi)
        out.append(cls(x=x, y=y, z=z, w=w))
    return out


# Monkeypatch onto the generated protobuf class (only if missing)
if not hasattr(Rotation, "from_quat"):
    Rotation.from_quat = from_quat
if not hasattr(Rotation, "from_matrix"):
    Rotation.from_matrix = from_matrix
if not hasattr(Rotation, "from_rotvec"):
    Rotation.from_rotvec = from_rotvec
if not hasattr(Rotation, "from_mrp"):
    Rotation.from_mrp = from_mrp
if not hasattr(Rotation, "from_euler"):
    Rotation.from_euler = from_euler
if not hasattr(Rotation, "from_davenport"):
    Rotation.from_davenport = from_davenport

if not hasattr(Rotation, "as_quat"):
    Rotation.as_quat = as_quat
if not hasattr(Rotation, "as_matrix"):
    Rotation.as_matrix = as_matrix
if not hasattr(Rotation, "as_rotvec"):
    Rotation.as_rotvec = as_rotvec
if not hasattr(Rotation, "as_mrp"):
    Rotation.as_mrp = as_mrp
if not hasattr(Rotation, "as_euler"):
    Rotation.as_euler = as_euler
if not hasattr(Rotation, "as_davenport"):
    Rotation.as_davenport = as_davenport

if not hasattr(Rotation, "inv"):
    Rotation.inv = inv
if not hasattr(Rotation, "magnitude"):
    Rotation.magnitude = magnitude
if not hasattr(Rotation, "approx_equal"):
    Rotation.approx_equal = approx_equal

if not hasattr(Rotation, "identity"):
    Rotation.identity = identity
if not hasattr(Rotation, "random"):
    Rotation.random = random

__all__ = ["Rotation"]
