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
        self.m_x = 0
        self.m_y = 0
        self.m_press = False


class Receiver:
    def __init__(self):
        self.width = None
        self.height = None
        self.players = {}
        self.bullets = set()
        self.walls = None


def run_client_game(rec, send, status_list):
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
    guns = {}
    for i, p in rec.players.items():
        if p.team == "T":
            players[i] = pyglet.shapes.Circle(
                p.pos.x, p.pos.y, config['player']['radius'], batch=moving_batch, color=config['color']['enemy'])
        else:
            players[i] = pyglet.shapes.Circle(
                p.pos.x, p.pos.y, config['player']['radius'], batch=moving_batch, color=config['color']['ally'])
        guns[i] = pyglet.shapes.Line(p.gun[0].x, p.gun[0].y, p.gun[1].x, p.gun[1].y,
                                     width=config['gun']['width'], color=config['color']['gun'], batch=moving_batch)

    bullets = {}

    keys = key.KeyStateHandler()
    win.push_handlers(keys)

    def update_keys(dt):
        send.x = keys[key.D] - keys[key.A]
        send.y = keys[key.W] - keys[key.S]

    def update_moving(dt):
        for i in players.keys():
            try:
                players[i].x = rec.players[i].pos.x
                players[i].y = rec.players[i].pos.y
                guns[i].x = rec.players[i].gun[0].x
                guns[i].y = rec.players[i].gun[0].y
                guns[i].x2 = rec.players[i].gun[1].x
                guns[i].y2 = rec.players[i].gun[1].y
            except KeyError:
                if players[i].opacity == 0:
                    players[i].visible = False
                    guns[i].visible = False
                else:
                    players[i].opacity -= config['fading_factor']
                    guns[i].opacity -= config['fading_factor']

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
        if "game" not in status_list:
            pyglet.clock.unschedule(update_keys)
            pyglet.app.exit()
            return
        win.clear()
        static_batch.draw()
        moving_batch.draw()

    @win.event
    def on_mouse_motion(x, y, dx, dy):
        send.m_x = x + dx
        send.m_y = y + dy

    @win.event
    def on_mouse_press(x, y, button, modifiers):
        send.m_press = True

    pyglet.app.run()
    win.close()


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
    start = False
    running = False
    status_list = [status]
    while status != "end":
        # time.sleep(1)

        try:
            s.send(pickle.dumps("connected"))
        except socket.error as e:
            print("Couldn't send connection status")
            print(e)
            break
        # load map here
        status_list.pop()
        status_list.append(status)
        if status == "lobby":
            #print(f"status: '{status}'")
            pass
        elif status == "start":
            try:
                print(f"status: '{status}'")
                game_map = pickle.loads(s.recv(4096))
                receiver.walls = game_map[0]
                receiver.width = game_map[1]
                receiver.height = game_map[2]

                # print(game_map)
                s.send(pickle.dumps("received"))
                start = True
            except:
                print("Couldn't receive game map")
        # game_loop
        elif status == "game":
            try:
                if start:
                    print(f"status: '{status}'")
                    _thread.start_new_thread(
                        run_client_game, (receiver, sender, status_list))
                    start = False

                players, bullets = pickle.loads(s.recv(4096))
                receiver.players = players
                receiver.bullets = bullets

                s.send(pickle.dumps(sender))
                sender.m_press = False
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
