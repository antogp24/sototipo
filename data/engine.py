import pygame, math, os
from pygame.locals import *

def AABB_inclusive(a, b):
    return (a.x + a.width >= b.x  and 
            a.x <= b.x + b.width  and
            a.y + a.height >= b.y and
            a.y <= b.y + b.height    )

# 2d collisions test
def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

def collision_test_inclusive(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if AABB_inclusive(obj, object_1):
            collision_list.append(obj)
    return collision_list

# 2d physics object
class physics_obj(object):
   
    def __init__(self,x,y,w,h):
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y
       
    def move(self,movement,platforms):
        self.x += movement[0]
        self.rect.x = int(self.x)
        block_hit_list = collision_test(self.rect,platforms)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        for block in block_hit_list:
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
            self.x = self.rect.x
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision_test(self.rect,platforms)
        for block in block_hit_list:
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
            self.change_y = 0
            self.y = self.rect.y
        return collision_types


class entity(object):
   
    def __init__(self,x,y,w,h,color,e_type): # x, y, size_x, size_y, type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.obj = physics_obj(x,y,w,h)
        self.color = color
 
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y
 
    def move(self,momentum,platforms):
        collisions = self.obj.move(momentum,platforms)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions
 
    def rect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)

    def display(self,surface,scroll):
        rect = self.rect()
        rect.x -= scroll[0]
        rect.y -= scroll[1]
        pygame.draw.rect(surface,self.color,rect,1)
 
def display_rect(surface, rect, color, scroll):
    rect = rect.copy()
    rect.x -= scroll[0]
    rect.y -= scroll[1]
    pygame.draw.rect(surface,color,rect,1)
