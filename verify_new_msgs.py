
from ark_msgs.twist import Twist
from ark_msgs.wrench import Wrench
from ark_msgs.image import Image
from ark_msgs.joystick import Joystick
from ark_msgs.imu import Imu
from ark_msgs.parallel_gripper_command import ParallelGripperCommand
from ark_msgs.joint_array_command import JointArrayCommand
from ark_msgs.rotation import Rotation
from ark_msgs.translation import Translation
import numpy as np

print("Testing all new messages...")

# 1. Twist
print("Testing Twist...")
twist = Twist.from_array([1.0, 2.0, 3.0, 0.1, 0.2, 0.3])
assert np.isclose(twist.linear.x, 1.0)
assert np.isclose(twist.angular.z, 0.3)

# 2. Wrench
print("Testing Wrench...")
wrench = Wrench.from_array([10.0, 0.0, 0.0, 0.0, 0.0, 1.0])
assert np.isclose(wrench.force.x, 10.0)

# 3. Image
print("Testing Image...")
img_data = np.zeros((10, 10, 3), dtype=np.uint8)
img = Image.from_array(img_data)
assert img.height == 10
assert img.width == 10
assert img.encoding == "rgb8"
# Check is_bigendian (0 for little endian/standard numpy on x86)
# If running on ARM/Big Endian it might be 1.
print(f"Image bigendian: {img.is_bigendian}") 
reconstructed = img.as_array()
assert reconstructed.shape == (10, 10, 3)

# 4. Joystick
print("Testing Joystick...")
joy = Joystick(axes=[0.0, 1.0], buttons=[0, 1])
assert len(joy.axes) == 2
assert joy.buttons[1] == 1

# 5. IMU
print("Testing IMU...")
imu = Imu(
    orientation=Rotation.identity(),
    angular_velocity=Translation(x=0.0, y=0.0, z=0.1),
    linear_acceleration=Translation(x=0.0, y=0.0, z=9.8)
)
assert imu.orientation.w == 1.0
assert np.isclose(imu.linear_acceleration.z, 9.8)

# 6. Parallel Gripper
print("Testing Gripper...")
grip = ParallelGripperCommand(width=0.05, max_force=10.0)
assert np.isclose(grip.width, 0.05)

# 7. Joint Array
print("Testing Joint Array...")
cmd = JointArrayCommand(
    name=["j1", "j2"],
    value=[0.1, 0.2],
    mode=JointArrayCommand.Mode.POSITION
)
assert cmd.mode == JointArrayCommand.Mode.POSITION
assert np.isclose(cmd.value[1], 0.2)

print("All verifications successful!")
