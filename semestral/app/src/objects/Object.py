from utils.Vector import Vector
import pyglet.shapes as sh


class Object:
    def __init__(self, x, y, shape=None, vel=None):
        self.pos = Vector(x, y)
        self.shape = shape
        self.vel = vel

    def updatePos(self, dt, speed):
        self.pos += self.vel * speed * dt
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y
