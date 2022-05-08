from src.objects.Object import Object
from utils.Vector import Vector
import pyglet.shapes as sh


class ObjectRect(Object):
    def __init__(self, x, y, w, h, color=(255, 255, 255), batch=None):
        super().__init__(x+w//2, y+h//2)
        self.size = Vector(w, h)
        self.shape = sh.Rectangle(
            x, y, w, h, color=color, batch=batch)
