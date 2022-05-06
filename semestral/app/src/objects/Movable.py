from src.objects.Object import Object
from utils.Vector import Vector


class Movable(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vel = Vector(0, 0)

    def update(self, dt):
        self.pos += self.vel * dt
