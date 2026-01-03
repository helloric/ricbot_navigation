import os
from pathlib import Path
from mapdesc import load


BASE_PATH = Path(os.path.dirname(__file__)).absolute()


def test_load_yaml():
    _map = load.load_yaml(
        input_file=BASE_PATH / 'yaml' / 'simple_walls.yaml')
    assert len(_map.wall) == 4
    assert _map.wall[0].pose.position.x == -10

    # Hi Digit Pro 4.0 production map as complex example
    _map = load.load_yaml(
        input_file=BASE_PATH / 'yaml' / 'hdp_2_agents_map.yml')
    assert len(_map.area) == 7
    assert len(_map.lane_graph.edges) == 74
    assert len(_map.lane_graph.nodes) == 23
