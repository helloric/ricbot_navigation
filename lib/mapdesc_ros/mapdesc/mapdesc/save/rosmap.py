from .png import save_png
from ..model import Map
import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def save_rosmap(_map: Map, yaml_file: str):
    path = Path(yaml_file)
    if path.suffix not in ['.yaml', '.yml']:
        logger.error('Not a yaml file!')
        return
    base = yaml_file[:-len(path.suffix)]
    png_file = Path(f'{base}.png')
    save_png(_map, png_file, obstacles_only=True)
    yaml_data = {
        'image': str(png_file.relative_to(png_file.parent)),
        'resolution': _map.resolution,
        'origin': list(_map.origin),
        'negate': 0,
        'occupied_thresh': 0.65,
        'free_thresh': 0.196
    }
    with open(str(yaml_file), 'w', encoding='utf-8') as fd:
        yaml.safe_dump(
            yaml_data, fd, default_style=None, default_flow_style=None)
