from utils.Vector import Vector


def test_operations():
    v1 = Vector(1, 0)

    assert v1 + v1 == Vector(2, 0)
    assert v1 - v1 == Vector(0, 0)
    assert v1 * 0 == Vector(0, 0)
    assert v1 * 10 == Vector(10, 0)
    assert v1 / 1 == v1
    e = None
    try:
        v1 / 0
    except Exception as exc:
        e = exc
    assert type(e) == ZeroDivisionError


def test_distance():
    v1 = Vector(0, 0)
    v2 = Vector(1, 0)
    assert v1.distance(v1) == 0
    assert v1.distance(v2) == 1


def test_normalize():
    v1 = Vector(1, 0)
    assert v1.norm() == 1
    assert v1.normalize() == v1
