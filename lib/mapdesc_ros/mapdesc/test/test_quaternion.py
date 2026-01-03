from mapdesc.model.geom import Box, Dimension, Pose, \
    Quaternion, Vector2, Mesh
import pytest


def test_from_any():
    original = Quaternion(1, 2, 3, 1)
    vec = Quaternion.from_any([1, 2, 3, 1])
    assert vec.to_tuple() == original.to_tuple()
    vec = Quaternion.from_any({'x': 1, 'y': 2, 'z': 3, 'w': 1})
    assert vec.to_tuple() == original.to_tuple()
    try:
        Quaternion.from_any('invalid')
        assert False
    except RuntimeError:
        pass


def test_rotaion():
    # test to rotate a mesh
    # 1. rotate simple box by 45 degree []
    box = Box(
        size=Dimension(
            width=2.0, length=5.0, height=1.0
        ),
        pose=Pose(
            # roate by 45 degree
            orientation=Quaternion(z=0.383, w=0.924)
        )
    )
    # apply roation
    points = box.local_points()
    points = [round(p, 3) for p in points]
    assert Vector2(1.062, -2.474) in points
    assert Vector2(2.475, -1.059) in points
    assert Vector2(-1.062, 2.474) in points
    assert Vector2(-2.475, 1.059) in points

    # 2. rotate complex shape by 23 degree []
    polygons = [
        Vector2(-20, -30),
        Vector2(10, -40),
        Vector2(50, -20),
        Vector2(100, 60),
        Vector2(-70, 10),
        Vector2(-10, 0)
    ]

    mesh = Mesh(
        polygons=polygons,
        pose=Pose(
            position=Vector2(80, 100),
            # roate by 23
            orientation=Quaternion(z=0.2, w=0.98)
        ))
    points = mesh.local_points()
    points = [round(p, 3) for p in points]
    assert points == [
        Vector2(x=73.355, y=64.562),
        Vector2(x=104.874, y=67.117),
        Vector2(x=133.838, y=101.192),
        Vector2(x=148.493, y=194.386),
        Vector2(x=11.679, y=81.771),
        Vector2(x=70.8, y=96.082)]


def test_getitem():
    q = Quaternion(x=3, y=4, z=5, w=6)
    assert q['w'] == 6
    assert q[2] == 5
    assert q[0] == q['x'] == 3
    assert q[1] == 4
    with pytest.raises(RuntimeError) as exc_info:
        assert not q['a']  # a should not be a valid subscription
    assert exc_info.value.args[0] == 'unknown key "a"'
    with pytest.raises(RuntimeError) as exc_info:
        assert q[-1]
    assert exc_info.value.args[0] == 'unknown key "-1"'


def test_copy():
    q = Quaternion(x=3, y=4, z=5, w=6)
    q2 = q.copy()
    q2.x = 1
    q2.y = 2
    q2.z = 3
    q2.w = 4
    assert q.x == 3
    assert q.y == 4
    assert q.z == 5
    assert q.w == 6


def test_normalize():
    vec = Quaternion(0, 0, 0, 0)
    with pytest.raises(RuntimeError) as exc_info:
        vec.normalize()
    assert exc_info.value.args[0].startswith(
        'Can not normalize null quaternion')
