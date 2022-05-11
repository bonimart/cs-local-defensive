import socket
import pickle
import pyglet


def run_client(addr, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((addr, port))
        print("Connected")
    except:
        print("Something went wrong")

    try:
        print(f"Received {pickle.loads(s.recv(4096))}")
    except:
        print("Couldn't receive data")

    try:
        s.send(pickle.dumps("Čusé"))
        print("Sent data")
    except socket.error:
        print("Couldn't send data")
