from src.server.server import run_server
from src.client.client import run_client
from utils.config import config
import sys

help_string = '''Usage: python3 main.py server|client [IP ADRESS]
------------------------------------------------
In order to play this 2D shooter, you need to connect to a local server.
You can either start a new server and then connect to it, or connect to an existing server straight away.
If you want to create a new server, use 'server' option, if you want to connect to a server, use 'client' option.
IP ADRESS is optional, default ip and port are specified in /utils/config.py.'''

if __name__ == "__main__":
    n_arguments = len(sys.argv)

    wrong_input = False

    if n_arguments <= 1:
        wrong_input = True

    elif n_arguments > 1:
        ip = config['server']['ip']
        port = config['server']['port']
        if n_arguments == 3:
            ip = sys.argv[2]
        elif n_arguments > 3:
            wrong_input = True
        if sys.argv[1] == "server":
            run_server(ip, port)
        elif sys.argv[1] == "client":
            run_client(ip, port)
        else:
            wrong_input = True

    if wrong_input:
        print("Error: wrong arguments given\n")
        print(help_string)
