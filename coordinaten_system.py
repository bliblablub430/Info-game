import pygame

surface = pygame.display.set_mode((1920, 1080))

def draw_coords(surface, rect_to_track, font_size=24, padding=5):
    """
    Zeichnet ein sauberes Koordinaten-HUD unten links auf den Bildschirm.
    """
    # 1. Text vorbereiten
    font = pygame.font.Font(None, font_size)
    text_string = f"X: {int(rect_to_track.x)} | Y: {int(rect_to_track.y)}"
    text_surface = font.render(text_string, True, (255, 255, 255))
    text_rect = text_surface.get_rect()

    # 2. Hintergrund-Rechteck erstellen
    bg_width = text_rect.width + padding * 2
    bg_height = text_rect.height + padding * 2
    bg_rect = pygame.Rect(0, 0, bg_width, bg_height) # Zuerst bei (0,0) erstellen

    # 3. Hintergrund an der unteren linken Ecke des Bildschirms ausrichten
    bg_rect.bottomleft = (220, 1000)

    # 4. Text im Hintergrund zentrieren
    text_rect.center = bg_rect.center

    # 5. Alles zeichnen
    pygame.draw.rect(surface, (20, 20, 20), bg_rect) # Hintergrund
    surface.blit(text_surface, text_rect)           # Text
