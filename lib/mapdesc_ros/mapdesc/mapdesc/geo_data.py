import math


PROJECTIONS = {
    'moon':
        'PROJCS["Equirectangular Moon",'
        'GEOGCS["GCS_Moon",DATUM["D_Moon",'
        'SPHEROID["Moon_localRadius",1737400,0]],'
        'PRIMEM["Reference_Meridian",0],'
        'UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],'
        'PROJECTION["Equirectangular"],'
        'PARAMETER["standard_parallel_1",0],'
        'PARAMETER["central_meridian",0],'
        'PARAMETER["false_easting",0],'
        'PARAMETER["false_northing",0],'
        'UNIT["metre",1,AUTHORITY["EPSG","9001"]],'
        'AXIS["Easting",EAST],'
        'AXIS["Northing",NORTH]]'
}

# Volumetric mean radius of planets and moons (approx. in meter)
RADIUS_IN_METERS = {
    'sun':       696342000,

    'mercury':     2439700,
    'venus':       6051800,
    'earth':       6378137,
    'moon':        1737400,
    'mars':        3389500,
    # Moons of Mars
    'phobos':        11266,
    'deimos':         6200,

    'jupiter':    69911000,
    # Moons of Jupiter
    'io':          1821600,
    'europa':      1560800,
    'ganymede':    2634100,
    'callisto':    2410300,

    'saturn':     58232000,
    # Moons of Saturn
    'mimas':        198200,
    'enceladus':    252100,
    'tethys':       531100,
    'dione':        561400,
    'rhea':         764300,
    'titan':       2574700,
    'iapetus':      734500,

    'uranus':     25362000,
    # Moons of Uranus
    'miranda':      235800,
    'ariel':        578900,
    'umbriel':      584700,
    'titania':      788400,
    'oberon':       761400,

    'neptune':    24622000,
    # Moon of Neptune
    'triton':      1353400,

    # dwarf planets
    'pluto':       1188300,
    # Moons of pluto
    'charon':       606000,
    'nix':           24900,  # diameter 49.8 × 33.2 × 31.1
    'hydra':         25500,  # diameter 50.9 × 36.1 × 30.9
    'kerberos':       9500,  # diameter 19 × 10 × 9
    'styx':           8000,  # diameter 16 × 9 × 8

    'eris':        1163000,
    'haumea':       780000,
    'makemake':     715000,
    'gongong':      615000,
    'quaora':       545000,
    'sedna':        500000,
    'ceres':        469700,
    'orcus':        435000,
    'vesta':        262700,
    'pallas':       255500,
    'hygiea':       216500,
    'juno':         135700,
    'chiron':        58350,
    'pholus':        49500,
    'nessus':        29000,
}

SIGNS = {
    'sun':         '☉',
    'mercury':     '☿',
    'venus':       '♀︎',
    'earth':       '🜨',
    'moon':        '☾',
    'mars':        '♂︎',
    'jupiter':     'J',

    'saturn':      '♄',
    'uranus':      '⛢',

    'neptune':     '♆',

    # dwarf planets
    'pluto':       '♇',
    'eris':        '⯰',
    'sedna':       '⯲',
    'ceres':       '⚳',
    'vesta':       '⚶',
    'pallas':      '⚴',
    'hygiea':      '⯚',
    'juno':        '⚵',
    'chiron':      '⚷',
    'pholus':      '⯛',
    'nessus':      '⯜',
}

CIRCUMFERENCE_IN_METERS = {}
for name, radius in RADIUS_IN_METERS.items():
    CIRCUMFERENCE_IN_METERS[name] = radius * math.pi * 2

METERS_PER_DEGREE_LATITUDE = {}
for name, circ in CIRCUMFERENCE_IN_METERS.items():
    METERS_PER_DEGREE_LATITUDE[name] = circ / 360


def meters_per_degree_longitude(lat, body):
    # A degree of longitude is widest at the equator at 111.321 km and
    # gradually shrinks to zero at the poles.
    return METERS_PER_DEGREE_LATITUDE[body] * math.cos(lat / 180 * math.pi)


def lon_lat_to_point(lat, lon, build_lat, buid_lon, body):
    lonToMeter = meters_per_degree_longitude(build_lat, body)
    latToMeter = METERS_PER_DEGREE_LATITUDE[body]
    return (lon - buid_lon) * lonToMeter,  (lat - build_lat) * latToMeter
