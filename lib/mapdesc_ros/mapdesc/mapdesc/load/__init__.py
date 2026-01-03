from .rosmap import load_rosmap
from .yaml import load_yaml
from .osm import load_osm
from .sdf import load_sdf
from .geojson import load_geojson

LOAD = {
    'yaml': load_yaml,
    'rosmap': load_rosmap,
    'osm': load_osm,
    'sdf': load_sdf,
    'geojson': load_geojson
}
