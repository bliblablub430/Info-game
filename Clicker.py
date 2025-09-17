import pygame
import sys

pygame.init()
# Fenstergröße und Farben
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker Game")

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# Startwert für Punkte
score = 0

# Button-Eigenschaften
button_rect = pygame.Rect(150, 120, 100, 60)

def draw_game(score):
    screen.fill(WHITE)
    # Zeigt Punkte an
    score_text = font.render(f"Punkte: {score}", True, BLACK)
    screen.blit(score_text, (120, 40))
    # Button zeichnen
    pygame.draw.rect(screen, GREEN, button_rect)
    btn_text = small_font.render("Klick mich!", True, BLACK)
    # Button-Text zentrieren
    text_rect = btn_text.get_rect(center=button_rect.center)
    screen.blit(btn_text, text_rect)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Wenn Button geklickt wird, Punkte erhöhen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                score += 1

    draw_game(score)
    pygame.display.flip()
    