# load data description from SDL file
# see http://sdformat.org/tutorials
from ..model import Map, Wall
from ..model.geom import Box, Pose, Dimension, Vector3, \
    Quaternion, Mesh
from ..util import euler_to_quaternion
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_pose(pose: str):
    pose = [float(x) for x in pose.split(' ')]
    position = Vector3(*[float(x) for x in pose[0:3]])
    rotation = euler_to_quaternion(*pose[3:6])
    return Pose(position=position, orientation=Quaternion(*rotation))


def parse_box_size(link_element):
    size = link_element.find('collision/geometry/box/size').text.strip()
    return Dimension(*[float(x) for x in size.split(' ')])


def parse_link(link_element):
    if link_element.find('collision/geometry/box'):
        wall_type = 'box'
        wall_data = Box(
            pose=parse_pose(link_element.find('pose').text.strip()),
            size=parse_box_size(link_element))
    elif link_element.find('collision/geometry/polyline'):
        wall_type = 'polygon'
        wall_data = Mesh(
            polygons=[
                [float(y) for y in x.text.strip().split(' ')] for x in
                link_element.findall('collision/geometry/polyline/point')])
    else:
        raise RuntimeError('unknown xml geometry')
    # we ignore the pose
    return Wall(
        name=link_element.attrib['name'],
        data=wall_data,
        type=wall_type,
    )


def get_walls_from_sdf(path):
    walls = []
    with open(str(path), encoding='utf-8') as fd:
        xml_string = fd.read()
        root = ET.fromstring(xml_string)
        model_element = root.find('model')
        # we assume our model is static and 
        # everything is stored inside a link,
        # we also ignore the initial pose of the model
        # links are translated into walls
        for link in model_element.findall('link'):
            wall = parse_link(link)
            if wall:
                walls.append(wall)
    return walls


def parse_sdf_dir(path):
    with open(str(path / 'model.config'), encoding='utf-8') as fd:
        xml_string = fd.read()
        root = ET.fromstring(xml_string)
        name_el = root.find('name')
        desc_el = root.find('description')
        sdf_el = root.find('sdf')

    description = desc_el.text.strip() if desc_el is not None else ''
    name = name_el.text.strip() if name_el is not None else ''
    sdf_file = sdf_el.text.strip() if sdf_el is not None else 'model.sdf'

    _map = Map(name=name, description=description)
    _map.walls = get_walls_from_sdf(str(path / sdf_file))
    return _map


def load_sdf(input_path=None):
    """Load from custom sdf format.
    """
    input_sdf = Path(input_path)
    if not input_sdf.exists():
        raise RuntimeError('file/folder to load does not exist')
    if input_sdf.is_dir():
        _map = parse_sdf_dir(input_sdf)
    elif str(input_path)[:4] in ['.sdf', '.xml']:
        _map = Map()
        _map.walls = get_walls_from_sdf(str(input_sdf))
    return _map
