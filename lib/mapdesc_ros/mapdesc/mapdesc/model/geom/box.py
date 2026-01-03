import dataclasses
import numpy as np

from .vector2 import Vector2
from .vector3 import Vector3
from .dimension import Dimension
from .pose import Pose


@dataclasses.dataclass
class Box:
    pose: Pose = dataclasses.field(default_factory=Pose)
    size: Dimension = dataclasses.field(default_factory=Dimension)

    def __post_init__(self):
        if isinstance(self.pose, dict):
            # pylint: disable=not-a-mapping
            self.pose = Pose(**self.pose)
        if isinstance(self.size, dict):
            # pylint: disable=not-a-mapping
            self.size = Dimension(**self.size)
        elif isinstance(self.size, (list, tuple, set)):
            self.size = Dimension(*self.size)

    @property
    def points(self):
        # return points counter clockwise sorted points defining the outer
        # hull in 2d
        return [
            Vector2(-self.size.width/2, self.size.length/2),
            Vector2(-self.size.width/2, -self.size.length/2),
            Vector2(self.size.width/2, -self.size.length/2),
            Vector2(self.size.width/2, self.size.length/2)
        ]

    def local_points(self):
        # apply pose (translate by position and rotate by orientation)
        points = []
        # 1. rotate by orientation
        # all points are centered/we rotate around x=0, y=0
        # returns a 3x3 matrix that we can multiply with our coordinates
        matrix = self.pose.orientation.rotation_matrix()
        for point in self.points:
            if isinstance(point, Vector3):
                point = list(point)
            elif isinstance(point, Vector2):
                point = list(point) + [0.0]
            dot = np.dot(matrix, point)
            points.append(Vector2(*dot[:2]))
        # 2. translate by position (only x and y coordinates)
        pose_2d = Vector3(self.pose.position.x, self.pose.position.y)
        points = [p + pose_2d for p in points]
        return points

    def __iter__(self):
        yield ('pose', dict(self.pose))
        if self.size:
            yield ('size', tuple(self.size))

    def copy(self):
        return Box(**dict(self))
