class Receiver:
    """
    helper class that stores game information received from the server
    """

    def __init__(self):
        self.main_player = None
        self.width = None
        self.height = None
        self.players = {}
        self.bullets = set()
        self.walls = None
        self.won = None
