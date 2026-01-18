# Ark Messages

The `ark_msgs` package provides a set of protobuf-based message definitions and lightweight Python helpers used throughout the Ark framework.

In `ark_msgs`, we use monkeypatching to add convenience methods directly to the generated protobuf message classes. 
Protobuf code is auto-generated and should not be edited by hand, but many applications benefit from rich, domain-specific helpers (e.g. quaternion and rotation conversions). 
Monkeypatching allows us to extend the `Rotation` message with a SciPy-compatible API while keeping the generated files untouched and fully regenerable. This provides a clean, familiar interface without introducing wrapper types or duplicating data structures.