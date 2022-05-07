from utils.Vector import Vector
import pyglet.shapes as sh


class Object:
    def __init__(self, x, y):
        self.pos = Vector(x, y)
