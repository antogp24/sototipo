import pygame
import pytmx
import os
import random
import time
clock = pygame.time.Clock()
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
from pygame.locals import *

from . import engine as engine
from . import levels as lvl

FPS = 60
BACKGROUND_COLOR = (15, 15, 65)

window_scale = 1
window_size = (960 * window_scale, 540 * window_scale)
window = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Prototype")

# Surface and Rect for pixel art scaling
display_scale = 2.5*window_scale
display_size = (window_size[0]/display_scale, window_size[1]/display_scale)
display = pygame.Surface(display_size)


# Timer
class Global_Inaccurate_Timer:
    def __init__(self):
        self.value = 0
        self.go = False

def timer_main_loop(timer, increment):
    if timer.go: timer.value += increment
    return timer

# Levels are in the object layers
tmx = pytmx.load_pygame("data/levels.tmx")
levels = lvl.load_all_levels(tmx)
current_level = levels['1']

enemies = []

player = engine.entity(current_level.start_pos[0], current_level.start_pos[1], 20, 30, 'red', 'player')
player_stamina = 300
player_horizontal_movement_increment = 2
player_wall_slide_timer = 0
player_flipped = False
player_gravity = 0.3
player_momentum_x = 0
player_momentum_y = 0
player_air_timer = 0
player_moving_left = False
player_moving_right = False
player_jumping = False
player_wall_sliding = False
player_available_dashes = 1
player_dashing = False
player_dashed_timer = Global_Inaccurate_Timer()
player_alive = True
player_died_timer = Global_Inaccurate_Timer()
player_holding_up_key = False
player_holding_down_key = False

jump_key_timer = 0

# Camera struct

class Camera:
    def __init__(self, view_collider, zoom, scroll, target, scroll_lag):
        self.view_collider = view_collider
        self.zoom = zoom
        self.true_scroll = scroll
        self.scroll = self.true_scroll.copy()
        self.target = target
        self.screen_shake = 0
        self.scroll_lag = scroll_lag

camera = Camera(
    view_collider=pygame.Rect(0, 0, window_size[0], window_size[1]),
    zoom=2.5,
    scroll=[player.x - display_size[0] / 2 + player.w / 2, 
            player.y - display_size[1] / 2 + player.h / 2 + 100],
    target=[player.x + player.w/2,
            player.y + player.h/2],
    scroll_lag=18,
)

def GetDeltaTime(last_time):
    dt = time.time() - last_time
    dt *= FPS
    last_time = time.time()
    return dt, last_time