import socket
import pickle
import pyglet
import time
import _thread
from utils.config import config
from pyglet.window import key


class Sender:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.m_x = None
        self.m_y = None
        self.m_press = None


class Receiver:
    def __init__(self):
        self.width = None
        self.height = None
        self.players = {}
        self.bullets = set()
        self.walls = None


def run_client_game(rec, send):
    win = pyglet.window.Window(rec.width, rec.height)
    moving_batch = pyglet.graphics.Batch()
    static_batch = pyglet.graphics.Batch()

    background = pyglet.shapes.Rectangle(
        0, 0, rec.width, rec.height, color=config['color']['background'], batch=static_batch)
    walls = set()
    for wall in rec.walls:
        walls.add(pyglet.shapes.Rectangle(
            *wall, color=config['color']['wall'], batch=static_batch))

    players = {}
    for i, p in rec.players.items():
        if p[2] == "T":
            players[i] = pyglet.shapes.Circle(
                p[0], p[1], config['player']['radius'], batch=moving_batch, color=config['color']['enemy'])
        else:
            players[i] = pyglet.shapes.Circle(
                p[0], p[1], config['player']['radius'], batch=moving_batch, color=config['color']['ally'])

    bullets = {}

    keys = key.KeyStateHandler()
    win.push_handlers(keys)

    def update_keys(dt):
        send.x = keys[key.D] - keys[key.A]
        send.y = keys[key.W] - keys[key.S]

    def update_moving(dt):
        for i in players.keys():
            try:
                players[i].x = rec.players[i][0]
                players[i].y = rec.players[i][1]
            except KeyError:
                players[i].visible = False
        for i in rec.bullets.keys():
            if i not in bullets:
                bullets[i] = pyglet.shapes.Circle(
                    rec.bullets[i][0], rec.bullets[i][1], config['bullet']['radius'], batch=moving_batch, color=config['color']['bullet'])
            else:
                bullets[i].x = rec.bullets[i][0]
                bullets[i].y = rec.bullets[i][1]
        exploded = set()
        for i in bullets.keys():
            if i not in rec.bullets:
                exploded.add(i)
        for i in exploded:
            del bullets[i]

    pyglet.clock.schedule_interval(update_keys, 1/config['update_rate'])
    pyglet.clock.schedule_interval(update_moving, 1/config['update_rate'])

    @win.event
    def on_draw():
        win.clear()
        static_batch.draw()
        moving_batch.draw()

    @win.event
    def on_mouse_motion(x, y, dx, dy):
        send.m_x = x + dx
        send.m_y = y + dy

    @win.event
    def on_mouse_press(x, y, button, modifiers):
        print(send.x)
        if send.m_press == False:
            send.m_press = True
        else:
            send.m_press = False

    pyglet.app.run()


def run_client(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((addr, port))
        print("Connected")
    except:
        print("Something went wrong")

    # default status, means we were not allowed to join the game or that the game ended later on

    status = "end"
    try:
        status = pickle.loads(s.recv(4096))
        print("Received game status")
    except:
        print("Couldn't receive game status")

    sender = Sender()
    receiver = Receiver()
    connected = False
    running = False
    while status != "end":
        # time.sleep(2)
        connected = True
        print(f"status: '{status}'")

        try:
            s.send(pickle.dumps("connected"))
        except socket.error as e:
            print("Couldn't send connection status")
            print(e)
        # load map here
        if status == "lobby":
            pass
        elif status == "start":
            try:
                game_map = pickle.loads(s.recv(4096))
                receiver.walls = game_map[0]
                receiver.width = game_map[1]
                receiver.height = game_map[2]

                print(game_map)
                s.send(pickle.dumps("received"))
            except:
                print("Couldn't receive game map")
        # game_loop
        elif status == "game":
            try:
                if receiver.players == {}:
                    _thread.start_new_thread(
                        run_client_game, (receiver, sender))
                players, bullets = pickle.loads(s.recv(4096))
                receiver.players = players
                receiver.bullets = bullets
                # print(bullets)
                s.send(pickle.dumps(sender))
            except Exception as e:
                print(e)
                print("Couldn't receive player positions")

        else:
            print("Received unknown status")
            break

        try:
            status = pickle.loads(s.recv(4096))
        except:
            print("Couldn't receive game status")
            status = "end"

    s.close()
