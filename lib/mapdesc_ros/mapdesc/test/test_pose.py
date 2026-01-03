import math
import pytest
from mapdesc.model.geom import Pose, Vector2, Vector3, Quaternion
from mapdesc.model.geom.pose import any_to_vector, dict_to_vector


def test_euler_orientation():
    p = Pose(orientation=Vector3(
        math.pi / 180 * 90,
        math.pi / 180 * 45,
        math.pi / 180 * 180))
    euler = p.euler_orientation()
    assert tuple(euler) == (math.pi / 2, math.pi / 4, math.pi)
    # check caching
    euler = p.euler_orientation()
    assert tuple(euler) == (math.pi / 2, math.pi / 4, math.pi)

    p = Pose(orientation=Quaternion(0, 0, 0, 1))
    euler = p.euler_orientation()
    assert tuple(euler) == (0, 0, 0)

    p = Pose(orientation=Quaternion(1, 0, 0, 0))
    euler = p.euler_orientation()
    assert tuple(euler) == (math.pi, 0, 0)

    p = Pose(orientation=Quaternion(0.707, 0, 0, 0.707))
    euler = p.euler_orientation()
    assert tuple(euler) == (pytest.approx(math.pi / 2, .001), 0, 0)


def test_pose_dict():
    p = Pose()
    # test post-init
    assert isinstance(p.orientation, Quaternion)
    # test __iter__
    assert '_euler_orientation' not in dict(p)
    assert 'orientation' in dict(p)
    # note that dict("custom_object") calls __iter__() on all nested
    # structures (like position and orientation).
    assert dict(p)['orientation'] == (0, 0, 0, 1)


def test_any_to_vector():
    my_dict = {'x': 1, 'y': 2}
    vec2 = any_to_vector(my_dict)
    assert isinstance(vec2, Vector2)

    my_dict['z'] = 3
    vec3 = any_to_vector(my_dict)
    assert isinstance(vec3, Vector3)

    my_dict['w'] = 4
    quat = any_to_vector(my_dict)
    assert isinstance(quat, Quaternion)

    my_dict = {'x': 1}
    with pytest.raises(RuntimeError) as exc_info:
        dict_to_vector(my_dict)
    err_str = 'x and y not set, not a valid pose.'
    assert exc_info.value.args[0] == err_str
