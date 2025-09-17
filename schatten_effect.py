import pygame

def draw_shadow(surface, rect, size=20):
    # Erstelle eine neue transparente Oberfläche für den Schatten
    shadow = pygame.Surface((size, size//2), pygame.SRCALPHA)
    # Zeichne eine halbtransparente schwarze Ellipse auf die Schatten-Oberfläche
    pygame.draw.ellipse(shadow, (0,0,0,80), shadow.get_rect())
    # Berechne die Position, an der der Schatten unter das Rechteck platziert werden soll
    pos = (rect.midbottom[0] - size // 2, rect.midbottom[1])
    # Zeichne (blitte) den Schatten auf die Zieloberfläche
    surface.blit(shadow, pos)

    # Schatten zeichenen(unter der Figur) Bsp: line x   draw_shadow(screen, player, size=60)
