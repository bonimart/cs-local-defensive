from src.objects.Player import Player
from src.objects.Bullet import Bullet
from src.objects.PlayerBot import PlayerBot
from src.objects.ObjectRect import ObjectRect
from src.objects.ObjectCircle import ObjectCircle
from utils.config import config
from utils.map import mp
import pyglet
import random


class Game:
    def __init__(self, win, walls, debug=False):
        self.players = set()
        self.bullets = set()
        self.objects = set()
        self.win = win
        self.debug = debug

    def isOver(self):
        t_dead = True
        ct_dead = True
        for p in self.players:
            if p.team == 'T':
                t_dead = False
            elif p.team == 'CT':
                ct_dead = False
        return ct_dead or t_dead

    def update_movable(self, obj, dt):
        if isinstance(obj, PlayerBot):
            self.update_bot(obj, dt)

        obj.update(dt)

        for o in self.objects:
            if obj.is_colliding(o):
                obj.resolve_collision(o)

    def update_bot(self, bot, dt):
        seen_walls = set()
        for wall in self.objects:
            if bot.search_radius.is_colliding(wall):
                seen_walls.add(wall)

        if bot.state == "search":
            bot.shape.color = config['color']['ally']
            seen = set()
            bot.timer = max(0, bot.timer - dt)
            for p in self.players - {bot}:
                if bot.search_radius.is_colliding(p) and bot.can_see(p, seen_walls):
                    seen.add(p)
            if seen != set():
                bot.target = random.sample(seen, 1)[0]
                bot.state = "kill"

        elif bot.state == "kill":
            bot.shape.color = config['color']['enemy']
            if bot.target in self.players and bot.search_radius.is_colliding(bot.target) and bot.can_see(bot.target, seen_walls):
                if self.debug:
                    bot.l = pyglet.shapes.Line(
                        bot.pos.x, bot.pos.y, bot.target.pos.x, bot.target.pos.y, batch=bot.shape._batch)
                if bot.timer == 0:
                    bot.timer = config['bot']['kill_cd']*(1 + random.random())
                    b = bot.shoot(bot.target.pos.x, bot.target.pos.y)
                    shot_himself = False
                    for o in self.objects:
                        if b.is_colliding(o):
                            shot_himself = True
                    if shot_himself:
                        bot.hp -= config['bullet']['damage']
                    else:
                        self.bullets.add(b)

                else:
                    bot.timer = max(0, bot.timer - dt)
            else:
                bot.l = None
                bot.target = None
                bot.state = "search"

    def update(self, dt):
        """Updates all game entities

        Args:
            dt (float): difference in time
        """
        hit = set()
        dead = set()

        for p in self.players:
            self.update_movable(p, dt)
            for p2 in self.players - {p}:
                if p.is_colliding(p2):
                    p.resolve_collision(p2)
            for b in self.bullets:
                if p.is_colliding(b):
                    hit.add(b)
                    p.hp -= config['bullet']['damage']
            if p.hp <= 0:
                dead.add(p)

        for p in dead:
            p.shape.visible = False
            self.players.remove(p)

        for b in hit:
            self.bullets.remove(b)

        exploded = set()
        for b in self.bullets:
            self.update_movable(b, dt)
            for b2 in self.bullets - {b}:
                if b.is_colliding(b2):
                    exploded.add(b)
                    exploded.add(b2)

        for b in exploded:
            self.bullets.remove(b)


def run_game():
    win = pyglet.window.Window(
        config['window']['width'], config['window']['height'])
    batch = pyglet.graphics.Batch()

    g = Game(win, mp, debug=False)

    #r = ObjectRect(120, 200, 100, 200, batch=batch)
    r = pyglet.shapes.Rectangle(0, 0, win.width, win.height,
                                color=config['color']['background'], batch=batch)
    p = Player(win.width//2, win.width//2, 0, batch)
    for i in range(5):
        b = PlayerBot(random.randrange(0, win.width),
                      random.randrange(0, win.height), 0, batch=batch, color=config['color']['enemy'])
        if g.debug:
            b.search_radius.shape.visible = True
            b.search_radius.shape.opacity = 40
        else:
            b.search_radius.shape.visible = False
        g.players.add(b)
    g.players.add(p)

    for o in mp:
        g.objects.add(ObjectRect(
            *o, color=config['color']['wall'], batch=batch))

    win.push_handlers(p.key_handler)
    pyglet.clock.schedule_interval(g.update, 1 / config['frame_rate'])

    @win.event
    def on_draw():
        win.clear()
        batch.draw()

    @win.event
    def on_mouse_press(x, y, button, modifiers):
        b = p.shoot(x, y)
        shot_himself = False
        for o in g.objects:
            if b.is_colliding(o):
                shot_himself = True
        if shot_himself:
            p.hp -= config['bullet']['damage']
        else:
            g.bullets.add(b)

    pyglet.app.run()
