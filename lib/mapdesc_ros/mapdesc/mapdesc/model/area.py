# An area defines a region by a rectangle or polygon on the map,
# either as annotation for the user without function or
# for the planning system to change agent behavior when it enters a
# region.
# For example go to the next task when the agent moves
# into a goal area or change from a behavior where the robot
# follows a strict line to a behavior where the robot
# explores the map further.
from .geom.box import Box
from .geom.mesh import Mesh
from dataclasses import dataclass, field


TYPES = {
    'mesh': Mesh,
    'box': Box
}


@dataclass
class Area:
    data: Box | Mesh
    # geometric type (mesh or box)
    type: str = 'mesh'
    # custom type of your are, can for example be 'recharging' or 'unload'
    # so other tools can use it to execute behavior based on this type
    area_type: str = 'unnamed'
    # name to identify area
    name: str = None
    # color as RGB array with values from 0 to 255
    color: list = field(default_factory=lambda: [50, 50, 255])

    @property
    def center(self):
        return self.data.pose.position

    @property
    def points(self):
        return self.data.points

    @property
    def size(self):
        return self.data.size

    @property
    def pose(self):
        return self.data.pose

    def local_points(self):
        return self.data.local_points()

    def __post_init__(self):
        if isinstance(self.data, dict):
            clz = TYPES[self.type]
            # pylint: disable=not-a-mapping
            self.data = clz(**self.data)

    def __iter__(self):
        yield ('data', dict(self.data))
        yield ('type', self.type)
        yield ('area_type', self.area_type)
        if self.name:
            yield ('name', self.name)
        if self.color:
            yield ('color', self.color)

    def copy(self):
        return Area(**dict(self))

    def bounding_box(self):
        if self.type != 'mesh':
            return
        self.data = self.data.bounding_box()
        self.type = 'box'

    def boxify(self):
        if self.type != 'mesh':
            return
        self.data = self.data.boxify()
        self.type = 'box'
