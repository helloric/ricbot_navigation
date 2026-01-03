from dataclasses import dataclass

from .box import Box


@dataclass
class Sphere(Box):
    radius: float = 1.0

    def __iter__(self):
        yield from super().__iter__()
        yield ('radius', self.radius)
