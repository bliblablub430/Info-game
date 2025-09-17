import pygame
import sys

pygame.init()

# Fenstergröße festlegen
WIDTH, HEIGHT = 200, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Fenster mit Breite und Höhe erstellen
pygame.display.set_caption("Pixelwährung")        # Titel des Fensters setzen

# Variable für die Pixel-Währung
pixel = 100

# Font-Objekt erstellen (Schriftart, Größe)
font = pygame.font.SysFont(None, 36)

# Funktion zum Zeichnen des Pixelfelds
def draw_pixelfeld(pixel):
    # Weißes Rechteck zeichnen (Position x=10, y=10, Breite=180, Höhe=80)
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, 180, 80))
    # Text rendern
    text = font.render(f"Pixel: {pixel}", True, (0, 0, 0))
    # Text auf das Rechteck zeichnen (Position x=30, y=40)
    
    # Rechte obere Ecke: x = Fensterbreite – Textbreite – Abstand, y = Abstand von oben
    x = 1920-text.get_width()-20  # 20 Pixel Abstand von rechts
    y = 1080-text.get_height()-20                            # 20 Pixel Abstand von oben

    # Text auf Bildschirm zeichnen
    screen.blit(text, (x, y))

# Haupt-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))# Hintergrund schwarz
    draw_pixelfeld(pixel)# Pixelfeld zeichnen
    pygame.display.flip()# Fenster aktualisieren