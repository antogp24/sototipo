from .common import *

def Respawn(player, current_level):
    player.set_pos(current_level.start_pos[0], current_level.start_pos[1])
    player_died_timer.go = False
    player_died_timer.value = 0
    return True