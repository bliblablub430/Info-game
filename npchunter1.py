import pygame
import ostblock
import mapinteraction

pygame.init()
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

# Player variables
x, y = 960, 540
h, l = 50, 50
speed = 10
character = pygame.Rect(x, y, h, l)

# alter NPC, der derzeit im Kreis läuft (beibehalten)
xn, yn = 800, 600
hn, ln = 50, 50
steps = 0
npcspeed = 5
npc = pygame.Rect(xn, yn, hn, ln)

# neuer Verfolger-NPC (gelb)
npchunter2speed = 7
npchunter2_rect = pygame.Rect(100, 100, 50, 50)

pixles = []

def movement(x, y, speed):  # actual movement happens in mapinteraction.wallinteraction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        speedc = speed * 2
    else:
        speedc = speed
    dx, dy = get_movement_vector()
    x += dx * speedc
    character.x = x   # direkt zuweisen (kein __name__-Check nötig)
    y += dy * speedc
    character.y = y
    return x, y, (dx * speedc), (dy * speedc)

def get_movement_vector():
    dx, dy = 0, 0  # Start with no movement
    keys = pygame.key.get_pressed()

    # Konventionelle Richtungstasten: d = rechts (+x), a = links (-x), w = oben (-y), s = unten (+y)
    if keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_s]:
        dy += 1

    # Normalize the vector (so diagonal movement isn't faster)
    if dx != 0 or dy != 0:
        vector_len = (dx ** 2 + dy ** 2) ** 0.5
        dx = dx / vector_len
        dy = dy / vector_len

    return dx, dy  # Return the calculated direction

def npcmovement(npc, steps, npcspeed):
    # NPC algorithm (ursprünglicher Kreis)
    if steps < 20:
        npc.x += npcspeed
    elif steps < 40:
        npc.y += npcspeed
    elif steps < 60:
        npc.x -= npcspeed
    elif steps < 80:
        npc.y -= npcspeed
    steps += 1
    if steps >= 80:
        steps = 0
    return steps

def npchunter2(npchunter2_rect, character, npchunter2speed):
    # NPC-Algorithmus: Verfolge den Character (Verfolger als gelbes Rect)
    dx = character.x - npchunter2_rect.x
    dy = character.y - npchunter2_rect.y

    dist = (dx ** 2 + dy ** 2) ** 0.5

    if dist != 0:  # Schutz gegen Division durch 0
        dx /= dist  # Normiere auf Länge 1
        dy /= dist
        npchunter2_rect.x += dx * npchunter2speed
        npchunter2_rect.y += dy * npchunter2speed
    return npchunter2_rect.x, npchunter2_rect.y

def drawing(screen, character, npc, npchunter2_rect, pixles):
    # check for drawing a pixel
    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        pixles.append(draw(character.x, character.y))
    # Drawing everything
    ostblock.walldraw(screen)  # Draw wall
    pygame.draw.rect(screen, (0, 0, 255), character)  # Draw player (blau)
    pygame.draw.rect(screen, (255, 0, 0), npc)        # Alter NPC (rot)
    pygame.draw.rect(screen, (255, 255, 0), npchunter2_rect)  # Verfolger-NPC (gelb)
    for p in pixles:
        pygame.draw.rect(screen, (0, 255, 0), (p))  # Draw pixles (grün)

def draw(x, y):
    pixle = pygame.Rect(x, y, 50, 50)
    mapinteraction.add_to_almosteverything(pixle, mapinteraction.almosteverything)
    return pixle

if __name__ == "__main__":
    screen = pygame.display.set_mode((1920, 1080))

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # proper quit check
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Spielerbewegung
        x, y, dx, dy = movement(x, y, speed)

        # alter NPC (Patrouille im Kreis) updaten
        steps = npcmovement(npc, steps, npcspeed)

        # neuer Verfolger-NPC updaten (verfolgt 'character')
        npchunter2(npchunter2_rect, character, npchunter2speed)

        screen.fill((0, 0, 0))  # Clear screen
        drawing(screen, character, npc, npchunter2_rect, pixles)
        pygame.display.update()  # Update the display
        clock.tick(60)

    pygame.quit()  # Quit pygame properly
