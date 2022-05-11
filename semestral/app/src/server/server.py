import socket
from queue import Queue
import _thread
import random
import pickle
import pyglet
from utils.config import config
from src.objects.Game import Game


def client_thread(s, player_id):
    s.send(pickle.dumps("Zdar"))
    reply = ""
    while True:
        try:
            # 11 bytes
            data = pickle.loads(s.recv(4096))

            print(f"Received {data}")
            break
        except:
            print("Exception occured")
            break

    s.close()


def input_thread(out_q, s):
    running = True
    inp = ""
    while inp != "exit":
        inp = input()
        out_q.put(running)
    running = False
    out_q.put(running)
    s.close()


def run_server(host, port):
    """
    Runs a server that can host a new game\n
    host - host IP address\n
    port - port to run a server on
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
        print(f"Socket on address {s.getsockname()} successfully created")
    except socket.error as e:
        print("Socket creation failed with error", str(e))

    s.listen()
    print("Sever started, waiting for a connection")

    q = Queue()
    _thread.start_new_thread(input_thread, (q, s))

    player_id = 0
    running = q.get()
    while running:
        try:
            sock, addr = s.accept()
        except OSError:
            print("Socket closed")
            return
        print("Connected to:", addr)
        _thread.start_new_thread(client_thread, (sock, player_id))
        player_id += 1
        running = q.get()
