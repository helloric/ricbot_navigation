from mapdesc.load.yaml import load_yaml


def test_map_to_dict():
    _map = load_yaml('./test/yaml/hdp_2_agents_map.yml')
    dict_map = dict(_map)
    assert len(dict_map['wall']) == 15
