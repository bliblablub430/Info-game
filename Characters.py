import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")

clock = pygame.time.Clock()
x, y = 700, 500
speed = 5 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_s]:
        y += speed

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 50))
    pygame.display.update()
    clock.tick(60)