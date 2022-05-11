from src.objects.Game import run_game
from src.server.server import run_server
from src.client.client import run_client
from utils.config import config
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "server":
        run_server(config['server']['ip'], config['server']['port'])
    elif sys.argv[1] == "client":
        run_client(config['server']['ip'], config['server']['port'])
else:
    run_game()
