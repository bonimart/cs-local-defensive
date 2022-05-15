from src.objects.Object import Object
from src.objects.ObjectRect import ObjectRect
from utils.Vector import Vector
import utils.collisions as clsn


class ObjectCircle(Object):
    """
    Class for storing circular objects derived from Object
    """

    def __init__(self, x, y, r, vel=None):
        super().__init__(x, y, vel=vel)
        self.r = r

    def resolve_collision(self, other: Object):
        """Resolves collision with another Object by moving self so that collision is not hapenning

        Args:
            other (Object): colliding object
        """
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

    def is_colliding(self, other: Object) -> bool:
        """Returns if self and other are colliding

        Args:
            other (Object): Object, which might be colliding with self

        Returns:
            bool: true if objects collide, false otherwise
        """
        if isinstance(other, ObjectRect):
            return clsn.circleRectangle(self, other)
        elif isinstance(other, ObjectCircle):
            return clsn.circleCircle(self, other)
