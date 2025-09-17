import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()
# Player variables
x, y = 700, 500
h, l = 50, 50
speed = 5
character = pygame.Rect(x, y, h, l)

xn, yn = 800, 600
hn, ln = 50, 50
steps = 0
npcspeed = 5
npc = pygame.Rect(xn, yn, hn, ln)

pixles = []
player_pixel = 0
slow_until = 0  # Zeitstempel, bis wann der Spieler verlangsamt ist


def movement(x, y, speed):
    global player_pixel, slow_until
    # Prüfe Kollision mit NPC
    if npc.colliderect(character):
        # Nur beim ersten Kontakt bestrafen
        if slow_until == 0:
            player_pixel -= 100
            slow_until = time.time() + 2  # 2 Sekunden verlangsamen
        return x, y  # Charakter bleibt stehen
    else:
        # Geschwindigkeit ggf. reduzieren
        current_speed = speed
        if slow_until > time.time():
            current_speed = speed * 0.25
        else:
            slow_until = 0  # Reset, falls Zeit abgelaufen

        dx, dy = get_movement_vector()
        x += dx * current_speed
        character.x = x
        y += dy * current_speed
        character.y = y
        return x, y


def get_movement_vector():
    dx, dy = 0, 0  # Start with no movement
    keys = pygame.key.get_pressed()
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
        vector_len = (dx**2 + dy**2)**0.5
        dx = dx / vector_len
        dy = dy / vector_len
    return dx, dy # Return the calculated direction

def npcmovement(npc, steps, npcspeed):
    #NPC algorythm
    if steps < 20:
        npc.x += npcspeed
    elif steps >= 20 and steps < 40:
        npc.y += npcspeed
    elif steps >= 40 and steps < 60:
        npc.x -= npcspeed
    elif steps >= 60 and steps < 80:
        npc.y -= npcspeed
    elif steps == 80:
        steps = 0
    steps += 1
    return steps
def drawing(screen, character, npc, pixles):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        pixles.append(draw(x, y))
    screen.fill((0, 0, 0)) # Clear screen
    pygame.draw.rect(screen, (0, 0, 255), character) # Draw player
    pygame.draw.rect(screen, (255, 0, 0), npc) #Draw npc
    for p in pixles:
        pygame.draw.rect(screen, (0, 255, 0), (p))
    # Pixelstand anzeigen
    font = pygame.font.SysFont(None, 48)
    pixel_text = font.render(f"Pixel: {player_pixel}", True, (255, 255, 255))
    screen.blit(pixel_text, (50, 50))
    pygame.display.update() # Update the display

def draw(x,y):
    return pygame.Rect(x, y, 50, 50)
if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        x, y = movement(x, y, speed)
        steps = npcmovement(npc, steps, npcspeed)
        drawing(screen, character, npc, pixles)
        clock.tick(60)

    pygame.quit()