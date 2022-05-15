from utils.Vector import Vector
import pyglet.shapes as sh


class Object:
    def __init__(self, x, y, vel=None):
        self.pos = Vector(x, y)
        self.vel = vel

    def updatePos(self, dt, speed):
        self.pos += self.vel * speed * dt
