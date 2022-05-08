from src.objects.ObjectCircle import ObjectCircle
from src.objects.Bullet import Bullet
from utils.Vector import Vector
from utils.config import config
from pyglet.window import key, mouse
import pyglet.shapes as sh
from math import sin, cos, radians


class Player(ObjectCircle):
    speed = config['player']['speed']

    def __init__(self, x, y, rotation, batch):
        super().__init__(x, y, config['player']['radius'],
                         color=config['color']['self'], batch=batch)
        self.vel = Vector(0, 0)
        self.hp = config['player']['max_hp']
        self.rotation = 0
        self.vel = Vector(0, 0)
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        """Updates player position and velocity based on user input

        Args:
            dt (float): difference in time
        """
        self.vel.y = self.key_handler[key.UP] - self.key_handler[key.DOWN]
        self.vel.x = self.key_handler[key.RIGHT] - self.key_handler[key.LEFT]
        self.vel = self.vel.normalize()

        self.pos += self.vel * Player.speed * dt

    def shoot(self, x, y):
        v = Vector(x - self.pos.x, y - self.pos.y).normalize()
        return Bullet(self.pos.x + v.x * (self.r + 2 * config['bullet']['radius']),
                      self.pos.y + v.y *
                      (self.r + 2 * config['bullet']['radius']),
                      v.x, v.y,
                      batch=self.shape._batch)

    def isHit():
        pass
