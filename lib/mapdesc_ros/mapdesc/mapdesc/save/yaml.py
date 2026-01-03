import yaml
from ..model import Map


def save_yaml(_map: Map, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(
            dict(_map), f, default_style=None, default_flow_style=None)
