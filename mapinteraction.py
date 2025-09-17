import Characters
import ostblock


def wallinteraction(x, y, dx, dy):
    Characters.character.x += dx
    for wall in ostblock.walls:
        if Characters.character.colliderect(wall):
                Characters.character.x -= dx
    Characters.character.y += dy
    for wall in ostblock.walls:
        if Characters.character.colliderect(wall):
            Characters.character.y -= dy
    x, y, dx, dy = Characters.movement(x, y, Characters.speed)
    return x, y, dx, dy