import math
from mapdesc import util
from mapdesc.model.geom import Quaternion, Vector2, Mesh
import pytest


def test_quaternion():
    assert \
        (0.0, 0.0, 0.707107, 0.707107) == \
        pytest.approx(util.euler_to_quaternion(0, 0, math.pi / 180 * 90))

    quat = Quaternion(0, 0, 0.707107, 0.707107)
    euler = quat.to_euler()
    assert euler.x == 0
    assert euler.y == 0
    assert euler.z == pytest.approx(math.pi / 180 * 90)


def test_sort_points():
    # these points are clockwise sort
    cw_points = [Vector2(x, y) for x, y in [[0, 0], [0, 1], [1, 0], [1, 1]]]
    # these are counter clockwise
    # TODO: check, if this is correct, we probably don't want to go
    # from 0.0 to 0.1!
    ccw_points = [Vector2(x, y) for x, y in [[1, 0], [1, 1], [0, 0], [0, 1]]]
    assert util.ccw_sort(cw_points) == ccw_points

    mesh = Mesh(polygons=cw_points)
    mesh.ccw_sort()
    assert mesh.polygons == ccw_points


def test_bounding_box():
    points = [[1, 2], [-3, 99], [-6, -100]]
    assert util.bounding_box(points) == (-6, -100, 1, 99)
