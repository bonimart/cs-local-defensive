from src.objects.Player import Player
from src.objects.ObjectCircle import ObjectCircle
from utils.Vector import Vector
from utils.config import config
import random


class PlayerBot(Player):
    # STATES: SEARCH, KILL

    def __init__(self, x, y, rotation, batch, color=(255, 255, 255)):
        super().__init__(x, y, rotation, batch)
        self.shape.color = color
        self.state = "search"
        self.target = None
        self.timer = 0
        self.vel = Vector(random.random(), random.random())
        self.search_radius = ObjectCircle(x, y, config['bot']['search_radius'])

    def update(self, dt, players):
        if self.state == "search":
            seen = set()
            self.timer = max(0, self.timer - dt)
            for p in players - {self}:
                if self.search_radius.is_colliding(p):
                    seen.add(p)
            if seen != set():
                self.target = random.sample(seen, 1)[0]
                self.state = "kill"

        elif self.state == "kill":
            if self.search_radius.is_colliding(self.target):
                if self.timer == 0:
                    self.timer = config['bot']['kill_cd']
                    return self.shoot(self.target.pos.x, self.target.pos.y)
                else:
                    self.timer = max(0, self.timer - dt)
            else:
                self.target = None
                self.state = "search"

        self.vel = self.vel.normalize()
        self.pos += self.vel * Player.speed * dt

    def resolve_collision(self, other):
        self.vel = Vector(random.choice(
            [-1, 1])*random.random(), random.choice([-1, 1])*random.random())
        super().resolve_collision(other)
