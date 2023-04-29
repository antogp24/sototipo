import pygame

def GetCollisionMap(tmx, id):
    colliders = []
    layer = tmx.get_layer_by_name(f'level_{id}')

    for obj in layer:
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        colliders.append(rect)
    return colliders

def GetFinishLineLV(tmx, id):
    if id == None:
        return None

    layer = tmx.get_layer_by_name(f'level_{id}_end')
    rect = pygame.Rect(0, 0, 0, 0)

    for obj in layer:
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    return rect

def GetDeathPlaneLV(tmx, id):
    layer = tmx.get_layer_by_name(f'level_{id}_death_plane')
    rect = pygame.Rect(0, 0, 0, 0)

    for obj in layer:
        rect = pygame.Rect(obj.x-500, obj.y, obj.width+1000, obj.height+100)
    return rect

def DisplayColliders(display, level, scroll):
    for collider in level.colliders:
        rect = collider.copy()
        rect.x -= scroll[0]
        rect.y -= scroll[1]
        pygame.draw.rect(display, "white", rect, 1)
    if level.end != None:
        end = level.end.copy()
        end.x -= scroll[0]
        end.y -= scroll[1]
        pygame.draw.rect(display, "magenta", end, 1)

def CheckPlayerHasFinished(player, camera, current_level, levels):
    if current_level.end != None:
        if player.obj.rect.colliderect(current_level.end):
            next_level_id = f'{current_level.id+1}'
            current_level = levels[next_level_id]
            player.set_pos(current_level.start_pos[0], current_level.start_pos[1])
            camera.reset()
    return current_level


class Level:
    def __init__(self, id, colliders, end, death_plane, start_pos, bg):
        self.id = id
        self.colliders = colliders
        self.end = end
        self.death_plane = death_plane
        self.start_pos = start_pos
        self.background_color = bg

def load_all_levels(tmx):
    lvls = {}

    bg_color_1 = (10, 10, 25)
    bg_color_2 = (250, 200, 100)

    lvls['1'] = Level(
        1,
        GetCollisionMap(tmx, 1),
        GetFinishLineLV(tmx, 1),
        GetDeathPlaneLV(tmx, 1),
        (480, 0),
        bg_color_1)
    
    lvls['2'] = Level(
        2,
        GetCollisionMap(tmx, 2),
        GetFinishLineLV(tmx, None),
        GetDeathPlaneLV(tmx, 2),
        (125, 0),
        bg_color_2)

    return lvls
