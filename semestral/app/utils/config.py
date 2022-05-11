config = {
    'player': {
        'radius': 20,
        'speed': 200,
        'max_hp': 100
    },
    'bot': {
        'search_radius': 300,
        'kill_cd': .25,
        'attraction_coefficient': 1/10000
    },
    'gun': {
        'width': 10,
        'length': 20
    },
    'bullet': {
        'radius': 10,
        'speed': 500,
        'damage': 20
    },
    'window': {
        'width': 1400,
        'height': 800,
        'border': 2
    },
    'color': {
        'self': (55, 175, 195),
        'ally': (42, 168, 118),
        'enemy': (231, 76, 60),
        'wall': (218, 150, 0),
        'bullet': (131, 114, 93),
        'gun': (85, 85, 85),
        'background': (42, 36, 36)
    },
    'server': {
        'ip': '192.168.1.19',
        'port': 5555
    },
    'friendly_fire': False,
    'frame_rate': 120.,
    'update_rate': 120.,
    'debug': False,
    'num_of_players': 20
}
