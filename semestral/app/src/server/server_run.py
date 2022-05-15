import socket
from queue import Queue
import _thread
import random
import pickle
import pyglet
import copy
import time
from utils.config import config
from utils.map import mp
from utils.Vector import Vector
from src.objects.Game import Game
from src.objects.Player import Player
from src.objects.ObjectCircle import ObjectCircle
from src.objects.PlayerBot import PlayerBot
from src.server.Server import Server

help_string = '''
Usage:
------
help - print this message
start - start the game
restart - reset to lobby after the game has ended
exit - shutdown the server
'''


class Client:
    def __init__(self):
        self.player = None
        self.ready = False


class PlayerData:
    def __init__(self, p):
        self.id = p.id
        self.pos = p.pos
        self.gun = (Vector(p.gun.x, p.gun.y), Vector(p.gun.x2, p.gun.y2))
        self.team = p.team


def check_for_connection(socket, status):
    socket.send(pickle.dumps(status))
    reply = pickle.loads(socket.recv(config['rcv_size']))
    if reply != config['reply']['connected']:
        return False
    return True


def client_thread(s, player_id, server):

    while server.status != config['status']['end']:
        reply = None
        try:
            if server.status == config['status']['lobby']:
                if not check_for_connection(s, server.status):
                    print(f"Received wrong reply from {player_id}")
                    break
                pass
            elif server.status == config['status']['start']:
                if not check_for_connection(s, server.status):
                    print(f"Received wrong reply from {player_id}")
                    break
                s.send(pickle.dumps(
                    (mp, config['window']['width'], config['window']['height'])))
                reply = pickle.loads(s.recv(config['rcv_size']))
                if reply != f"received":
                    print(f"Received wrong reply from {player_id}")
                    break

                # ? the game will start only when this player is the last one to be ready
                if not server.clients[player_id].ready:
                    server.clients[player_id].ready = True
                    if server.readyCheck():
                        server.startGame()
                        print(f"Everyone ready, starting the game")

                # ? make every client know which player they are
                if server.readyCheck():
                    for p in server.game.players:
                        if p.id == player_id:
                            threaded_player = p

            elif server.status == config['status']['game']:

                if server.game.isOver():
                    over = True
                else:
                    over = False

                if not check_for_connection(s, server.status):
                    print(f"Received wrong reply from {player_id}")
                    break

                plrs = {p.id: PlayerData(p) for p in server.game.players}
                blts = {b.id: (b.pos.x, b.pos.y) for b in server.game.bullets}

                s.send(pickle.dumps((plrs, blts, threaded_player)))
                reply = pickle.loads(s.recv(config['rcv_size']))

                if threaded_player in server.game.players:
                    threaded_player.mouse_pos.x = reply.m_x
                    threaded_player.mouse_pos.y = reply.m_y
                    threaded_player.mouse_press = reply.m_press
                    threaded_player.vel.x = reply.x
                    threaded_player.vel.y = reply.y
                    threaded_player.dash = reply.dash

                if over:
                    time.sleep(config['game_over_delay'])
                    print(f"Game is over: {server.game.whoWon()} won")
                    server.endGame()

            elif server.status == config['status']['game_over']:
                if not check_for_connection(s, server.status):
                    print(f"Received wrong reply from {player_id}")
                    break
                s.send(pickle.dumps(server.game.whoWon()))
                reply = pickle.loads(s.recv(config['rcv_size']))
                if reply != f"received":
                    print(f"Received wrong reply from {player_id}")
                    break

            else:
                print("Server received unknown status")
                break

        except Exception as e:
            print(
                f"Exception occured during communication with client {player_id}")
            print(print(e))
            break

    print(f"Terminating communication with client {player_id}")
    s.close()
    del server.clients[player_id]
    return


def input_thread(s, server):

    inp = ""
    while inp != "exit":
        inp = input()
        if inp == "help":
            print(help_string)
        elif inp == "start":
            server.status = config['status']['start']
        elif inp == 'restart' and server.status == config['status']['game_over']:
            server.status = config['status']['lobby']

    server.status = config['status']['end']
    s.shutdown(socket.SHUT_RDWR)


def run_server(host, port):
    """Runs a server that can host the game

    Args:
        host (string): host ip address
        port (int): port where the server should listen for new connections
    """
    server = Server()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ? making sure the address is reusable
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))
        print(
            f"Lobby on port {s.getsockname()[1]} of address {s.getsockname()[0]} successfully created")
    except socket.error as e:
        print("Socket creation failed with error:", str(e))
        return

    s.listen(config['num_of_players'])
    print("Waiting for connections...")

    _thread.start_new_thread(input_thread, (s, server))
    print("Type 'help' for more information")

    server.status = config['status']['lobby']
    while server.status != config['status']['end']:
        try:
            sock, addr = s.accept()
            sock.settimeout(5)
        except OSError:
            break
        except KeyboardInterrupt:
            print("Received keyboard interrupt")
            break
        if server.status == config['status']['game']:
            print("Someone tried to connect during the game, sad for him")
            sock.close()
        else:
            _thread.start_new_thread(
                client_thread, (sock, server.client_id, server))
            server.addClient(Client())
            print("New connection on address ", addr[0],
                  f", id - {server.client_id}, {len(server.clients.keys())}/{config['num_of_players']} players connected")

    server.status = config['status']['end']
    print("Server is shutting down")
    s.close()
