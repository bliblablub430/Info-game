import pygame
import sys
import math

pygame.init()

# Hauptfenstergröße
MAIN_WIDTH, MAIN_HEIGHT = 800, 600
main_screen = pygame.display.set_mode((MAIN_WIDTH, MAIN_HEIGHT))
pygame.display.set_caption("Hauptspiel")

# Overlay-Fenster (für Stats)
OVERLAY_WIDTH, OVERLAY_HEIGHT = 250, 150
overlay_screen = pygame.Surface((OVERLAY_WIDTH, OVERLAY_HEIGHT))  # Surface für Overlay
# Position Overlay rechts neben Hauptfenster (simuliert, man kann es als Surface zeichnen)
OVERLAY_POS_X = MAIN_WIDTH - OVERLAY_WIDTH - 10
OVERLAY_POS_Y = 10

# Font
font = pygame.font.SysFont(None, 24)


player_pos = [character.x, character.y]
predator_pos = []

def draw_stats(surface, pos, speed, predator):
    """
    Zeichnet die Statistiken auf das Overlay-Surface.
    surface : Surface, auf das gezeichnet wird
    pos     : [x, y] Position des Spielers
    speed   : Geschwindigkeit des Spielers
    predator: [x, y] Position des Predators
    """
    surface.fill((30, 30, 30))  # dunkler Hintergrund
    pygame.draw.rect(surface, (200, 200, 200), (0, 0, OVERLAY_WIDTH, OVERLAY_HEIGHT), 2)  # Rahmen

    # Berechne Abstand zum Predator
    distance = math.hypot(predator[0]-pos[0], predator[1]-pos[1])

    # Stats-Text
    stats_texts = [
        f"Position: ({pos[0]}, {pos[1]})",
        f"Speed: {speed}",
        f"Predator dist: {int(distance)}"
    ]

    # Text auf Overlay zeichnen
    for i, t in enumerate(stats_texts):
        text_surf = font.render(t, True, (255, 255, 255))
        surface.blit(text_surf, (10, 10 + i*30))  # Abstand 30 Pixel pro Zeile

# -----------------------------
# Haupt-Loop
# -----------------------------
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Beispiel: Spieler bewegt sich nach rechts
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed

    # Hauptfenster zeichnen
    main_screen.fill((0, 0, 0))
    pygame.draw.circle(main_screen, (0, 255, 0), player_pos, 20)       # Spieler als Kreis
    pygame.draw.circle(main_screen, (255, 0, 0), predator_pos, 20)     # Predator als Kreis

    # Overlay zeichnen
    draw_stats(overlay_screen, player_pos, player_speed, predator_pos)
    main_screen.blit(overlay_screen, (OVERLAY_POS_X, OVERLAY_POS_Y))  # Overlay rechts oben

    pygame.display.flip()
    clock.tick(60)
