import socket
import pickle
import pyglet
import time


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

    connected = False
    while status != "end":
        connected = True
        print(f"status: '{status}'")
        time.sleep(2)

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
                print(game_map)
                s.send(pickle.dumps("received"))
            except:
                print("Couldn't receive game map")
        # game_loop
        elif status == "game":
            try:
                player_positions = pickle.loads(s.recv(4096))
                print(player_positions)
                s.send(pickle.dumps("received"))
            except:
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
