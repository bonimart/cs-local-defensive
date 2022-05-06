from src.objects.Player import Player
from utils.config import config
import pyglet


class Game:
    def __init__(self):
        self.players = set()
        self.bullets = set()
        self.objects = set()

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


def run_game():
    win = pyglet.window.Window(
        config['window']['width'], config['window']['height'])
    batch = pyglet.graphics.Batch()

    p = Player(win.width//2, win.width//2, 0, batch)
    win.push_handlers(p)
    pyglet.clock.schedule_interval(p.update, 1 / 120.)

    @win.event
    def on_draw():
        win.clear()
        batch.draw()

    pyglet.app.run()
