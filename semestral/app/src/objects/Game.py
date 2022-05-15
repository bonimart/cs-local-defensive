from src.objects.Player import Player
from src.objects.Bullet import Bullet
from src.server.server import Client
from src.objects.PlayerBot import PlayerBot
from src.objects.ObjectRect import ObjectRect
from src.objects.ObjectCircle import ObjectCircle
from utils.config import config
import pyglet
import random


class Game:
    """
    Class for storing information about game instance
    """

    def __init__(self, walls, clients):
        self.bullets = set()
        self.walls = set()
        self.bullet_id = 0
        for w in walls:
            self.walls.add(ObjectRect(*w))
        self.players = self.generate_positions(clients)

    def generate_position(self, players: set, range_x: tuple, range_y: tuple) -> ObjectCircle:
        """Randomly generates position for a player.
        Players are not taken from self because they don't exist at the time

        Args:
            players (set(players)): players that have their positions already generated
            range_x (tuple(int)): range on the x-axis where the position can be generated
            range_y (tuple(int)): range on the y-axis where the position can be generated

        Returns:
            ObjectCircle: circle which represents position of the new player
        """
        collides = True
        while collides:
            collides = False
            x = random.randint(*range_x)
            y = random.randint(*range_y)
            c = ObjectCircle(x, y, config['player']['radius'])
            for w in self.walls:
                if c.is_colliding(w):
                    collides = True
            for p in players:
                if c.is_colliding(p):
                    collides = True
        return c

    def generate_positions(self, clients: dict) -> set(ObjectCircle):
        """Generates positions for all clients and bots, so that the number of total players matches configuration.

        Args:
            clients (dict(int : Client)): dictionary of connected clients

        Returns:
            set(ObjectCircle): set of player positions
        """
        players = set()
        m = max(clients.keys()) + 1
        l = len(clients.keys())
        ids = [k for k in clients.keys()]
        for j in [m+i for i in range(0, config['num_of_players']-l)]:
            ids.append(j)
        random.shuffle(ids)
        for i in range(len(ids)):
            if i % 2:
                c = self.generate_position(players, *config['t_spawn'])
                if ids[i] in clients.keys():
                    b = Player(c.pos.x, c.pos.y, "T")
                else:
                    b = PlayerBot(c.pos.x, c.pos.y, "T")
            else:
                c = self.generate_position(players, *config['ct_spawn'])
                if ids[i] in clients.keys():
                    b = Player(c.pos.x, c.pos.y, "CT")
                else:
                    b = PlayerBot(c.pos.x, c.pos.y, "CT")
            b.id = ids[i]
            players.add(b)
        return players

    def isOver(self) -> bool:
        """Check if game has ended, game ends if either team has no players alive

        Returns:
            bool: true if game is over, otherwise false
        """
        players = self.players.copy()
        t_dead = True
        ct_dead = True
        for p in players:
            if p.team == "T":
                t_dead = False
            elif p.team == "CT":
                ct_dead = False
        return t_dead or ct_dead

    def whoWon(self) -> str:
        """Checks which team has won the game

        Returns:
            str: T if terorrists won, CT if counter-terorrists won, None otherwise
        """
        players = self.players.copy()
        t_dead = True
        ct_dead = True
        for p in players:
            if p.team == "T":
                t_dead = False
            elif p.team == "CT":
                ct_dead = False
        if t_dead:
            return "CT"
        elif ct_dead:
            return "T"
        else:
            return None

    def update_movable(self, obj, dt):
        """Updates movable object, that means player or bullet

        Args:
            obj (Object): Object to update
            dt (float): difference in time
        """
        if isinstance(obj, PlayerBot):
            self.update_bot(obj, dt)
        elif isinstance(obj, Player):
            b = obj.update_shoot()
            if b != None and not self.wall_shot(b):
                b.id = self.bullet_id
                self.bullets.add(b)
                self.bullet_id += 1

        obj.update(dt)

        for w in self.walls:
            if obj.is_colliding(w):
                obj.resolve_collision(w)

    def wall_shot(self, bullet: Bullet) -> bool:
        """Checks if bullet was shot into the wall or not

        Args:
            bullet (Bullet): fired bullet

        Returns:
            bool: true if fired bullet collides with any wall, false otherwise
        """
        wall_shot = False
        for w in self.walls:
            if bullet.is_colliding(w):
                wall_shot = True
        return wall_shot

    def update_bot(self, bot: PlayerBot, dt: float):
        """Updates bots in the game

        Args:
            bot (PlayerBot): bot to update
            dt (float): difference in time
        """
        seen_walls = set()
        for wall in self.walls:
            if bot.search_radius.is_colliding(wall):
                seen_walls.add(wall)

        # bot is searching for its prey
        if bot.state == "search":
            seen = set()
            bot.update_timer(dt)
            for p in self.players - {bot}:
                if bot.can_see(p, seen_walls) and p.team != bot.team:
                    seen.add(p)
            if seen != set():
                bot.target = random.sample(seen, 1)[0]
                bot.state = "KILL"

        # bot is hunting the target
        elif bot.state == "KILL":
            if bot.target in self.players and bot.can_see(bot.target, seen_walls):
                if bot.bullet_timer <= 0:
                    bot.reset_timer()
                    b = bot.shoot(bot.target.pos.x, bot.target.pos.y)
                    b.id = self.bullet_id
                    self.bullet_id += 1
                    # bot shot against the wall meaning he shot himself
                    if self.wall_shot(b):
                        bot.get_hit(b)
                    else:
                        self.bullets.add(b)
                else:
                    bot.update_timer(dt)
                # stay close to the target
                bot.follow_target()

            else:
                bot.target = None
                bot.state = "search"

    def update(self, dt: float):
        """Updates all game entities

        Args:
            dt (float): difference in time
        """
        hit = set()
        dead = set()

        for p in self.players:
            self.update_movable(p, dt)
            # collisions between players
            for p2 in self.players - {p}:
                if p.is_colliding(p2):
                    p.resolve_collision(p2)
            # bullet hits
            for b in self.bullets:
                if p.is_colliding(b):
                    hit.add(b)
                    p.get_hit(b)
            # dead players
            if p.dead == True:
                dead.add(p)
        # bury the dead
        for p in dead:
            self.players.remove(p)
        # remove bullets that hit
        for b in hit:
            self.bullets.remove(b)

        exploded = set()
        for b in self.bullets:
            self.update_movable(b, dt)
            # collision between bullets
            for b2 in self.bullets - {b}:
                if b.is_colliding(b2):
                    exploded.add(b)
                    exploded.add(b2)

        for b in exploded:
            self.bullets.remove(b)

        return self

    def run(self):
        """
        Update the game until it is over
        """
        pyglet.clock.schedule_interval(self.update, 1/(config['frame_rate']))
        while not self.isOver():
            pyglet.clock.tick()
