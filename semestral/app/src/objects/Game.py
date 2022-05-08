from src.objects.Player import Player
from src.objects.ObjectRect import ObjectRect
from src.objects.ObjectCircle import ObjectCircle
from utils.config import config
from utils.map import mp
import pyglet


class Game:
    def __init__(self, win, walls):
        self.players = set()
        self.bullets = set()
        self.objects = set()
        self.win = win

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
        obj.update(dt)
        for o in self.objects:
            if obj.is_colliding(o):
                obj.resolve_collision(o)

        obj.shape.x = obj.pos.x
        obj.shape.y = obj.pos.y

    def update(self, dt):
        """Updates all game entities

        Args:
            dt (float): difference in time
        """
        hit = set()
        dead = set()

        for p in self.players:
            self.update_movable(p, dt)
            for b in self.bullets:
                if p.is_colliding(b):
                    hit.add(b)
                    p.hp -= config['bullet']['damage']
            if p.hp <= 0:
                dead.add(p)

        for p in dead:
            p.shape.color = (255, 0, 0)

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

    g = Game(win, mp)

    #r = ObjectRect(120, 200, 100, 200, batch=batch)
    r = pyglet.shapes.Rectangle(0, 0, win.width, win.height,
                                color=config['color']['background'], batch=batch)
    p = Player(win.width//2, win.width//2, 0, batch)
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
