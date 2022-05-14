import socket
from queue import Queue
import _thread
import random
import pickle
import pyglet
import copy
from utils.config import config
from utils.map import mp
from utils.Vector import Vector
from src.objects.Game import Game, GameNew
from src.objects.Player import Player
from src.objects.ObjectCircle import ObjectCircle
from src.objects.PlayerBot import PlayerBot


status = "lobby"
clients = {}
players = set()
positions = []
bullets = []
gameSave = GameNew(mp, players)
game = None


class Client:
    def __init__(self):
        self.player = None
        self.ready = False


class PlayerData:
    def __init__(self, p):
        self.pos = p.pos
        self.gun = (Vector(p.gun.x, p.gun.y), Vector(p.gun.x2, p.gun.y2))
        self.team = p.team


def generate_position(walls, players, range_x, range_y):
    collides = True
    while collides:
        collides = False
        x = random.randint(*range_x)
        y = random.randint(*range_y)
        c = ObjectCircle(x, y, config['player']['radius'])
        for w in walls:
            if c.is_colliding(w):
                collides = True
        for p in players:
            if c.is_colliding(p):
                colliding = True
    return c


def generate_player_positions(walls, game):
    global players
    global client_id

    players = set()
    m = max(clients.keys()) + 1
    #print(f"Maximum is {m}")
    l = len(clients.keys())
    #print(f"Length is {l}")
    ids = [k for k in clients.keys()]
    for j in [m+i for i in range(0, config['num_of_players']-l)]:
        ids.append(j)
    random.shuffle(ids)
    positions = []
    for i in range(len(ids)):
        #print(f"Iterating id: {i}")
        # terrorist
        if i % 2:
            c = generate_position(
                walls, positions, (0, config['window']['width']/2), (0, config['window']['height']))
            positions.append(c)
            if ids[i] in clients.keys():
                b = Player(c.pos.x, c.pos.y, "T", batch=None)
            else:
                b = PlayerBot(c.pos.x, c.pos.y, "T", batch=None)
            b.id = ids[i]
            game.players.add(b)

        # counter-terrorist
        else:
            c = generate_position(
                walls, positions, (config['window']['width']/2, config['window']['width']), (0, config['window']['height']))
            positions.append(c)
            if ids[i] in clients.keys():
                b = Player(c.pos.x, c.pos.y, "CT", batch=None)
            else:
                b = PlayerBot(c.pos.x, c.pos.y, "CT", batch=None)
            b.id = ids[i]
            game.players.add(b)

    return [[p.pos.x, p.pos.y] for p in positions]


def client_thread(s, player_id):
    global status
    global players
    global positions
    global game

    while status != "end":
        reply = None
        try:
            if status == "lobby":
                s.send(pickle.dumps(status))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))
                #print(f"received {reply} from {player_id}")
                if reply != f"connected":
                    print(f"Received wrong reply from {player_id}")
                    break
            elif status == "start":
                ready = False
                s.send(pickle.dumps(status))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))
                #print(f"received {reply} from {player_id}")
                if reply != f"connected":
                    print(f"Received wrong reply from {player_id}")
                    break

                s.send(pickle.dumps(
                    (mp, config['window']['width'], config['window']['height'])))
                reply = pickle.loads(s.recv(4096))
                if reply != f"received":
                    print(f"Received wrong reply from {player_id}")
                    break
                else:
                    clients[player_id].ready = True

                everyone_ready = True
                for client in clients.values():
                    if client.ready == False:
                        everyone_ready = False
                if everyone_ready:
                    game = copy.deepcopy(gameSave)
                    positions = generate_player_positions(mp, game)
                    status = "game"
                    _thread.start_new_thread(game.run, ())

                    for p in game.players:
                        if p.id == player_id:
                            threaded_player = p

                    print(f"Everyone ready, starting the game")

            elif status == "game":
                if game.isOver():
                    status = "lobby"
                    continue
                s.send(pickle.dumps(status))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))
                #print(f"received {reply} from {player_id}")
                if reply != f"connected":
                    print(f"Received wrong reply from {player_id}")
                    break

                plrs = {p.id: PlayerData(p) for p in game.players}
                blts = {b.id: (b.pos.x, b.pos.y) for b in game.bullets}
                s.send(pickle.dumps((plrs, blts)))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))

                if threaded_player in game.players:
                    threaded_player.mouse_pos.x = reply.m_x
                    threaded_player.mouse_pos.y = reply.m_y
                    threaded_player.mouse_press = reply.m_press
                    threaded_player.vel.x = reply.x
                    threaded_player.vel.y = reply.y

        except Exception as e:
            print(print(e))
            print(f"Couldn't receive data from {player_id}")
            break

    print("CLIENT_THREAD: Killing thread")
    s.close()
    return


def input_thread(s):
    global running
    global status
    inp = ""
    while inp != "exit":
        inp = input()
        if inp == "help":
            print("""***USAGE:***:
    start: starts a new game
    exit: shuts the server down""")
        elif inp == "start":
            status = "start"

    running = False
    status = "end"
    '''
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(s.getsockname())
    s2.close()
    '''
    s.shutdown(socket.SHUT_RDWR)


def run_server(host, port):
    """
    Runs a server that can host a new game\n
    host - host IP address\n
    port - port to run a server on
    """
    global players
    global status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))
        print(f"Socket on address {s.getsockname()} successfully created")
    except socket.error as e:
        print("Socket creation failed with error", str(e))

    s.listen(config['num_of_players'])
    print("Sever started, waiting for a connection")

    running = True
    _thread.start_new_thread(input_thread, (s,))
    print("Type 'help' to list possible commands")

    client_id = 0
    status = "lobby"
    while running:
        try:
            sock, addr = s.accept()
            sock.settimeout(5)
        except OSError:
            print("Socket closed")
            break
        if status == "game":
            print("Someone tried to connect during the game, sad for him")
            sock.close()
        else:
            print("Connected to:", addr)
            _thread.start_new_thread(client_thread, (sock, client_id))
            clients[client_id] = Client()
            client_id += 1

    status = "end"
    print("Server is shutting down")
    s.close()
