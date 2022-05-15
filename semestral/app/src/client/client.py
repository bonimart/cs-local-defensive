from utils.config import config
from pyglet.window import key
from src.client.Receiver import Receiver
from src.client.Sender import Sender
import socket
import pickle
import pyglet
import _thread


def run_client_game(rec, send, status_list):
    """Runs an instance of the game based on data in rec

    Args:
        rec (Receiver): container for server input
        send (Sender): container for player input
        status_list (list(string)): list for storing current status
    """

    win = pyglet.window.Window(rec.width, rec.height)
    moving_batch = pyglet.graphics.Batch()
    static_batch = pyglet.graphics.Batch()
    fps_display = pyglet.window.FPSDisplay(win)
    # static batch objects
    background = pyglet.shapes.Rectangle(0, 0,
                                         rec.width, rec.height,
                                         color=config['color']['background'],
                                         batch=static_batch)
    walls = set()
    for wall in rec.walls:
        walls.add(pyglet.shapes.Rectangle(*wall,
                                          color=config['color']['wall'],
                                          batch=static_batch))

    # endgame text label
    text = pyglet.text.Label(font_name=config['font'],
                             font_size=config['font_size'],
                             bold=True,
                             anchor_x='center',
                             x=config['window']['width']//2,
                             y=config['window']['height']//3,
                             batch=static_batch)
    text.opacity = 180
    # objects that get updated during the game
    players = {}
    guns = {}
    bullets = {}
    for i, p in rec.players.items():
        players[i] = pyglet.shapes.Circle(p.pos.x, p.pos.y,
                                          config['player']['radius'],
                                          batch=moving_batch)
        if p.id == rec.main_player.id:
            players[i].color = config['color']['self']
        elif p.team == rec.main_player.team:
            players[i].color = config['color']['ally']
        else:
            players[i].color = config['color']['enemy']
        guns[i] = pyglet.shapes.Line(p.gun[0].x, p.gun[0].y,
                                     p.gun[1].x, p.gun[1].y,
                                     width=config['gun']['width'],
                                     color=config['color']['gun'],
                                     batch=moving_batch)
    health_points = []
    # ? visualize health points as stars
    margin_factor = 2
    outer_to_inner_radius = 2
    spikes = 5
    for n in range(1, rec.main_player.hp+1):
        hp = pyglet.shapes.Star(
            config['window']['width'] - margin_factor *
            n*config['hit_point_radius'],
            margin_factor*config['hit_point_radius'],
            config['hit_point_radius'],
            config['hit_point_radius']/outer_to_inner_radius,
            spikes,
            batch=moving_batch)
        hp.opacity = 160
        health_points.append(hp)
    # movement input
    keys = key.KeyStateHandler()
    win.push_handlers(keys)

    def update_keys(dt):
        send.x = keys[key.D] - keys[key.A]
        send.y = keys[key.W] - keys[key.S]
        send.dash = keys[key.SPACE]

    def update_moving(dt):
        """Updates moving objects on the client side

        Args:
            dt (float): difference of time between updates
        """
        for i in players.keys():
            try:
                if rec.players[i].id == rec.main_player.id:
                    if rec.main_player.dash_cooldown > 0:
                        players[i].color = config['color']['cooldown']
                    else:
                        players[i].color = config['color']['self']
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
                    rec.bullets[i][0],
                    rec.bullets[i][1],
                    config['bullet']['radius'],
                    color=config['color']['bullet'],
                    batch=moving_batch)
            else:
                bullets[i].x = rec.bullets[i][0]
                bullets[i].y = rec.bullets[i][1]
        exploded = set()
        for i in bullets.keys():
            if i not in rec.bullets:
                exploded.add(i)
        for i in exploded:
            del bullets[i]

        while rec.main_player.hp < len(health_points):
            health_points.pop().visible = False

    pyglet.clock.schedule_interval(update_keys, 1/config['client_update_rate'])
    pyglet.clock.schedule_interval(
        update_moving, 1/config['client_update_rate'])

    @ win.event
    def on_draw():
        if status_list[0] == config['status']['game']:
            win.clear()
            static_batch.draw()
            moving_batch.draw()
            fps_display.draw()
        elif status_list[0] == config['status']['game_over']:
            if rec.won == rec.main_player.team:
                text.text = 'Your team has won the game'
            else:
                text.text = 'Your team has lost the game'
            win.clear()
            static_batch.draw()
            text.draw()
        else:
            pyglet.clock.unschedule(update_keys)
            pyglet.app.exit()
            return

    @ win.event
    def on_mouse_motion(x, y, dx, dy):
        send.m_x = x + dx
        send.m_y = y + dy

    @ win.event
    def on_mouse_press(x, y, button, modifiers):
        send.m_press = True

    @ win.event
    def on_close():
        win.has_exit = True
        win.close()
        status_list[0] = config['status']['end']

    pyglet.app.run()
    win.close()


def run_client(addr, port):
    """Runs a client that tries to connect to server on (addr, port)

    Args:
        addr (string): ip address of the server
        port (int): port where the server listens
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((addr, port))
        print("Connected to", addr)
    except Exception as e:
        print("Couldn't connect to the server")

    # default status, means we were not allowed to join the game
    # or that the game ended later on
    status = config['status']['end']

    try:
        status = pickle.loads(s.recv(config['rcv_size']))
    except Exception as e:
        print("Couldn't receive game status from the server due to", e)

    sender = Sender()
    receiver = Receiver()
    # start signalizes to start game thread,
    # this way there's only one instance of it
    start = False
    # variable for game thread
    status_list = [status]
    while status != config['status']['end']:

        if status_list[0] == config['status']['end']:
            print("You have left the game")
            s.send(pickle.dumps(config['reply']['disconnected']))
            break

        try:
            s.send(pickle.dumps(config['reply']['connected']))
        except socket.error as e:
            print("Couldn't send connection status", e)
            break

        status_list[0] = status

        if status == config['status']['lobby']:
            pass
        # load map here
        elif status == config['status']['start']:
            try:
                game_map = pickle.loads(s.recv(config['rcv_size']))
                receiver.walls = game_map[0]
                receiver.width = game_map[1]
                receiver.height = game_map[2]

                s.send(pickle.dumps(config['reply']['received']))
                start = True
                print("The game is going to start")
            except Exception as e:
                print("Couldn't receive game map due to")
                print(e)
        # game_loop
        elif status == config['status']['game']:
            try:
                if start:
                    _thread.start_new_thread(
                        run_client_game, (receiver, sender, status_list))
                    start = False

                receiver.players,
                receiver.bullets,
                receiver.main_player = pickle.loads(
                    s.recv(config['rcv_size']))

                s.send(pickle.dumps(sender))
                sender.m_press = False
            except Exception as e:
                print("Couldn't receive player positions due to", e)

        elif status == config['status']['game_over']:
            try:
                receiver.won = pickle.loads(s.recv(config['rcv_size']))
                s.send(pickle.dumps(config['reply']['received']))
            except Exception as e:
                print("Couldnt receive end-game status due to", e)
                break
        else:
            print("Received unknown status")
            break

        try:
            status = pickle.loads(s.recv(config['rcv_size']))
        except Exception as e:
            print("Couldn't receive game status due to", e)
            status = config['status']['end']
        except KeyboardInterrupt:
            print("Received keyboard interrupt")
            status = config['status']['end']

    s.close()
