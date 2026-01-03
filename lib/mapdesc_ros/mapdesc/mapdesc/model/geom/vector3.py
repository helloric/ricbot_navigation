import dataclasses
import math
from .vector2 import Vector2


@dataclasses.dataclass
class Vector3(Vector2):
    z: float = 0.0

    def __init__(self, x=0.0, y=0.0, z=0.0, *args, **kwargs):
        super().__init__(x, y)
        self.z = z

    def __getitem__(self, idx):
        if idx in [2, 'z']:
            return self.z
        return super().__getitem__(idx)

    def __iter__(self):
        """ Helper to create a tuple from this """
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, o):
        if isinstance(o, Vector3):
            return Vector3(self.x + o.x, self.y + o.y, self.z + o.z)
        else:
            return Vector3(*[val + o for val in self])

    def __sub__(self, o):
        if isinstance(o, Vector3):
            return Vector3(self.x - o.x, self.y - o.y, self.z - o.z)
        else:
            return Vector3(*[val - o for val in self])

    def __mul__(self, o):
        """ Scalar multiplication """
        if isinstance(o, Vector3):
            return Vector3(self.x * o.x, self.y * o.y, self.z * o.z)
        else:
            return Vector3(*[val * o for val in self])

    def __neg__(self):
        """ Returns a vector pointing in the opposite direction """
        return Vector3(*[-val for val in self])

    def __round__(self, num):
        return Vector3(
            round(self.x, num),
            round(self.y, num),
            round(self.z, num))

    def normalize(self):
        """ Normalizes the vector to have unit length """
        return Vector3(*[q / self.magnitude() for q in self])

    def copy(self):
        return Vector3(self.x, self.y, self.y)

    def is_close(self, o, rel_tol=0.01, abs_tol=0.01, threshold=None):
        """ Check if a Vector3 is close to another Vector3. """
        if not o:
            return False
        if isinstance(o, dict):
            x, y, z = o['x'], o['y'], o['z']
        elif isinstance(o, (list, tuple, set)):
            x, y, z = o
        else:
            x, y, z = o.x, o.y, o.z
        if threshold:
            return abs(self.x - x) + abs(self.y - y) + abs(self.z - z) < \
                threshold
        return math.isclose(
                self.x, x, rel_tol=rel_tol, abs_tol=abs_tol) and \
            math.isclose(
                self.y, y, rel_tol=rel_tol, abs_tol=abs_tol) and \
            math.isclose(
                self.z, z, rel_tol=rel_tol, abs_tol=abs_tol)

    @staticmethod
    def from_any(lst):
        if isinstance(lst, Vector3):
            return lst
        if isinstance(lst, (list, tuple, set)):
            return Vector3(*lst)
        if isinstance(lst, dict):
            return Vector3(**lst)
        raise RuntimeError('given data neither list nor dict')

    def midpoint(self, other):
        """Return a midpoint between the two points."""
        return Vector3(
            (self.x + other.x) / 2,
            (self.y + other.y) / 2,
            (self.z + other.z) / 2)
