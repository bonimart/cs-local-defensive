from src.objects.Player import Player
from src.objects.ObjectRect import ObjectRect
from src.objects.ObjectCircle import ObjectCircle
from utils.config import config
from utils.map import mp
import pyglet


class Game:
    def __init__(self, win):
        self.players = []
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

    def update(self, dt):
        for p in self.players:
            p.update(dt)

            if p.pos.x - p.r < 0:
                p.pos.x = p.r
            elif p.pos.x + p.r > self.win.width:
                p.pos.x = self.win.width - p.r

            if p.pos.y - p.r < 0:
                p.pos.y = p.r
            elif p.pos.y + p.r > self.win.height:
                p.pos.y = self.win.height - p.r

            for o in self.objects:
                if p.is_colliding(o):
                    p.resolve_collision(o)

            p.shape.x = p.pos.x
            p.shape.y = p.pos.y


def run_game():
    win = pyglet.window.Window(
        config['window']['width'], config['window']['height'])
    batch = pyglet.graphics.Batch()

    g = Game(win)

    #r = ObjectRect(120, 200, 100, 200, batch=batch)
    p = Player(win.width//2, win.width//2, 0, batch)
    g.players.append(p)

    for o in mp:
        g.objects.add(ObjectRect(*o, batch=batch))

    win.push_handlers(p)
    pyglet.clock.schedule_interval(g.update, 1 / config['frame_rate'])

    @win.event
    def on_draw():
        win.clear()
        batch.draw()

    pyglet.app.run()
