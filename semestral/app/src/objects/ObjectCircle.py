from src.objects.Object import Object
from src.objects.ObjectRect import ObjectRect
from utils.Vector import Vector
import utils.collisions as clsn
import pyglet.shapes as sh


class ObjectCircle(Object):
    def __init__(self, x, y, r, batch=None, color=(255, 255, 255), vel=None):
        super().__init__(x, y, shape=sh.Circle(x, y, r, color=color, batch=batch), vel=vel)
        self.r = r

    def resolve_collision(self, other):
        if isinstance(other, ObjectRect):
            p = clsn.circRectClosestPoint(self, other)
            # vector between our centre and closest point on the rectangle
            v = Vector(self.pos.x - p.x, self.pos.y - p.y)
            # norm == 0 means we are already on the correct point
            if v.norm() > 0:
                self.pos += v * (self.r - self.pos.distance(p)) / v.norm()
        elif isinstance(other, ObjectCircle):
            v = Vector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
            self.pos += v * (((self.r + other.r) / v.norm()) - 1)

    def is_colliding(self, other):
        if isinstance(other, ObjectRect):
            return clsn.circleRectangle(self, other)
        elif isinstance(other, ObjectCircle):
            return clsn.circleCircle(self, other)
