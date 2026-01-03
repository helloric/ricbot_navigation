from mapdesc.model.geom import Dimension, Plane


def test_plane():
    plane = Plane(
        normal=[1, 1, 1],
        size=[2, 2])
    assert isinstance(plane.size, Dimension)
    assert plane.size.height == 0
    plane_dict = dict(plane)
    assert plane_dict['size'] == (2, 2)
