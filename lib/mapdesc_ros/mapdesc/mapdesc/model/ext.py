# An external object,
from dataclasses import dataclass
# bounding box
from .geom.box import Box


@dataclass
class Ext:
    name: str = None
    type: str = 'gltf'  # 'geotiff' | 'obj' | 'fbx' | 'ifc' | 'gltf'
    data: Box
    # list of strings
    filenames: list

    def __iter__(self):
        yield ('name', self.name)
        yield ('type', self.type)
        yield ('data', dict(self.data))
        yield ('filenames', list(self.filenames))