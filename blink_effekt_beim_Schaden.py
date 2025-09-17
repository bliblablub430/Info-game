import pygame

def blink_effect(surface, color=(200, 0, 0)):
    
    overlay = pygame.Surface(surface.get_size())  # Neue Fläche, so groß wie der Bildschirm
    overlay.fill(color)                           # Fläche färben
    surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)  # Fläche drüberlegen