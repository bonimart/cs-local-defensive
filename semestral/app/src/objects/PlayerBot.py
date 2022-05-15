from src.objects import Object
from src.objects.Player import Player
from src.objects.ObjectCircle import ObjectCircle
from utils.Vector import Vector
from utils.config import config
import utils.collisions as clsn
import random


class PlayerBot(Player):
    """
    Bot class derived from Player
    """

    def __init__(self, x, y, team):
        super().__init__(x, y, team, vel=Vector(
            random.random(), random.random()).normalize())
        self.state: str = "search"
        self.target: Player = None
        self.search_radius = ObjectCircle(x, y,
                                          config['bot']['search_radius'])

    def update_timer(self, dt: float):
        self.bullet_timer -= dt

    def reset_timer(self):
        self.bullet_timer = config['bot']['kill_cd']*(1 + random.random())

    def can_see(self, target: Player, obstacles: set) -> bool:
        """Method that checks if bot can see another Player

        Args:
            target (Player): target which the bot might see
            obstacles (Object): obstacles between bot and target

        Returns:
            bool: true if bot can see the target, false otherwise
        """
        if not self.search_radius.is_colliding(target):
            return False
        # ! checking only the center might not be the best idea, but it's
        # ! efficient
        botTargetLine = (self.pos, target.pos)
        for o in obstacles:
            if clsn.lineRect(botTargetLine, o):
                return False
        return True

    def follow_target(self):
        """Method that updates bots velocity based on relative position
        to its target
        """
        # ? bot tries to stay in distance that is half of its search radius rn
        self.vel = (self.vel + (self.target.pos - self.pos) *
                    (((self.target.pos - self.pos).norm() -
                      self.search_radius.r/2)
                     / config['bot']['attraction_coefficient'])).normalize()

    def resolve_collision(self, other: Object):
        """Method that updates bots velocity when colliding

        Args:
            other (Object): object that collides with the bot
        """
        # ? bot moves randomly when collision occurs
        self.vel = Vector(random.choice([-1, 1])*random.random(),
                          random.choice([-1, 1])*random.random()).normalize()
        super().resolve_collision(other)

    def update(self, dt: float):
        """Update PlayerBot attributes

        Args:
            dt (float): difference in time
        """
        self.updatePos(dt, config['player']['speed'])
        self.search_radius.pos = self.pos
        # ? bot points its gun in the direction of its movement while searching
        if self.state == "search":
            aim = self.vel
        # ? bot points its gun in the direction of its target when hunting
        elif self.state == "KILL":
            aim = (self.target.pos - self.pos).normalize()

        self.gun.x = self.pos.x + aim.x * self.r
        self.gun.y = self.pos.y + aim.y * self.r
        self.gun.x2 = self.pos.x + aim.x * \
            (self.r + config['gun']['length'])
        self.gun.y2 = self.pos.y + aim.y * \
            (self.r + config['gun']['length'])
