from mapdesc import model


def test_wall_box():
    wall = model.Wall(data=model.geom.Box())
    # assure a default length is set
    assert wall.data.size.length == 1.0
    # assure the type is the given box
    assert wall.type == 'box'


def test_wall_mesh():
    wall = model.Wall(data=model.geom.Mesh())
    assert wall.type == 'mesh'
    assert wall.data.size.width == 1.0
