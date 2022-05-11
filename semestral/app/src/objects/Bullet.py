from src.objects.ObjectCircle import ObjectCircle
from src.objects.ObjectRect import ObjectRect
from utils.Vector import Vector
from utils.config import config
import utils.collisions as clsn


class Bullet(ObjectCircle):
    def __init__(self, x, y, velx, vely, team, batch=None):
        super().__init__(x, y,
                         config['bullet']['radius'],
                         batch=batch,
                         color=config['color']['bullet'],
                         vel=Vector(velx, vely))
        self.team = team

    def resolve_collision(self, other):
        if isinstance(other, ObjectRect):
            p = clsn.circRectClosestPoint(self, other)
            # vector between our centre and closest point on the rectangle
            v = Vector(self.pos.x - p.x, self.pos.y - p.y)
            if v.norm() > 0:
                self.pos += v * (self.r - self.pos.distance(p)) / v.norm()
            # rotates velocity based on position against wall
            if v.x == 0:
                self.vel = Vector(self.vel.x, -self.vel.y)
            else:
                self.vel = Vector(-self.vel.x, self.vel.y)
        else:
            raise Exception("Bullet can collides with type ObjectRect only")

    def update(self, dt):
        """Update position

        Args:
            dt (float): difference in time
        """
        self.updatePos(dt, config['bullet']['speed'])
