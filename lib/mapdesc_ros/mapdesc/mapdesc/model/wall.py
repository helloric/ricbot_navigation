from dataclasses import dataclass
from .geom.box import Box
from .geom.mesh import Mesh


TYPES = {
    'mesh': Mesh,
    'box': Box
}


@dataclass
class Wall:
    # required, either a Box or a Mesh
    data: Box | Mesh

    # optional name for the wall
    name: str = None

    # optional list of holes in the wall
    holes: list = None

    # type, is set based on given data
    type: str = None

    def __post_init__(self):
        if isinstance(self.data, dict):
            clz = TYPES[self.type]
            # pylint: disable=not-a-mapping
            self.data = clz(**self.data)
        else:
            self.type = self.data.__class__.__name__.lower()
        self.holes = self.holes if self.holes else []

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

    def __iter__(self):
        yield ('data', dict(self.data))
        yield ('type', self.type)
        if self.name:
            yield ('name', self.name)
        if self.holes:
            yield ('holes', self.holes)

    def bounding_box(self):
        if self.type != 'mesh':
            return
        box = self.data.bounding_box()
        if not box:
            return
        self.data = box
        self.type = 'box'

    def boxify(self):
        if self.type != 'mesh':
            return
        box = self.data.boxify()
        if not box:
            return
        self.data = box
        self.type = 'box'
