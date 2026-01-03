# load data description from OSM coordinages
from ..model import Map, Wall
from ..model.geom import Mesh
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
import numpy as np
from ..geo_data import lon_lat_to_point


def load_osm(lat: float, lon: float, radius: float, body: str = 'earth'):
    lat = float(lat)
    lon = float(lon)
    radius = float(radius)

    north = lat + radius/111320
    south = lat - radius/111320
    east = lon + radius/111320/np.cos(lat*np.pi/180)
    west = lon - radius/111320/np.cos(lat*np.pi/180)

    # Build the query using the OverpassQueryBuilder
    query = overpassQueryBuilder(
        bbox=(south, west, north, east),
        elementType=['way', 'relation', 'node'],
        selector='"building"="yes"',
        out='body',
    )

    overpass = Overpass()
    results = overpass.query(query).ways()

    # TODO: save buildings
    # building_nodes = {}

    walls = []
    if results:
        for way in results:
            nodes = way.nodes()
            points = [
                lon_lat_to_point(
                    lat, lon, n.lat(), n.lon(), body) for n in nodes]
            mesh = Mesh(polygons=points)
            wall = Wall(mesh, name=way.id)
            walls.append(wall)

    return Map(wall=walls)
