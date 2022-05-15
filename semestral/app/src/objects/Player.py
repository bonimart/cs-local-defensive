from src.objects.ObjectCircle import ObjectCircle
from src.objects.Bullet import Bullet
from src.objects.Gun import Gun
from utils.Vector import Vector
from utils.config import config


class Player(ObjectCircle):
    speed = config['player']['speed']

    def __init__(self, x, y, team, vel=Vector(0, 0)):
        super().__init__(x, y, config['player']['radius'], vel=vel)
        # state attributes
        self.id = None
        self.team = team
        self.hp = config['player']['max_hp']
        self.dead = False
        # timer to limit player's fire rate
        self.bullet_timer = 0
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.gun = Gun(0, 0, 0, 0)
        # client input
        self.mouse_pos = Vector(0, 0)
        self.mouse_press = False
        self.dash = False

    def update(self, dt):
        """Updates player position, velocity and gun position based on user input

        Args:
            dt (float): difference in time
        """
        self.vel = self.vel.normalize()

        self.bullet_timer = max(0, self.bullet_timer - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)
        self.dash_timer = max(0, self.dash_timer - dt)

        gun_vec = (self.mouse_pos - self.pos).normalize()
        self.gun.x = self.pos.x + gun_vec.x * self.r
        self.gun.y = self.pos.y + gun_vec.y * self.r
        self.gun.x2 = self.pos.x + gun_vec.x * \
            (self.r + config['gun']['length'])
        self.gun.y2 = self.pos.y + gun_vec.y * \
            (self.r + config['gun']['length'])

        if self.dash == True and self.canDash():
            self.dash_timer = config['player']['dash_time']
            self.dash_cooldown = config['player']['dash_cd']

        if self.isDashing():
            self.updatePos(dt, config['player']['dash_speed'])
        else:
            self.updatePos(dt, config['player']['speed'])

    def canDash(self):
        return self.dash_cooldown == 0

    def isDashing(self):
        if self.dash_timer > 0:
            return True
        return False

    def update_shoot(self):
        if self.mouse_press and self.bullet_timer <= 0:
            self.bullet_timer = config['player']['bullet_timer']
            return self.shoot(self.mouse_pos.x, self.mouse_pos.y)
        return None

    def shoot(self, x: int, y: int) -> Bullet:
        """Shoot a bullet towards the given position

        Args:
            x (int): x coordinate of target point
            y (int): y coordinate of target point

        Returns:
            Bullet: the bullet player just fired
        """
        v = Vector(x - self.pos.x, y - self.pos.y).normalize()
        return Bullet(self.pos.x + v.x * (self.r + config['gun']['length']),
                      self.pos.y + v.y *
                      (self.r + config['gun']['length']),
                      v.x, v.y, self.team)

    def get_hit(self, bullet):
        """Update player state on hit

        Args:
            bullet (Bullet): evil bullet that hit our player
        """
        if not config['friendly_fire'] and bullet.team == self.team:
            return
        self.hp = max(0, self.hp - bullet.damage)
        if self.hp == 0:
            self.dead = True
