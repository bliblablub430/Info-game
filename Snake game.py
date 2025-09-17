import pygame
import sys
import random

# Pygame starten
pygame.init()

# Fenster erstellen
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Farben
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Clock und Schrift
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Snake und Essen starten
snake = [(100, 100), (80, 100), (60, 100)]  # Startposition des Schlangenkörpers
direction = (CELL_SIZE, 0)                  # Startbewegung nach rechts
food = (random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE))
score = 0

def draw_snake():
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
def verloren():
    screen.fill(GREEN)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    # 10 Sekunden warten, während Fenster offen bleibt
    start_time = time.time()
    if time.time() - start_time < 10:
        pygame.quit()
        sys.exit()
# Hauptspiel-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            verloren()
        elif event.type == pygame.KEYDOWN:
            # Richtung ändern, aber nicht in die entgegengesetzte
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    # Neue Position des Kopfes berechnen
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Kollision mit Essen
    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, CELL_SIZE),
                random.randrange(0, HEIGHT, CELL_SIZE))
    else:
        snake.pop()

    # Kollision mit Wand oder sich selbst
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake[1:]
    ):
        verloren()
        

    # Zeichnen
    screen.fill(BLACK)
    draw_snake()
    draw_food()

    # Punktestand anzeigen
    score_text = font.render(f"Punkte: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)  # 10 FPS