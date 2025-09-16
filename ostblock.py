import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
# Map-Bild laden
map_img = pygame.image.load("Lerbermatt_Ostblock_2.png").convert()
width, height = map_img.get_size()
TILESIZE = 1
# Liste für Wände
walls = []

# Position der Map
offset_x = (800 - width * TILESIZE) // 2
offset_y = (600 - height * TILESIZE) // 2
# Pixel einlesen und Wände/Boden erstellen
for y in range(height):
    for x in range(width):
        color = map_img.get_at((x, y))[:3]  # RGB
        rect = pygame.Rect(x * TILESIZE + offset_x, y * TILESIZE + offset_y, TILESIZE, TILESIZE)

        if color == (0, 0, 0):  # Schwarz = Wand
            walls.append(rect)
        elif color == (255, 255, 255):  # Weiß = Boden
            pass  # Boden, nichts zu tun


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Hintergrundfarbe
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()