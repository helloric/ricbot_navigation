from mapdesc.model.geom import Vector3


def test_is_close():
    a = Vector3(1, 2, 5)
    b = Vector3(3, 4, 6)
    assert not a.is_close(b)
    assert not a.is_close(None)
    assert not a.is_close({'x': 3, 'y': 5, 'z': 8})
    assert not a.is_close({3, 5, 6})
    assert a.is_close({3, 5, 6}, threshold=10)
    assert not a.is_close({3, 11, 10}, threshold=10)


def test_to_tuple():
    a = Vector3(1, 2, 5)
    # check inherited to_tuple
    assert a.to_tuple() == tuple((1.0, 2.0, 5.0))


def test_normalize():
    a = Vector3(1, 2, 3).normalize()
    assert a.x == 0.2672612419124244
    assert a.y == 0.5345224838248488
    assert a.z == 0.8017837257372732


def test_from_any():
    original = Vector3(1, 2, 3)
    vec = Vector3.from_any([1, 2, 3])
    assert vec.to_tuple() == original.to_tuple()
    vec = Vector3.from_any({'x': 1, 'y': 2, 'z': 3})
    assert vec.to_tuple() == original.to_tuple()
    try:
        Vector3.from_any('invalid')
        assert False
    except RuntimeError:
        pass


def test_copy():
    vec = Vector3(x=3, y=4, z=5)
    vec2 = vec.copy()
    vec2.x = 1
    vec2.y = 2
    vec2.z = 3
    assert vec.x == 3
    assert vec.y == 4
    assert vec.z == 5


def test_round():
    vec = Vector3(1.1111111, 2.22222222, 3.333333)
    vec2 = round(vec, 2)
    assert vec.x == 1.1111111
    assert vec2 == Vector3(1.11, 2.22, 3.33)
