from dataclasses import dataclass

from .box import Box


@dataclass
class Capsule(Box):
    radius: float = 1.0
    length: float = 1.0

    def __iter__(self):
        yield from super().__iter__()
        yield ('radius', self.radius)
        yield ('length', self.length)
