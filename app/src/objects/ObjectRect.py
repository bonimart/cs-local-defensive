from src.objects.Object import Object
from utils.Vector import Vector
import pyglet.shapes as sh


class ObjectRect(Object):
    """
    Class for storing rectangles derived from Object
    """

    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.size = Vector(w, h)
