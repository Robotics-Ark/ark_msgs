# Ark Messages

The `ark_msgs` package provides a set of protobuf-based message definitions and lightweight Python helpers used throughout the Ark framework.

In `ark_msgs`, we use monkeypatching to add convenience methods directly to the generated protobuf message classes. 
Protobuf code is auto-generated and should not be edited by hand, but many applications benefit from rich, domain-specific helpers (e.g. quaternion and rotation conversions). 
Monkeypatching allows us to extend the `Rotation` message with a SciPy-compatible API while keeping the generated files untouched and fully regenerable. This provides a clean, familiar interface without introducing wrapper types or duplicating data structures.

# Install

1. Create and activate a conda environment.
2. Clone this repository and change directory `cd ark_msgs`.
3. Install: `pip install -e .`

# Documentation

Documentation for each message type supported in `ark_msgs` can be found below.

## TOC

- [Geometry](https://github.com/Robotics-Ark/ark_msgs/tree/master#geometry)
- [Sensor](https://github.com/Robotics-Ark/ark_msgs/tree/master#sensor)

## Geometry

Common message types involving geometry calculations.
The helper methods for geometry message types are inspired and try to follow (as closely as possible) the [`scipy.spatial.transform` module](https://docs.scipy.org/doc/scipy/reference/spatial.transform.html).

### Translation

`Translation` represents a 3D translation vector with `x`, `y`, and `z` components.

#### Fields

- `x`: X component.
- `y`: Y component.
- `z`: Z component.

All numeric fields use `float32`.

#### Helpers

- `Translation.from_array(array)`  
  Create a `Translation` from an array-like of shape `(3,)`.

- `t.as_array()`  
  Convert to a `numpy.ndarray` of shape `(3,)` with dtype `float32`.

- `t1 + t2`, `t1 + array_like`, `array_like + t1`  
  Vector addition (returns `Translation`).

- `t1 - t2`, `t1 - array_like`, `array_like - t1`  
  Vector subtraction (returns `Translation`).

#### Usage

```python
import numpy as np
from ark_msgs.translation import Translation

t1 = Translation.from_array([1.0, 2.0, 3.0])
arr = t1.as_array()  # -> np.ndarray shape (3,), float32

t2 = Translation(x=0.5, y=0.0, z=-1.0)

t3 = t1 + t2
t4 = t1 - [1.0, 0.0, 0.0]
t5 = np.array([0.0, 1.0, 0.0], dtype=np.float32) + t1
```

### Rotation

`Rotation` represents a 3D rotation as a unit quaternion with components `x`, `y`, `z`, and `w`.

#### Fields

- `x`: Quaternion x component.
- `y`: Quaternion y component.
- `z`: Quaternion z component.
- `w`: Quaternion w (scalar) component.

All numeric fields use `float32`.

#### Helpers

- `Rotation.from_quat(quat, scalar_first=False)`  
  Create from a quaternion. Accepts `[x, y, z, w]` by default, or `[w, x, y, z]` if `scalar_first=True`.

- `Rotation.from_matrix(matrix)`  
  Create from a 3×3 rotation matrix.

- `Rotation.from_rotvec(rotvec, degrees=False)`  
  Create from a rotation vector.

- `Rotation.from_mrp(mrp)`  
  Create from Modified Rodrigues Parameters (MRPs).

- `Rotation.from_euler(seq, angles, degrees=False)`  
  Create from Euler angles.

- `Rotation.from_davenport(axes, order, angles, degrees=False)`  
  Create from Davenport angles.

- `r.as_quat(canonical=False, scalar_first=False)`  
  Convert to quaternion array.

- `r.as_matrix()`  
  Convert to 3×3 rotation matrix.

- `r.as_rotvec(degrees=False)`  
  Convert to rotation vector.

- `r.as_mrp()`  
  Convert to MRPs.

- `r.as_euler(seq, degrees=False, suppress_warnings=False)`  
  Convert to Euler angles.

- `r.as_davenport(axes, order, degrees=False, suppress_warnings=False)`  
  Convert to Davenport angles.

- `r.inv()`  
  Invert the rotation.

- `r.magnitude()`  
  Return rotation magnitude in radians.

- `Rotation.identity()`  
  Identity rotation.

- `Rotation.random(rng=None)`  
  Random rotation (uniformly distributed), optionally using a NumPy `Generator` or integer seed.

- `r1 * r2`, `r1 * Rot`, `Rot * r1`  
  Compose rotations using SciPy semantics: `r = r1 * r2` applies `r2` first, then `r1`.
  The result is always an `ark_msgs.Rotation`.

#### Usage

```python
import numpy as np
from scipy.spatial.transform import Rotation as Rot
from ark_msgs.rotation import Rotation

# Construction
r1 = Rotation.from_euler("z", 90, degrees=True)
r2 = Rotation.from_quat([0.0, 0.0, 0.0, 1.0])

# Conversions
q = r1.as_quat()          # (x, y, z, w)
R = r1.as_matrix()        # 3x3
v = r1.as_rotvec()        # radians

# Composition (apply r2, then r1)
r3 = r1 * r2

# Works with SciPy rotations too (result is protobuf Rotation)
rs = Rot.from_euler("x", 30, degrees=True)
r4 = r1 * rs
r5 = rs * r1

# Inversion / magnitude
r_inv = r1.inv()
angle = r1.magnitude()

# Identity / random
r_id = Rotation.identity()
r_rand = Rotation.random(rng=np.random.default_rng(0))
```

### RigidTransform

`RigidTransform` represents a rigid transform (translation + rotation) between two coordinate frames.

#### Fields

- `translation`: Translation component (`ark_msgs.Translation`).
- `rotation`: Rotation component (`ark_msgs.Rotation`).
- `child_id`: Child frame ID.
- `parent_id`: Parent frame ID.

#### Helpers

- `RigidTransform.from_matrix(matrix, child_id="child", parent_id="parent")`  
  Create from a 4×4 homogeneous transform matrix.

- `RigidTransform.from_rotation(rotation, child_id="child", parent_id="parent")`  
  Create from a rotation (protobuf `Rotation` or SciPy `Rotation`).

- `RigidTransform.from_translation(translation, child_id="child", parent_id="parent")`  
  Create from a translation (protobuf `Translation` or array-like `(3,)`).

- `RigidTransform.from_components(translation, rotation, child_id="child", parent_id="parent")`  
  Create from translation and rotation components.

- `RigidTransform.from_exp_coords(exp_coords, child_id="child", parent_id="parent")`  
  Create from exponential coordinates `(6,)`.

- `RigidTransform.from_dual_quat(dual_quat, scalar_first=True, child_id="child", parent_id="parent")`  
  Create from a dual quaternion `(8,)`.

- `t.as_matrix()`  
  Convert to a 4×4 homogeneous transform matrix.

- `t.as_components(proto=False)`  
  Return `(translation, rotation)` components. If `proto=True`, returns `ark_msgs.Translation` and
  `ark_msgs.Rotation`; otherwise returns SciPy-compatible arrays.

- `t.as_exp_coords()`  
  Convert to exponential coordinates `(6,)`.

- `t.as_dual_quat(scalar_first=True)`  
  Convert to dual quaternion `(8,)`.

- `t1 * t2`, `t1 * matrix`, `matrix * t1`  
  Compose transforms (SciPy semantics). Frame IDs are not propagated; users should assign
  `child_id` and `parent_id` manually if needed.

- `t.inv()`  
  Invert the transform (swaps `parent_id` and `child_id`).

#### Usage

```python
import numpy as np
from ark_msgs.translation import Translation
from ark_msgs.rotation import Rotation
from ark_msgs.rigid_transform import RigidTransform

# Construction
t = Translation.from_array([1.0, 2.0, 3.0])
r = Rotation.from_euler("z", 90, degrees=True)

T1 = RigidTransform.from_components(
    translation=t,
    rotation=r,
    parent_id="world",
    child_id="camera",
)

# Conversions
M = T1.as_matrix()
tr_proto, r_proto = T1.as_components(proto=True)
exp = T1.as_exp_coords()
dq = T1.as_dual_quat()

# Composition (apply T2, then T1)
T2 = RigidTransform.from_translation([0.1, 0.0, 0.0])
T3 = T1 * T2

# Inversion
T_inv = T1.inv()
```

## Sensor

Common sensor message types.

### JointState

`JointState` represents the joint states for a robot at an instance in time. 

#### Fields

- `name`: Joint names.
- `position`: Joint positions (e.g. radians or meters).
- `velocity`: Joint velocities.
- `effort`: Joint efforts or currents (e.g. torque or force or amps)  
- `ext_torque`: External torques acting on the robot joints.

All numeric fields use `float32`. 
Elements at the same index across fields refer to the same joint.

#### Usage

```python
from ark_msgs.joint_state import JointState

js = JointState(
    name=["joint1", "joint2"],
    position=[0.1, 1.57],
    velocity=[0.0, 0.1],
    effort=[0.001, 0.002],
    effort=[-0.2, -0.1],
)
```