import pygame
import random
import sys
import textwrap

pygame.init()

# Fenster
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Baum mit Codeanzeige")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)

GROUND = (45, 110, 45)
WHITE = (240, 240, 240)

# --------------------------
# Der Code, der angezeigt wird
# --------------------------
def draw_tree(surface, x, y, scale=1.0):
    trunk_color = (101, 67, 33)
    leaf_color = (30, 160, 60)
    pygame.draw.circle(surface, trunk_color, (int(x), int(y)), int(6*scale))
    for i in range(10):
        cx = x + random.randint(-20, 20)*scale
        cy = y + random.randint(-20, 20)*scale
        r = random.randint(10, 20)*scale
        pygame.draw.circle(surface, leaf_color, (int(cx), int(cy)), int(r))


# Funktion zum Baum zeichnen
def draw_tree(surface, x, y, scale=1.0):
    trunk_color = (101, 67, 33)
    leaf_color = (30, 160, 60)
    pygame.draw.circle(surface, trunk_color, (int(x), int(y)), int(6*scale))
    for i in range(10):
        cx = x + random.randint(-20, 20)*scale
        cy = y + random.randint(-20, 20)*scale
        r = random.randint(10, 20)*scale
        pygame.draw.circle(surface, leaf_color, (int(cx), int(cy)), int(r))

# Liste aller Bäume
trees = []

running = True
while running:
    screen.fill(GROUND)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            trees.append((mx, my, random.uniform(0.7, 1.3)))

    # Bäume zeichnen
    for (x, y, s) in trees:
        draw_tree(screen, x, y, s)

    # Code rechts anzeigen
    wrapped_lines = textwrap.wrap(source_code, width=60, replace_whitespace=False)
    for i, line in enumerate(wrapped_lines):
        txt = font.render(line, True, WHITE)
        screen.blit(txt, (600, 20 + i*18))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()