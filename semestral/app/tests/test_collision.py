from src.objects.ObjectCircle import ObjectCircle
from src.objects.ObjectRect import ObjectRect
from utils.Vector import Vector
import utils.collisions as clsn


def test_circleCircle():
    c1 = ObjectCircle(0, 0, 10)
    assert c1.is_colliding(c1)

    c2 = ObjectCircle(0, 0, 100)
    assert c1.is_colliding(c2)

    c3 = ObjectCircle(50, 50, 10)
    assert not c1.is_colliding(c3)

    c4 = ObjectCircle(10, 0, 0)
    assert c1.is_colliding(c4)


def test_circleRect():
    c1 = ObjectCircle(0, 0, 10)

    r1 = ObjectRect(0, 0, 10, 10)
    assert c1.is_colliding(r1)

    r2 = ObjectRect(10, 0, 10, 10)
    assert c1.is_colliding(r2)

    r3 = ObjectRect(11, 0, 10, 10)
    assert not c1.is_colliding(r3)


def test_lineRect():
    r1 = ObjectRect(0, 0, 10, 10)

    l1 = (Vector(0, 0), Vector(10, 0))
    assert clsn.lineRect(l1, r1)

    l2 = (Vector(20, 0), Vector(30, 10))
    assert not clsn.lineRect(l2, r1)
