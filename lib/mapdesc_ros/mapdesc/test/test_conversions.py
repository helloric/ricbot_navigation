from mapdesc.model.geom import Vector2, Vector3, Quaternion, Dimension


def test_from_to_list():
    vec = Vector2(*[1, 2, 'ignore_me'])
    assert vec.x == 1
    assert vec.y == 2
    assert list(vec) == [1.0, 2.0]

    vec = Vector3(*[1, 2, 3, 'ignore_me'])
    assert vec.x == 1
    assert vec.y == 2
    assert vec.z == 3
    assert list(vec) == [1.0, 2.0, 3.0]

    quat = Quaternion(*[1, 2, 3, 4, 'ignore_me'])
    assert quat.x == 1
    assert quat.y == 2
    assert quat.z == 3
    assert quat.w == 4
    assert list(quat) == [1.0, 2.0, 3.0, 4.0]

    dim = Dimension(*[1, 2, 3, 'ignore_me'])
    assert dim.width == 1
    assert dim.length == 2
    assert dim.height == 3
    assert list(dim) == [1.0, 2.0, 3.0]


def test_null():
    num = [1, 2, 3, 4, 'ignore_me']
    for clz in [Vector2, Vector3, Quaternion]:
        vec = clz(*num)
        assert not vec.null()
        vec = clz()
        assert vec.null()

    dim = Dimension(*[1, 2, 3])
    assert not dim.null()
    dim = Dimension()
    assert not dim.null()
    dim = Dimension(0, 0, 0)
    assert dim.null()


def test_sub():
    num = [10, 9, 8, 7, 'ignore_me']

    vec = Vector2(*num) - 3
    assert vec.x == 7
    assert vec.y == 6
    vec -= Vector2(1, 1)
    assert vec.x == 6
    assert vec.y == 5

    vec = Vector3(*num) - 2
    assert vec.x == 8
    assert vec.y == 7
    assert vec.z == 6
    vec -= Vector3(1, 1, 1)
    assert vec.x == 7
    assert vec.y == 6
    assert vec.z == 5

    quat = Quaternion(*num) - 2
    assert quat.x == 8
    assert quat.y == 7
    assert quat.z == 6
    assert quat.w == 5
    quat -= Quaternion(-1, 1, -2, -3)
    assert quat.x == 9
    assert quat.y == 6
    assert quat.z == 8
    assert quat.w == 8

    dim = Dimension(*num) - 2
    assert dim.width == 8
    assert dim.length == 7
    assert dim.height == 6
    dim -= Dimension(-2, -4, -6)
    assert dim.width == 10
    assert dim.length == 11
    assert dim.height == 12
    dim -= dim
    assert dim.null()


def test_mul():
    num = [1, 2, 3, 4, 'ignore_me']

    vec = Vector2(*num) * 2
    assert vec.x == 2
    assert vec.y == 4
    vec *= vec
    assert vec.x == 4
    assert vec.y == 16

    vec = Vector3(*num) * 2
    assert vec.x == 2
    assert vec.y == 4
    assert vec.z == 6
    vec *= vec
    assert vec.x == 4
    assert vec.y == 16
    assert vec.z == 36

    quat = Quaternion(*num) * 2
    assert quat.x == 2
    assert quat.y == 4
    assert quat.z == 6
    assert quat.w == 8
    quat *= quat
    assert quat.x == 4
    assert quat.y == 16
    assert quat.z == 36
    assert quat.w == 64

    dim = Dimension(*num) * 2
    assert dim.width == 2
    assert dim.length == 4
    assert dim.height == 6
    dim *= dim
    assert dim.width == 4
    assert dim.length == 16
    assert dim.height == 36


def test_add():
    num = [1, 2, 3, 4, 'ignore_me']

    vec = Vector2(*num) + 2
    assert vec.x == 3
    assert vec.y == 4
    vec += vec
    assert vec.x == 6
    assert vec.y == 8

    vec = Vector3(*num) + 4
    assert vec.x == 5
    assert vec.y == 6
    assert vec.z == 7
    vec += vec
    assert vec.x == 10
    assert vec.y == 12
    assert vec.z == 14

    quat = Quaternion(*num) + 6
    assert quat.x == 7
    assert quat.y == 8
    assert quat.z == 9
    assert quat.w == 10
    quat += quat
    assert quat.x == 14
    assert quat.y == 16
    assert quat.z == 18
    assert quat.w == 20

    dim = Dimension(*num) + 2
    assert dim.width == 3
    assert dim.length == 4
    assert dim.height == 5
    dim += dim
    assert dim.width == 6
    assert dim.length == 8
    assert dim.height == 10


def test_neg():
    vec = -Vector2(*[1, 2, 'ignore_me'])
    assert vec.x == -1
    assert vec.y == -2

    vec = -Vector3(*[1, 2, 3, 'ignore_me'])
    assert vec.x == -1
    assert vec.y == -2
    assert vec.z == -3

    quat = -Quaternion(*[1, 2, 3, 4, 'ignore_me'])
    assert quat.x == -1
    assert quat.y == -2
    assert quat.z == -3
    assert quat.w == -4

    dim = -Dimension(*[1, 2, 3, 'ignore_me'])
    assert dim.width == -1
    assert dim.length == -2
    assert dim.height == -3
