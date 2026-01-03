from mapdesc.model.geom import Vector2
import json


def test_is_close():
    a = Vector2(1, 2)
    b = Vector2(3, 4)
    assert not a.is_close(b)
    assert not a.is_close(None)
    assert not a.is_close({'x': 3, 'y': 5})
    assert not a.is_close({3, 5})
    assert a.is_close({3, 5}, threshold=10)


def test_distance():
    a = Vector2(1, 2)
    b = Vector2(3, 4)
    assert a.distance(b) == 2.8284271247461903


def test_normalize():
    a = Vector2(1, 2).normalize()
    # we are using the euclidean length, so we do not normalize based on
    # min and max (so the solution is not 0.5, 1.0)
    assert a.x == 0.4472135954999579
    assert a.y == 0.8944271909999159


def test_serialize():
    a = Vector2(1, 2)
    assert "[1.0, 2.0]" == json.dumps(a.serialize())


def test_from_any():
    original = Vector2(1, 2)
    vec = Vector2.from_any([1, 2])
    assert vec.to_tuple() == original.to_tuple()
    vec = Vector2.from_any({'x': 1, 'y': 2})
    assert vec.to_tuple() == original.to_tuple()
    try:
        Vector2.from_any('invalid')
        assert False
    except RuntimeError:
        pass


def test_copy():
    vec = Vector2(x=3, y=4)
    vec2 = vec.copy()
    vec2.x = 1
    vec2.y = 2
    assert vec.x == 3
    assert vec.y == 4


def test_round():
    vec = Vector2(1.1111111, 2.22222222)
    vec2 = round(vec, 2)
    assert vec.x == 1.1111111
    assert vec2 == Vector2(1.11, 2.22)
