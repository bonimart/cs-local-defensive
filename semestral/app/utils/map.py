from utils.config import config

w = config['window']['width']
h = config['window']['height']
r = config['player']['radius']
b = config['window']['border']
"""
list of all static objects in the game in format (left_corner_x, left_corner_y, width, height)
"""
mp = [
    (0, 0, w, b),
    (0, h-b, w, b),
    (0, 0, b, h),
    (w-b, 0, b, h),
    (300+r, 200, 200, r),
    (700, 200, 350-r, r),
    (200, 450, 300, r),
    (700, 450, 300, r),
    (50+r, 600, 300, r),
    (800, 600, 200, r),
    (1200, 600, 200, r), # -
    (1000, 600, r, 200), # |
    (1000, 300+r, r, 150),
    (1200, 100+r, r, 350),
    (500, 350, r, 350),
    (150, 100, r, 250),
    (700, 0, r, 100)
]
