import socket
from queue import Queue
import _thread
import random
import pickle
import pyglet
import copy
from utils.config import config
from utils.map import mp
from src.objects.Game import Game, GameNew
from src.objects.Player import Player
from src.objects.ObjectCircle import ObjectCircle
from src.objects.PlayerBot import PlayerBot


class Client:
    def __init__(self):
        self.player = None
        self.ready = False


status = "lobby"
clients = {}
players = set()
positions = []
bullets = []
game = GameNew(mp, players)


def generate_player_positions(walls):
    global players

    positions = []
    for i in range(config['num_of_players']):
        # terrorist
        if i % 2:
            collides = True
            while collides:
                colliding = False
                x = random.randint(0, config['window']['width']/2)
                y = random.randint(0, config['window']['height']/2)
                c = ObjectCircle(x, y, config['player']['radius'])
                for w in walls:
                    if c.is_colliding(w):
                        colliding = True
                for p in positions:
                    if c.is_colliding(p):
                        colliding = True
                collides = colliding
            positions.append(c)
            b = PlayerBot(x, y, "T", batch=None)
            b.id = i
            players.add(b)

        # counter-terrorist
        else:
            collides = True
            while collides:
                colliding = False
                x = random.randint(
                    config['window']['width']/2, config['window']['width'])
                y = random.randint(
                    0, config['window']['height'])
                c = ObjectCircle(x, y, config['player']['radius'])
                for w in walls:
                    if c.is_colliding(w):
                        colliding = True
                for p in positions:
                    if c.is_colliding(p):
                        colliding = True
                collides = colliding
            positions.append(c)
            b = PlayerBot(x, y, "CT", batch=None)
            b.id = i
            players.add(b)

    return [[p.pos.x, p.pos.y] for p in positions]


def client_thread(s, player_id):
    global status
    global players
    global positions
    global game
    # print(status)
    # s.send(pickle.dumps(status))
    while status != "end":
        reply = None
        try:
            if status == "lobby":
                s.send(pickle.dumps(status))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))
                print(f"received {reply} from {player_id}")
                if reply != f"connected":
                    print(f"Received wrong reply from {player_id}")
                    break
            elif status == "start":
                ready = False
                s.send(pickle.dumps(status))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))
                print(f"received {reply} from {player_id}")
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
                    positions = generate_player_positions(mp)
                    status = "game"
                    _thread.start_new_thread(game.run, ())

                    print(f"Everyone ready, starting the game")

            elif status == "game":
                s.send(pickle.dumps(status))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))
                print(f"received {reply} from {player_id}")
                if reply != f"connected":
                    print(f"Received wrong reply from {player_id}")
                    break

                plrs = {p.id: (p.pos.x, p.pos.y, p.team) for p in game.players}
                blts = {b.id: (b.pos.x, b.pos.y) for b in game.bullets}
                s.send(pickle.dumps((plrs, blts)))
                # 11 bytes
                reply = pickle.loads(s.recv(4096))

        except Exception as e:
            print(print(e))
            print(f"Couldn't receive data from {player_id}")
            break

    print("CLIENT_THREAD: Killing thread")
    s.shutdown(1)
    return


def input_thread(s):
    global running
    global status
    inp = ""
    while inp != "exit":
        inp = input()
        if inp == "help":
            print("""
***USAGE:***:
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
