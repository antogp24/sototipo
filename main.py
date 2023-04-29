import sys
from data.common import *

import data.camera as cam
import data.death as death

last_time = time.time()

while True:
    dt, last_time = GetDeltaTime(last_time)
    current_fps = int(clock.get_fps())
    
    display.fill(current_level.background_color)
    
    camera = cam.moveCamera(camera, dt)
    camera.target = [player.x + player.w/2, player.y + player.h/2]

    if player_alive:
        # Looking down
        if player_holding_down_key:
            camera.target[1] = player.y + player.h/2 + 20
        else:
            camera.target[1] = player.y + player.h/2

        movement = [0, 0]

        # Horizontal Movement
        direction = 1
        if player_moving_left:
            player_flipped = True
        elif player_moving_right:
            player_flipped = False

        if player_flipped:
            direction = -1
        else:
            direction = 1

        if player_moving_left or player_moving_right:
            increment = player_horizontal_movement_increment*direction*dt
            movement[0] = increment+player_momentum_x

        if player_dashing:
            player_available_dashes -= 1
            player_dashed_timer.go = True
            # camera moves faster to catch up
            camera.scroll_lag = 5
            # horizontal boost
            player_momentum_x += int(12 * direction * dt)
            # vertical boost
            if player_holding_up_key and not(player_moving_left or player_moving_right):
                player_momentum_y += float(-28 * dt)
            # diagonal boost
            elif player_holding_up_key:
                player_momentum_y += float(-18 * dt)
            elif player_holding_down_key:
                player_momentum_y += float(10 * dt)
            player_dashing = False
        else:
            camera.scroll_lag = 18
        player_dashed_timer = timer_main_loop(player_dashed_timer, dt)

        # Make the player fall slower during and after the dash
        if 3 <= player_dashed_timer.value < 15:
            if player_holding_down_key == False:
                player_momentum_y = 0
                player_gravity = 0.05
        # Reset the timer after falling slower 
        if player_dashed_timer.value >= 6:
            player_momentum_x = 0
        if player_dashed_timer.value >= 15:
            player_dashed_timer.value = 0
            player_dashed_timer.go = False
        
        # Check for wall jumping 
        player_rect_next_frame = player.obj.rect.copy()
        player_rect_next_frame.x += movement[0]
        player_wall_jump_collider = pygame.Rect(player.x + int(player.w/2*direction),
                                                player.y + player.h/2-int(player.h/8),
                                                player.w,
                                                player.h/4)
        # engine.display_rect(display, player_wall_jump_collider, "orange", camera.scroll)
        hit_list_1 = engine.collision_test_inclusive(player_wall_jump_collider, current_level.colliders)
        hit_list_2 = engine.collision_test_inclusive(player_rect_next_frame, current_level.colliders)
        player_holding_a_wall = (len(hit_list_1) != 0) and (len(hit_list_2) != 0) and (player_air_timer > 3)
        opposite_direction = 1

        if player_holding_a_wall:
            player_wall_slide_timer += dt

            if movement[0] < 0:
                opposite_direction = +1
            elif movement[0] > 0:
                opposite_direction = -1

            if player_stamina > 0:
                if player_jumping is False and player_wall_sliding:
                    # Stamina decreases slowly
                    player_stamina -= dt
                    # Slow down the fall (sliding)
                    player_momentum_y = 0
                    player_gravity = 0.1
                elif player_jumping and player_wall_sliding and player_wall_slide_timer > 15:
                    # Can jump while sliding
                    movement[0] += int(5*opposite_direction*dt)
                    # Jumping consumes a lot of stamina
                    player_stamina -= 10
                    # Fixes the bug of jumping too high after stamina runs out
                    if player_stamina <= 0:
                        player_momentum_y = 0
        else:
            if not (3 <= player_dashed_timer.value < 15):
                player_gravity = 0.3
            player_wall_slide_timer = 0

        # Gravity
        player_momentum_y += player_gravity * dt
        if player_dashing == False and player_holding_down_key == False:
            if player_momentum_y > 4:
                player_momentum_y = 4
        movement[1] += player_momentum_y * dt

        # Player collisions with the level    
        player_direction = player.move(movement, current_level.colliders)

        if player_direction["bottom"]:
            player_stamina = 300
            player_available_dashes = 1
            player_momentum_y = 0
            player_air_timer = 0
        elif player_direction["top"]:
            player_momentum_y = 0
        else:
            player_air_timer += dt
            player_air_timer = round(player_air_timer, 2)
    
    # Player death
    if player.obj.rect.colliderect(current_level.death_plane):
        player_died_timer.go = True
        player_alive = False
        if player_died_timer.value > 50:
            player_alive = death.Respawn(player, current_level)
    player_died_timer = timer_main_loop(player_died_timer, dt)

    lvl.DisplayColliders(display, current_level, camera.scroll)
    if player_alive:
        player.display(display, camera.scroll)
    
    # Level Managing
    current_level = lvl.CheckPlayerHasFinished(player, camera, current_level, levels)

    # Input
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                player_moving_left = True
            if event.key == K_RIGHT or event.key == K_d:
                player_moving_right = True
            if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                if player_air_timer < 5 or (player_holding_a_wall and player_stamina > 0 and player_wall_sliding):
                    player_jumping = True
                    player_momentum_y = -6
            if event.key == K_UP or event.key == K_w:
                player_holding_up_key = True
            if event.key == K_DOWN or event.key == K_s:
                player_holding_down_key = True
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                player_wall_sliding = True
            if event.key == K_x:
                if player_available_dashes > 0:
                    player_dashing = True 

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_a:
                player_moving_left = False
            if event.key == K_RIGHT or event.key == K_d:
                player_moving_right = False
            if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                jump_key_timer = 0
                player_jumping = False
            if event.key == K_UP or event.key == K_w:
                player_holding_up_key = False
            if event.key == K_DOWN or event.key == K_s:
                player_holding_down_key = False
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                player_wall_sliding = False

    scaled_display = pygame.transform.scale(display, window_size, window)
    window.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
