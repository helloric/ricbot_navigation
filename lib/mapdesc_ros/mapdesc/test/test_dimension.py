from mapdesc.model.geom import Dimension


def test_dimension():
    dim = Dimension()
    assert dim.length == 1
    assert dim.height == 1
    assert dim.width == 1
