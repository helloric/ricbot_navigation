from dataclasses import dataclass, field

from .vector3 import Vector3
from .box import Box


# TODO: let the Box inerhit plane - a box is a plane with a height
# or have them separated?
@dataclass
class Plane(Box):
    normal: Vector3 = field(default_factory=Vector3())

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.normal, (list, tuple)):
            self.normal = Vector3(*self.normal)
        # default for dimension is a 1x1x1 cube, so we have to set it to 0.
        self.size.height = 0.0

    def __iter__(self):
        yield from super().__iter__()
        yield ('normal', tuple(self.normal))
        yield ('size', tuple(self.size)[0:2])
