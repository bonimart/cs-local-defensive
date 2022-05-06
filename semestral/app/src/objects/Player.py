from src.objects.Movable import Movable
from utils.Vector import Vector
from utils.config import config
from pyglet.window import key
import pyglet.shapes as sh
from math import sin, cos, radians


class Player(Movable, key.KeyStateHandler):
    speed = config['player']['speed']

    def __init__(self, x, y, rotation, batch):
        super().__init__(x, y)
        self.vel = Vector(0, 0)
        self.rotation = 0
        self.vel = Vector(0, 0)
        self.shape = sh.Circle(
            self.pos.x, self.pos.y, config['player']['radius'],
            color=config['player']['self_color'], batch=batch)

    def update(self, dt):
        self.vel.y = self[key.UP] - self[key.DOWN]
        self.vel.x = self[key.RIGHT] - self[key.LEFT]
        self.vel.normalize()

        self.pos += self.vel * Player.speed * dt
        self.shape.anchor_x += self.vel.x * Player.speed * dt
        self.shape.anchor_y += self.vel.y * Player.speed * dt

    def shoot(self):
        pass

    def isHit():
        pass
