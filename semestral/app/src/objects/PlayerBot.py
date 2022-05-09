from src.objects.Player import Player
from src.objects.ObjectCircle import ObjectCircle
from utils.Vector import Vector
from utils.config import config
import utils.collisions as clsn
import random


class PlayerBot(Player):
    # STATES: SEARCH, KILL

    def __init__(self, x, y, rotation, batch, color=(255, 255, 255)):
        super().__init__(x, y, rotation, batch, vel=Vector(
            random.random(), random.random()).normalize())
        self.shape.color = color
        self.state = "search"
        self.target = None
        self.timer = 0
        self.search_radius = ObjectCircle(x, y,
                                          config['bot']['search_radius'], batch=batch)
        self.l = None

    def can_see(self, target, obstacles):
        line = (self.pos, target.pos)
        for o in obstacles:
            if clsn.lineRect(line, o):
                return False
        return True

    def update(self, dt):
        self.updatePos(dt, config['player']['speed'])
        self.search_radius.pos = self.pos
        self.search_radius.shape.x = self.pos.x
        self.search_radius.shape.y = self.pos.y

    def resolve_collision(self, other):
        self.vel = Vector(random.choice([-1, 1])*random.random(),
                          random.choice([-1, 1])*random.random()).normalize()
        super().resolve_collision(other)
