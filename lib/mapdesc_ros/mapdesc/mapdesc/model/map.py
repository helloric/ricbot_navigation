from dataclasses import dataclass, field

from .geom.dimension import Dimension
from .geom.vector3 import Vector3
from .wall import Wall
from .marker import Marker
from .area import Area
from .lane import LaneGraph
from .path import Path


@dataclass
class Map:
    # name has to be unique as its also the file-name
    name: str = 'undefined'
    # optional description of the map
    description: str = 'some map'

    # size of the map
    size: Dimension = field(default_factory=Dimension)
    # resolution - important for export for the ROS 2 mapserver
    resolution: float = 0.05
    # optional origin of the 0:0 position
    # (mostly imporant for the ROS 2 mapserver)
    origin: Vector3 = field(default_factory=Vector3)

    # obstacles/walls, for example useful to model a building
    wall: list = field(default_factory=list)  # list[Wall]
    # a marker is a single points with a direction
    marker: list = field(default_factory=list)
    # the area is an annotation of a region
    area: list = field(default_factory=list)  # list[Area]
    # the path consists of multiple points connected to each other
    path: list = field(default_factory=list)

    # ext is short for external mesh, useful for more complex environments.
    ext: list = field(default_factory=list)

    lane_graph: LaneGraph = None

    def __post_init__(self):
        if isinstance(self.size, (list, tuple)):
            self.size = Dimension(*self.size)
        if isinstance(self.origin, list):
            # pylint: disable=not-a-mapping
            self.origin = Vector3(*self.origin)
        if isinstance(self.origin, dict):
            # pylint: disable=not-a-mapping
            self.origin = Vector3(**self.origin)
        if self.marker:
            self.marker = [
                Marker(**m) if isinstance(m, dict) else m
                for m in self.marker
            ]
        if self.area:
            self.area = [
                Area(**a) if isinstance(a, dict) else a
                for a in self.area
            ]
        if self.wall:
            self.wall = [
                Wall(**w) if isinstance(w, dict) else w
                for w in self.wall
            ]
        if self.path:
            self.path = [
                Path(**p) if isinstance(p, dict) else p
                for p in self.path
            ]

        # TODO: self.ext

        if isinstance(self.lane_graph, dict):
            self.lane_graph = LaneGraph(**self.lane_graph)

    def __iter__(self):
        yield ('name', self.name)
        yield ('description', self.description)
        if self.wall:
            yield ('wall', [dict(w) for w in self.wall])
        yield ('resolution', self.resolution)
        yield ('origin', list(self.origin))
        if self.lane_graph:
            yield ('lane_graph', dict(self.lane_graph))
        if self.area:
            yield ('area', [dict(a) for a in self.area])
        if self.marker:
            yield ('marker', [dict(m) for m in self.marker])
        if self.path:
            yield ('path', [dict(m) for m in self.path])
        if self.ext:
            yield ('ext', [dict(m) for m in self.ext])

    def _meshes(self):
        """returns all items that have a mesh."""
        meshes = []
        if self.area:
            meshes += self.area
        if self.wall:
            meshes += self.wall
        return [m for m in meshes if m.type == 'mesh']

    def recenter(self):
        """Recenter walls and areas"""
        for item in self._meshes():
            if item.type == 'mesh':
                item.data.recenter()

    def boxify(self):
        """If there is a mesh with 4 points that align to make it a box"""
        for item in self._meshes():
            item.boxify()

    def bounding_box(self):
        """recenter walls and areas."""
        for item in self._meshes():
            item.bounding_box()
