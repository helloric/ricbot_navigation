"""A simple path is just a list of (way-)points.

For a more defined behavior use lanes (see lane.py).
"""
from dataclasses import dataclass, field
from .geom.pose import Pose
from .geom.vector3 import Vector3


@dataclass
class Path:
    name: str
    points: list = field(default_factory=list)
    pose: Pose = field(default_factory=Pose)
    size: Vector3 = None
    color: str = 'red'
    distance_relative_to_ground: bool = True
    radius: float = 0.3

    def __post_init__(self):
        if not self.size:
            self.size = Vector3(1, 1, 1)

    def __iter__(self):
        yield ('name', self.name)
        yield ('points', self.points)
        if self.pose:
            yield ('pose', dict(self.pose))
        if self.size:
            yield ('size', list(self.size))
        if self.color:
            yield ('color', self.color)
        if self.distance_relative_to_ground:
            yield (
                'distance_relative_to_ground',
                self.distance_relative_to_ground)
        if self.radius:
            yield ('radius', self.radius)
