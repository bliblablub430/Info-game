import pygame
import time

# Pygame initialisieren
pygame.init()

# Fenster erstellen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zahlraten-Spiel")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)

# Schriftart
font = pygame.font.SysFont(None, 48)

# Funktion für Abstand zweier Zahlen
def unterschied(a, b):
    return abs(a - b)

# Spielvariablen
pixel = 100
zeit = 10

zahlen_liste = list(range(1, 11))  # Zahlen von 1 bis 10
aktuelle_index = 0
wechselzahl = zahlen_liste[aktuelle_index]

letzter_wechsel = time.time()
user_input = ""
clock = pygame.time.Clock()

start_time = time.time()
game_over = False
ergebnis_text = ""

# Spielschleife
running = True
while running:
    screen.fill(BLACK)

    # --- Eingaben abfragen ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.unicode.isdigit():
                user_input += event.unicode
            elif event.key == pygame.K_RETURN and user_input != "":
                zahl = int(user_input)

                # Bereich prüfen
                if zahl < 1 or zahl > 10:
                    ergebnis_text = "Zahl nicht im Bereich!"
                    pixel -= 30
                else:
                    # Auswertung
                    if zahl == wechselzahl:
                        pixel += 100
                        ergebnis_text = "Reaktionszeit einer Gazelle"
                    elif 0 < unterschied(zahl, wechselzahl) < 3:
                        pixel += 10
                        ergebnis_text = "Reaktionszeit von Frau Lehmann"
                    elif 3 < unterschied(zahl, wechselzahl) < 6:
                        pixel -= 1
                        ergebnis_text = "Reaktionszeit von Thong Cena"
                    elif 6 <= unterschied(zahl, wechselzahl) <= 10:
                        pixel -= 30
                        ergebnis_text = "Reaktionszeit von einem Faultier"

                game_over = True

    # --- Zahl wechseln (alle 0.2 Sekunden) ---
    if not game_over and time.time() - letzter_wechsel > 0.2:
        aktuelle_index = (aktuelle_index + 1) % len(zahlen_liste)
        wechselzahl = zahlen_liste[aktuelle_index]
        letzter_wechsel = time.time()

    # --- Countdown ---
    if not game_over:
        vergangen = int(time.time() - start_time)
        verbleibend = max(0, zeit - vergangen)
    else:
        verbleibend = 0

    if verbleibend == 0 and not game_over:
        ergebnis_text = "Zeit abgelaufen!"
        pixel -= 50
        game_over = True

    # --- Anzeige ---
    timer_surface = font.render(f"Zeit: {verbleibend}", True, WHITE)
    screen.blit(timer_surface, (20, 20))

    pixel_surface = font.render(f"Pixel: {pixel}", True, GREEN)
    screen.blit(pixel_surface, (20, 80))

    eingabe_surface = font.render(f"Eingabe: {user_input}", True, WHITE)
    screen.blit(eingabe_surface, (20, 150))

    if not game_over:
        wechsel_surface = font.render(f"Zahl: {wechselzahl}", True, RED)
        screen.blit(wechsel_surface, (400, 150))

    if ergebnis_text:
        ergebnis_surface = font.render(ergebnis_text, True, RED)
        screen.blit(ergebnis_surface, (20, 220))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()