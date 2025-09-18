import pygame # von Chatgpt gezeichnet

def draw_lives(surface, lives, x=1400, y=220, max_lives=3, size=16, trianglefactor=1.44, gap=8):   # Herzen als rote Kreise + Dreieck
  
    for i in range(max_lives):
        cx = x + i * (size*2 + gap)
        if i < lives:
            color = (200, 50, 60)
        else:
            color = (105,105,105)  
         # zwei Kreise
        pygame.draw.circle(surface, color, (cx + size//2, y + size//2), size//2)
        pygame.draw.circle(surface, color, (cx + size,     y + size//2), size//2)
        # kleines Dreieck unten
        points = [(cx-4.5 + size*trianglefactor//4, y-0.2 + size*trianglefactor//2),
                  (cx-4.5 + size*trianglefactor + size*trianglefactor//4, y-0.2 + size*trianglefactor//2),
                  (cx-4.5 + size*trianglefactor//2 + size*trianglefactor//4, y-0.2 + size*trianglefactor)]
        pygame.draw.polygon(surface, color, points)
    return lives

def lose_life(lives): # von Thông
    lives -= 1
    return lives

def gain_life(lives, max_lives=3): # von Thông
    return min(lives + 1, max_lives)