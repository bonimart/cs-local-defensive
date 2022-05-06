from utils.Vector import Vector


class Object:
    def __init__(self, x, y):
        self.pos = Vector(x, y)
        self.shape = None

    def is_colliding(self, other):
        pass
