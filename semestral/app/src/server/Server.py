from utils.config import config
from src.objects.Game import Game
from utils.map import mp
import _thread


class Server:
    def __init__(self):
        self.client_id = 0
        self.status = config['status']['end']
        self.clients = {}
        self.everyone_ready = False
        self.game = None

    def addClient(self, client):
        self.clients[self.client_id] = client
        self.client_id += 1

    def startGame(self):
        self.game = Game(mp, self.clients)
        self.status = config['status']['game']
        _thread.start_new_thread(self.game.run, ())

    def endGame(self):
        for client in self.clients.values():
            client.ready = False
        self.everyone_ready = False
        self.status = config['status']['game_over']

    def readyCheck(self):
        if not self.everyone_ready:
            self.everyone_ready = True
            for client in self.clients.values():
                if not client.ready:
                    self.everyone_ready = False
        return self.everyone_ready
