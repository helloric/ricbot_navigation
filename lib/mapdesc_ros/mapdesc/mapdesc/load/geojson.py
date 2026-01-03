from ..model import Map, Path
from pathlib import Path as PathLib
import json
import logging
from ..geo_data import lon_lat_to_point

logger = logging.getLogger(__name__)


def parse_coordinates(first_lat, first_lon, coords, planet: str = 'earth'):
    distances = []
    if not first_lat:
        first_lon, first_lat = coords[0][0], coords[0][1]
        coords = coords[1:]
    for lon, lat in coords:
        distances.append(
            lon_lat_to_point(lat, lon, first_lat, first_lon, body=planet))
    return first_lon, first_lat, distances


def get_path_from_geojson(path, planet: str = 'earth'):
    paths = []
    first_lat, first_lon = None, None
    with open(str(path), encoding='utf-8') as fd:
        data = json.load(fd)
        for feature in data['features']:
            if 'geometry' not in feature:
                continue
            if 'coordinates' not in feature['geometry']:
                continue
            if feature['geometry']['type'] == 'Point':
                continue
            if len(feature['geometry']['coordinates']) == 1:
                continue
            path = Path(
                name='unknown path',
            )
            paths.append(path)
            first_lon, first_lat, coords = \
                parse_coordinates(
                    first_lat, first_lon,
                    feature['geometry']['coordinates'],
                    planet)
            path.points = coords
    return paths


def load_geojson(input_path=None, planet: str = 'earth'):
    input_geojson = PathLib(input_path)
    if not input_geojson.exists():
        raise RuntimeError('file/folder to load does not exist')
    _map = Map()
    _map.path = get_path_from_geojson(input_geojson, planet)
    return _map
