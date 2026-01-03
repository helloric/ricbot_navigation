from dataclasses import dataclass, field
from .quaternion import Quaternion
from .vector2 import Vector2
from .vector3 import Vector3


def list_to_vector(data):
    """Creates a Vector or Quaternion from a list by the list size."""
    if len(data) == 2:
        return Vector2(*data)
    if len(data) == 3:
        return Vector3(*data)
    if len(data) == 4:
        return Quaternion(*data)
    raise RuntimeError(f'data for vector should be of length 2-4: {data}')


def dict_to_vector(data):
    """Creates a Vector or Quaternion from a dict.

    Needs at least x and y for a 2d pose, creates a 3D-vector for x, y, z
    and a Quaternion if w is also given.
    """
    if 'x' not in data or 'y' not in data:
        raise RuntimeError('x and y not set, not a valid pose.')
    if 'w' in data:
        return Quaternion(**data)
    if 'z' in data:
        return Vector3(**data)
    return Vector2(**data)


def any_to_vector(data):
    """converts any data to a vector or Quaternion if possible.

    see @dict_to_vector and @list_to_vector.
    """
    if isinstance(data, (list, tuple, set)):
        return list_to_vector(data)
    if isinstance(data, dict):
        return dict_to_vector(data)
    if isinstance(data, (Vector2, Vector3, Quaternion)):
        return data
    raise RuntimeError(f'unknown vector type {type(data)} ({data})')


@dataclass
class Pose:
    """Describes the pose of an object.

    (defined by its position and orientation)."""
    position: Vector3 = field(default_factory=Vector3)
    orientation: Quaternion = field(default_factory=Quaternion)
    _euler_orientation: Vector3 = field(default_factory=Vector3)

    def __post_init__(self):
        if self.orientation:
            self.orientation = any_to_vector(self.orientation)
        if self.position:
            self.position = any_to_vector(self.position)

    def euler_orientation(self):
        """Create euler orientation from Quaternion.

        Caches the generated euler orientation to a local _euler_orientation.
        Note that it might be different from the given orientation-quaternion.
        """
        if isinstance(self.orientation, Quaternion):
            self._euler_orientation = self.orientation.to_euler()
        elif isinstance(self.orientation, Vector3):
            self._euler_orientation = self.orientation
        return self._euler_orientation

    def __iter__(self):
        yield ('orientation', tuple(self.orientation))
        yield ('position', tuple(self.position))

    def copy(self):
        """copy values from current Pose to a new Pose-instance."""
        return Pose(**dict(self))
