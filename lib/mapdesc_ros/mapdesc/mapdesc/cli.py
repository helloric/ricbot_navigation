#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

"""mapdesc command line tool."""

import argparse
import logging
import os
import sys

from .load import LOAD
from .save import SAVE

CONFIG_FORMATTER = '%(asctime)s %(name)s[%(levelname)s] %(message)s'
LOAD_ARGS = {
    'yaml': [('load_file', 'YAML filename (.yml/.yaml)')],
    'rosmap': [('load_file', 'ROS filename (.yml/.yaml), NOT the png')],
    'geojson': [
        ('load_file', 'Load GeoJSON file (.geojson)'),
        ('planet', 'Planet (normally "earth")')],
    'sdf': [('load_file', 'SDF file (.xml/.sdf)')],
    'osm': [
        ('lat', 'latitude of coordinate'),
        ('lon', 'longitude of coordinate'),
        ('radius', 'radius around the given coordinate'),
        ('planet', 'Planet (normally "earth")')
    ]
}
SAVE_ARGS = {
    'png': [('file_name', 'PNG image (.png)')],
    'rosmap': [
        (
            'file_name',
            'Name of YAML-File, will create a png from the map'
        )
    ],
    'sdf': [
        (
            'folder_name',
            'folder name of the model, will create a .sdf and config file'
        )
    ],
    'svg': [('file_name', 'SVG file (.svg)')],
    'yaml': [
        (
            'file_name',
            'Name of YAML-File, lossless, '
            'based on the description with all information'
        )
    ],
}


def setup_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level)
    logging.basicConfig(level=log_level, format=CONFIG_FORMATTER)


def print_help():
    print(
        'usage: mapdesc [-h] [LOAD_TYPE] [LOAD_PARAMS...] '
        '[SAVE_TYPE] [SAVE_PARAMS...]:')
    print(__doc__)
    print('')
    print('LOAD_TYPE can be one of these (with LOAD_PARAMS):')
    for key, arg in LOAD_ARGS.items():
        print(f'  {key}: ')
        for sarg in arg:
            print(f'    {sarg[0]}: {sarg[1]}')
    print('')
    print('SAVE_TYPE can be one of these (with SAVE_PARAMS):')
    for key, arg in SAVE_ARGS.items():
        print(f'  {key}: ')
        for sarg in arg:
            print(f'    {sarg[0]}: {sarg[1]}')
    print('')
    print('examples:')
    print('# convert yaml file to sdf')
    print('mapdesc yaml test/yaml/simple_walls.yaml sdf ./generated/sdf/test1')
    print('# get buildings from OSM and save as svg')
    print('mapdesc osm 53.0762098 8.8075270 80 svg bremen_city.svg')


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        'load_type', choices=LOAD_ARGS.keys(),
        help='Type of loading operation')
    parser.add_argument(
        '--recenter', '-r', default=False,
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        '--bounding_box', default=False,
        action=argparse.BooleanOptionalAction
    )
    # boxify creates a box from meshes that have 4 points as polygon that
    # perfectly align as box
    parser.add_argument(
        '--boxify', '-b', default=False,
        action=argparse.BooleanOptionalAction
    )

    parser.add_argument(
        'load_params', nargs='+', help='Parameters for loading operation')

    parser.add_argument(
        'save_type', choices=SAVE_ARGS.keys(), help='Type of saving operation')
    parser.add_argument(
        'save_params', nargs='+', help='Parameters for saving operation')

    args = parser.parse_args()

    if len(LOAD_ARGS[args.load_type]) != len(args.load_params):
        print(
            f'Error: {args.load_type} operation requires '
            f'{len(LOAD_ARGS[args.load_type])} parameters '
            f'({len(args.load_params)} given)')
        parser.print_help()
        sys.exit(1)

    if len(SAVE_ARGS[args.save_type]) != len(args.save_params):
        print(
            f'Error: {args.save_type} operation requires '
            f'{len(SAVE_ARGS[args.save_type])} parameters '
            f'({len(args.save_params)} given)')
        parser.print_help()
        sys.exit(1)

    _map = LOAD[args.load_type](*args.load_params)
    if not _map:
        return
    if args.recenter:
        _map.recenter()
    if args.bounding_box:
        _map.bounding_box()
    if args.boxify:
        _map.boxify()
    SAVE[args.save_type](_map, *args.save_params)


if __name__ == '__main__':
    main()
