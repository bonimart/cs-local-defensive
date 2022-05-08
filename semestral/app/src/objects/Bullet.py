from src.objects.ObjectCircle import ObjectCircle
from src.objects.ObjectRect import ObjectRect
from utils.Vector import Vector
from utils.config import config


class Bullet(ObjectCircle):
    def __init__(self, x, y, velx, vely, batch=None):
        super().__init__(x, y, config['bullet']['radius'],
                         batch=batch, color=config['color']['bullet'])
        self.vel = Vector(velx, vely)

    def resolve_collision(self, other):
        l = other.pos.x - other.size.x / 2
        r = other.pos.x + other.size.x / 2
        b = other.pos.y - other.size.y / 2
        u = other.pos.y + other.size.y / 2

        px = max(l, min(self.pos.x, r))
        py = max(b, min(self.pos.y, u))
        p = Vector(px, py)

        v = Vector(self.pos.x - px, self.pos.y - py)
        if v.norm() > 0:
            self.pos += v * (self.r - self.pos.distance(p)) / v.norm()
        if v.x == 0:
            self.vel = Vector(self.vel.x, -self.vel.y)
        else:
            self.vel = Vector(-self.vel.x, self.vel.y)

    def update(self, dt):
        """Update position

        Args:
            dt (float): difference in time
        """
        self.pos += self.vel * config['bullet']['speed'] * dt

    def hit():
        pass
