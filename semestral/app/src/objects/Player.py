from src.objects.ObjectCircle import ObjectCircle
from src.objects.Bullet import Bullet
from utils.Vector import Vector
from utils.config import config
from pyglet.window import key
import pyglet.shapes as sh


class Player(ObjectCircle):
    speed = config['player']['speed']

    def __init__(self, x, y, rotation, batch, vel=Vector(0, 0)):
        super().__init__(x, y, config['player']['radius'],
                         color=config['color']['self'],
                         batch=batch,
                         vel=vel)
        self.hp = config['player']['max_hp']
        self.rotation = 0
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        """Updates player position and velocity based on user input

        Args:
            dt (float): difference in time
        """
        self.vel.y = self.key_handler[key.W] - self.key_handler[key.S]
        self.vel.x = self.key_handler[key.D] - self.key_handler[key.A]
        self.vel = self.vel.normalize()

        self.updatePos(dt, config['player']['speed'])

    def shoot(self, x, y):
        v = Vector(x - self.pos.x, y - self.pos.y).normalize()
        return Bullet(self.pos.x + v.x * (self.r + 2 * config['bullet']['radius']),
                      self.pos.y + v.y *
                      (self.r + 2 * config['bullet']['radius']),
                      v.x, v.y,
                      batch=self.shape._batch)
