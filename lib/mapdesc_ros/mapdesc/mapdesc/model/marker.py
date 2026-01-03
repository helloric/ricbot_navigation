# annotations or special points on the map, can for example be used
# by navigation as a goal (similar to lane.LaneNode)
from dataclasses import dataclass, field
from .geom.pose import Pose


@dataclass
class Marker:
    name: str = 'new marker'

    # marker can have an orientation
    pose: Pose = field(default_factory=Pose)

    # additional information about this marker that the user can define
    params: dict = field(default_factory=dict)

    # color the marker has on the map, defaults to red
    color: list = field(default_factory=lambda: [255, 50, 50])

    # radius of the marker (if we print the map)
    radius: float = 1.0

    # type of the marker (point, sphere, box, ...)
    type: str = 'point'

    def __post_init__(self):
        if isinstance(self.pose, dict):
            # pylint: disable=not-a-mapping
            self.pose = Pose(**self.pose)

    def __iter__(self):
        yield ('name', self.name)
        yield ('pose', dict(self.pose))
        if self.color:
            yield ('color', self.color)
        if self.radius is not None:
            yield ('radius', self.radius)
        if self.params:
            yield ('params', self.params)
        if self.type:
            yield ('type', self.type)
