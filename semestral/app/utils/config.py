config = {
    'player': {
        'radius': 20,
        'speed': 150,
        'dash_speed': 300,
        'max_hp': 1,
        'bullet_timer': 0.25,
        'dash_cd': 3,
        'dash_time': 0.5
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
        'speed': 400,
        'damage': 1
    },
    'window': {
        'width': 1400,
        'height': 800,
        'border': 2
    },
    'color': {
        'self': (55, 175, 195),
        'cooldown': (25, 145, 165),
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
    'status': {'lobby': 'lobby',
               'start': 'start',
               'game': 'game',
               'game_over': 'game_over',
               'end': 'end'},
    'reply': {'connected': f'connected',
              'disconnected': f'disconnected',
              'received': f'received'},
    'friendly_fire': False,
    'frame_rate': 120.,
    'update_rate': 250.,
    'debug': False,
    'num_of_players': 2,
    'fading_factor': 5,
    'rcv_size': 4096,
    # ? these are not points but ranges (x_range, y_range)
    't_spawn': ((0, 190), (0, 350)),
    'ct_spawn': ((1040, 1400), (640, 800)),
    'hit_point_radius': 20,
    'font': 'Times New Roman',
    'font_size': 50,
    'game_over_delay': 1
}
