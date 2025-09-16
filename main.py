import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")

clock = pygame.time.Clock()

running = True
while running:
    dx = 0
    dy = 0
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.update()
    clock.tick(60)