import Characters
import ostblock

almosteverything = []


def wallinteraction(x, y, dx, dy, almosteverything):
    moving_everythingx(dx, almosteverything)
    for wall in ostblock.walls:
        if Characters.character.colliderect(wall):
                moving_everythingx(-dx, almosteverything)
    moving_everythingy(dy, almosteverything)
    for wall in ostblock.walls:
        if Characters.character.colliderect(wall):
            moving_everythingy(-dy, almosteverything)
    x, y, dx, dy = Characters.movement(x, y, Characters.speed)
    return x, y, dx, dy

def moving_everythingx(dx, almosteverything):
     for objects in almosteverything:
          objects.x += dx

def moving_everythingy(dy, almosteverything):
     for objects in almosteverything:
          objects.y += dy

def add_to_almosteverything(object, almosteverything):
    if type(object) == list:
        for value in object:
            add_to_almosteverything(value, almosteverything)
    else:
         almosteverything.append(object)
    return almosteverything