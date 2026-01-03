import math

from dataclasses import dataclass, field

from .box import Box
from .dimension import Dimension
from .vector2 import Vector2
from .vector3 import Vector3
from .quaternion import Quaternion
from ...util import ccw_sort, calculate_slope, \
    dot_product, euler_to_quaternion
from .pose import list_to_vector, Pose


@dataclass
class Mesh(Box):
    polygons: list = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.polygons = [
            list_to_vector(poly) if isinstance(poly, (list, tuple)) else poly
            for poly in self.polygons
        ]

    def ccw_sort(self):
        """sort polygon points counter-clockwise."""
        self.polygons = ccw_sort(self.polygons)

    @property
    def points(self):
        return self.polygons

    @staticmethod
    def calculate_position(points, clz=Vector2):
        # if you like to not use the zero-vector as position for the mesh
        # but the center of it you can use this function to calculate the
        # new position. Make sure to subtract the result of this vector
        # from each point.
        if clz == Vector2:
            return Vector2(
                sum([p.x for p in points]) / len(points),
                sum([p.y for p in points]) / len(points))
        elif clz == Vector3:
            return Vector3(
                sum([p.x for p in points]) / len(points),
                sum([p.y for p in points]) / len(points),
                sum([p.z for p in points]) / len(points))
        else:
            raise RuntimeError(
                'Only Vector2 or Vector3 are valid options as class, not '
                f'{clz}')

    def recenter(self):
        clz = self.polygons[0].__class__
        center = Mesh.calculate_position(self.polygons, clz)
        for idx, _ in enumerate(self.polygons):
            self.polygons[idx] -= center
        self.pose.position.x += center.x
        self.pose.position.y += center.y

    def is_rectangle(self):
        p = self.polygons
        if len(p) != 4:
            return False
        slopes = [
            calculate_slope(p[0], p[1]),
            calculate_slope(p[1], p[2]),
            calculate_slope(p[2], p[3]),
            calculate_slope(p[3], p[0])
        ]
        if slopes[0] != slopes[2] or slopes[1] != slopes[3]:
            return False
        # check for right angle using dot product
        if dot_product(p[0], p[1], p[2]) != 0:
            return False
        return True

    def boxify(self):
        if not self.is_rectangle():
            # the mesh has to consist of exactly 4 polygons
            return False
        # recalculate center

        self.recenter()

        p = self.polygons
        # calculate center of points right to the center
        midpoint = p[0].midpoint(p[1])
        width = midpoint.distance(Vector2()) * 2
        length = p[1].midpoint(p[2]).distance(Vector2()) * 2

        rot_z = math.atan2(midpoint.y, midpoint.x)
        quat = euler_to_quaternion(0, 0, rot_z)
        self.pose.orientation = Quaternion(*quat)

        return Box(size=Dimension(width, length), pose=self.pose)

    def bounding_box(self):
        """create a new bounding box around the points."""
        min_x = min([p.x for p in self.polygons])
        max_x = max([p.x for p in self.polygons])
        min_y = min([p.y for p in self.polygons])
        max_y = max([p.y for p in self.polygons])

        size = Dimension()
        size.width = float(max_x - min_x)

        pose = Pose(orientation=self.pose.orientation.copy())
        pose.position.x = float(min_x + max_x) / 2

        pose.position.y = float(min_y + max_y) / 2
        pose.position.z = float(pose.position.z)
        size.length = float(max_y - min_y)

        if isinstance(self.polygons[0], Vector3):
            min_z = min([p.z for p in self.polygons])
            max_z = max([p.z for p in self.polygons])
            pose.position.z = float(min_z + max_z) / 2
            size.height = float(max_z - min_z)

        return Box(pose=pose, size=size)

    def __iter__(self):
        yield from super().__iter__()
        yield ('polygons', [list(p) for p in self.polygons])
