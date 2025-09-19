import pygame
import Characters
import ostblock
#list of everything except the character (for moving everything around the player)
almosteverything = []

#wall collition plus map movement around the player
def wallinteraction(x, y, dx, dy, almosteverything, sprint_unlocked):
    moving_everythingx(dx, almosteverything)
    for wall in ostblock.walls:
        if Characters.character.rect.colliderect(wall):
            moving_everythingx(-dx, almosteverything)
    moving_everythingy(dy, almosteverything)
    for wall in ostblock.walls:
        if Characters.character.rect.colliderect(wall):
            moving_everythingy(-dy, almosteverything)
    x, y, dx, dy = Characters.movement(x, y, Characters.speed, sprint_unlocked)
    return x, y, dx, dy
# movin eferything around the player in x direction
def moving_everythingx(dx, almosteverything):
     for objects in almosteverything:
        if isinstance(objects, pygame.sprite.Sprite):
            objects.rect.x += dx
        else:
            objects.x += dx
# movin eferything around the player in y direction
def moving_everythingy(dy, almosteverything):
     for objects in almosteverything:
        if isinstance(objects, pygame.sprite.Sprite):
            objects.rect.y += dy
        else:
            objects.y += dy
# adds objects to the list of everything except the player
def add_to_almosteverything(object, almosteverything):
    if type(object) == list:
        for value in object:
            add_to_almosteverything(value, almosteverything)
    else:
         almosteverything.append(object)
    return almosteverything