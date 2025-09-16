import pygame
import sys
import random
import math

# -----------------------------
# Pygame initialisieren
# -----------------------------
pygame.init()

# Fenstergröße und Farben
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)

# Spielfenster erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette")

# Schrift und Uhr
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Zahlen auf dem Roulette-Rad (0 bis 36)
numbers = list(range(37))

# Position und Größe des Roulette-Rades
center = (WIDTH // 2, HEIGHT // 2)
radius = 200

# Spielzustände
bet_number = None       # Zahl, auf die gesetzt wurde
result_number = None    # Zahl, die herauskommt
spinning = False
angle = 0
speed = 0

# ---------------------------------------------------
# Funktion: Roulette-Rad zeichnen
# ---------------------------------------------------
def draw_roulette():
    # Grüner Außenkreis
    pygame.draw.circle(screen, GREEN, center, radius + 10)
    # Schwarzer Innenkreis
    pygame.draw.circle(screen, BLACK, center, radius)

    # Alle Zahlen am Radrand
    for i, n in enumerate(numbers):
        seg_angle = (360 / len(numbers)) * i + angle
        rad = math.radians(seg_angle)
        x = center[0] + math.cos(rad) * (radius - 20)
        y = center[1] + math.sin(rad) * (radius - 20)
        text = font.render(str(n), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

# ---------------------------------------------------
# Funktion: Drehen starten
# ---------------------------------------------------
def spin():
    global spinning, speed, result_number
    spinning = True
    speed = random.uniform(15, 20)  # zufällige Startgeschwindigkeit
    result_number = None

# ---------------------------------------------------
# Funktion: Stoppen & Gewinner ermitteln
# ---------------------------------------------------
def stop_and_choose():
    global result_number
    index = int((-angle % 360) / (360 / len(numbers)))
    result_number = numbers[index]

# ---------------------------------------------------
# Hauptspiel-Loop
# ---------------------------------------------------
while True:
    # Events abfangen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # Zifferntaste für Wette
            if event.unicode.isdigit():
                bet_number = int(event.unicode)

            # SPACE startet Drehung
            elif event.key == pygame.K_SPACE and not spinning:
                spin()

    # Wenn Rad sich dreht
    if spinning:
        angle += speed
        speed *= 0.97  # Bremse
        if speed < 0.3:
            spinning = False
            stop_and_choose()

    # ---------------------------------------------------
    # Zeichnen
    # ---------------------------------------------------
    screen.fill((30, 30, 30))
    draw_roulette()

    # Aktuelle Wette anzeigen
    if bet_number is not None:
        bet_text = font.render(f"Wette: {bet_number}", True, WHITE)
        screen.blit(bet_text, (20, 20))

    # Ergebnis anzeigen
    if result_number is not None:
        result_text = font.render(f"Ergebnis: {result_number}", True, WHITE)
        screen.blit(result_text, (20, 60))
        if bet_number == result_number:
            win_text = font.render("GEWONNEN!", True, (255, 0, 0))
            screen.blit(win_text, (20, 100))
        else:
            lose_text = font.render("VERLOREN!", True, (255, 0, 0))
            screen.blit(lose_text, (20, 100))

    # Hinweis
    instr_text = font.render("Ziffer (0–9) zum Setzen, SPACE zum Drehen", True, WHITE)
    screen.blit(instr_text, (20, HEIGHT - 40))

    # Anzeige aktualisieren
    pygame.display.flip()
    clock.tick(60)
