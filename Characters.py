import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")

clock = pygame.time.Clock()
x, y = 700, 500
speed = 5 

running = True
while running:
    dx = 0
    dy = 0
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    def movement():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        if dx or dy != 0:
            vectorlen = (dx**2 + dy**2)**0.5
            dx = dx/vectorlen
            dy = dy/vectorlen 

        if keys[pygame.K_d]:
            x += (dx*speed)
        if keys[pygame.K_a]:
            x += (dx*speed)
        if keys[pygame.K_w]:
            y += (dy*speed)
        if keys[pygame.K_s]:
            y += (dy*speed)       

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 50))
        pygame.display.update()
        clock.tick(60)