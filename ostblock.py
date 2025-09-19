# Mit AI
import pygame
import sprites
#Mit AI
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
# Map-Bild laden
map_img = pygame.image.load("Lerbermatt_premium.png").convert()
width, height = map_img.get_size()
TILESIZE = 15
# Liste für Wände
walls = []



# Position der Map
#Mit Ai
offset_x = (800 - width * TILESIZE) // 2 
offset_y = (600 - height * TILESIZE) // 2
# Pixel einlesen und Wände/Boden erstellen
def wallcreation():
    for y in range(height):
        for x in range(width):
            color = map_img.get_at((x, y))[:3]  # RGB
            rect = pygame.Rect(x * TILESIZE + offset_x, y * TILESIZE + offset_y, TILESIZE, TILESIZE)
                        # Zerlege die Farbe in ihre Rot-, Grün- und Blau-Werte
            r, g, b = color
            
            # Lege einen Schwellenwert fest. Alle Farben, deren RGB-Werte
            # ALLE unter diesem Wert liegen, gelten als "fast schwarz".     # AI generated
            # Ein Wert um 10 ist gut für kleine Abstufungen.
            threshold = 10 
            
            # Prüfe, ob die Farbe dunkel genug ist, um als Wand zu gelten
            if r < threshold and g < threshold and b < threshold:
                walls.append(rect)
    return walls
#mit AI
# Wände zeichnen
def walldraw(screen):
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall)
#Hintergrundbild anpassung an Wände
#Human made
map_imgup = pygame.transform.scale(map_img, (TILESIZE*width, TILESIZE*height))
map_imgsp = sprites.Sprites("Lerbermatt_3Version.png", pygame.Rect(offset_x, offset_y, width*TILESIZE, height*TILESIZE))
#Mit AI
def drawmap(map_imgup):
    screen.blit(map_imgup, map_imgsp.rect)

if __name__ == "__main__":

    wallcreation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        walldraw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()