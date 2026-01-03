from dataclasses import dataclass

from ...util import quaternion_to_euler
from .vector3 import Vector3


@dataclass
class Quaternion(Vector3):
    # a quaternion describes rotation in radians.
    w: float = 1.0

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0, *args, **kwargs):
        super().__init__(x, y, z)
        self.w = w

    def __iter__(self):
        """ Helper to create a tuple from this """
        yield self.x
        yield self.y
        yield self.z
        yield self.w

    def __getitem__(self, idx):
        if idx in [3, 'w']:
            return self.w
        return super().__getitem__(idx)

    def __add__(self, o):
        if isinstance(o, Quaternion):
            return Quaternion(
                self.x + o.x, self.y + o.y, self.z + o.z, self.w + o.w)
        else:
            return Quaternion(*[val + o for val in self])

    def __sub__(self, o):
        if isinstance(o, Quaternion):
            return Quaternion(
                self.x - o.x, self.y - o.y, self.z - o.z, self.w - o.w)
        else:
            return Quaternion(*[val - o for val in self])

    def __mul__(self, o):
        """ Scalar multiplication """
        if isinstance(o, Quaternion):
            return Quaternion(
                self.x * o.x, self.y * o.y, self.z * o.z, self.w * o.w)
        else:
            return Quaternion(*[val * o for val in self])

    def __neg__(self):
        """ Returns a vector pointing in the opposite direction """
        return Quaternion(*[-val for val in self])

    def normalize(self):
        """ Normalizes the vector to have unit length """
        mag = self.magnitude()
        if not mag:
            raise RuntimeError(
                f'Can not normalize null quaternion {self}')
        return Quaternion(*[q / mag for q in self])

    def copy(self):
        return Quaternion(self.x, self.y, self.z, self.w)

    @staticmethod
    def from_any(lst):
        if isinstance(lst, Quaternion):
            return lst
        if isinstance(lst, (list, tuple)):
            return Quaternion(*lst[:4])
        elif isinstance(lst, dict):
            return Quaternion(**lst)
        else:
            raise RuntimeError('given data neither list nor dict')

    def rotation_matrix(self) -> list:
        # see https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#
        #     Conversion_to_and_from_the_matrix_representation

        # get a normalized copy of the quaternion
        quat = self.normalize()

        # Calculate the elements of the rotation matrix
        w, x, y, z = quat.w, quat.x, quat.y, quat.z
        xx = x * x
        xy = x * y
        xz = x * z
        yy = y * y
        yz = y * z
        zz = z * z
        wx = w * x
        wy = w * y
        wz = w * z

        # Construct and return the rotation matrix
        return [[1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
                [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
                [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)]]

    def to_euler(self):
        e = Vector3()
        e.x, e.y, e.z = quaternion_to_euler(self.x, self.y, self.z, self.w)
        return e
