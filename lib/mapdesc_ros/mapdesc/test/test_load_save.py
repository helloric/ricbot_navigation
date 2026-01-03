from mapdesc.load.rosmap import load_rosmap
from mapdesc.load.yaml import load_yaml
from mapdesc.save import save_sdf, save_png, save_svg, save_rosmap
from pathlib import Path


def test_gen_sdf():
    _map = load_rosmap('./test/map/mallmap.yaml')
    assert _map.wall
    save_sdf(_map, './generated/sdf/mallmap_unittest_sdf1')


def test_gen_sdf2():
    _map = load_yaml('./test/yaml/simple_walls.yaml')
    save_sdf(_map, './generated/sdf/mallmap_unittest_sdf2')


def test_gen_png():
    mall_map = load_rosmap('./test/map/mallmap.yaml')
    assert mall_map.wall
    save_png(mall_map, './generated/mallmap_unittest_png.png')

    hdp_map = load_yaml('./test/yaml/hdp_2_agents_map.yml')
    assert hdp_map.wall
    save_png(hdp_map, './generated/hdp_unittest_png.png')


def test_gen_svg():
    _map = load_yaml('./test/yaml/hdp_2_agents_map.yml')
    save_svg(_map, './generated/hdp2_unittest_svg.svg')


def test_rosmap():
    _map = load_yaml('./test/yaml/hdp_2_agents_map.yml')
    save_rosmap(_map, './generated/fail.test')
    save_rosmap(_map, './generated/hdp_rosmap.yaml')
    assert Path('./generated/hdp_rosmap.png').exists()
    assert Path('./generated/hdp_rosmap.yaml').exists()
