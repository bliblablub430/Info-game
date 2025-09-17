import pygame

def draw_lives(surface, x, y, lives, max_lives=3, size=16, gap=8):   # Herzen als rote Kreise + Dreieck
  
    for i in range(max_lives):
        cx = x + i * (size*2 + gap)
        color = (200, 50, 60) if i < lives else (80, 80, 80)  
         # zwei Kreise
        pygame.draw.circle(surface, color, (cx + size//2, y + size//2), size//2)
        pygame.draw.circle(surface, color, (cx + size,     y + size//2), size//2)
        # kleines Dreieck unten
        points = [(cx + size//4, y + size//2),
                  (cx + size + size//4, y + size//2),
                  (cx + size//2 + size//4, y + size)]
        pygame.draw.polygon(surface, color, points)

def lose_life(lives):
    return max(lives - 1, 0)

def gain_life(lives, max_lives=3):
    return min(lives + 1, max_lives)