from src.objects.Object import Object
from src.objects.ObjectRect import ObjectRect
from utils.Vector import Vector
import pyglet.shapes as sh


class ObjectCircle(Object):
    def __init__(self, x, y, r, batch=None, color=(255, 255, 255)):
        super().__init__(x, y)
        self.r = r
        self.shape = sh.Circle(x, y, r, color=color, batch=batch)

    def resolve_collision(self, other):
        if isinstance(other, ObjectRect):
            l = other.pos.x - other.size.x / 2
            r = other.pos.x + other.size.x / 2
            b = other.pos.y - other.size.y / 2
            u = other.pos.y + other.size.y / 2

            px = max(l, min(self.pos.x, r))
            py = max(b, min(self.pos.y, u))
            p = Vector(px, py)

            v = Vector(self.pos.x - px, self.pos.y - py)
            self.pos += v * (self.r - self.pos.distance(p)) / v.norm()
            return

        else:
            v = Vector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
            self.pos += v * (((self.r + other.r) / v.norm()) - 1)

    def is_colliding(self, other):
        if isinstance(other, ObjectRect):
            # collision circle to rectangle
            '''
            l, b = other.pos - other.size // 2
            r, u = other.pos + other.size // 2
            '''
            l = other.pos.x - other.size.x / 2
            r = other.pos.x + other.size.x / 2
            b = other.pos.y - other.size.y / 2
            u = other.pos.y + other.size.y / 2

            px = max(l, min(self.pos.x, r))
            py = max(b, min(self.pos.y, u))
            return self.pos.distance(Vector(px, py)) <= self.r

        else:
            return self.pos.distance(other.pos) <= self.r + other.r
