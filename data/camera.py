from .common import *

def moveCamera(camera, dt):
    scroll_x_offset = -camera.true_scroll[0] - display_size[0]/2
    scroll_y_offset = -camera.true_scroll[1] - display_size[1]/2

    # The actual scroll uses floats to be smooth
    camera.true_scroll[0] += (camera.target[0] + scroll_x_offset) / camera.scroll_lag * dt
    camera.true_scroll[1] += (camera.target[1] + scroll_y_offset) / camera.scroll_lag * dt

    if camera.screen_shake > 0:
        camera.true_scroll[0] += random.randint(-40, 40)/10
        camera.true_scroll[1] += random.randint(-40, 40)/10
        camera.screen_shake -= 1

    # The one used for rendering is rounded to avoid artifacts
    camera.scroll[0] = int(camera.true_scroll[0])
    camera.scroll[1] = int(camera.true_scroll[1])

    return camera