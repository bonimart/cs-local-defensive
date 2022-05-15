from src.objects.Player import Player
from src.objects.Bullet import Bullet
from utils.config import config


def test_hit():
    p = Player(0, 0, "T")
    hp = p.hp
    b1 = Bullet(0, 0, 0, 0, "T")
    p.get_hit(b1)
    if not config['friendly_fire']:
        assert p.hp == hp
    else:
        assert p.hp < hp

    hp = p.hp
    b2 = Bullet(0, 0, 0, 0, "CT")
    p.get_hit(b2)
    if config['bullet']['damage'] > 0:
        assert p.hp == 0 or p.hp < hp
