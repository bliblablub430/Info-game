import pygame
import sys
import time
WIDTH,HEIGHT=100,50
GREEN=(0,200, 0)
x, y= 0,0
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game over")
clock=pygame.time.Clock()
def verloren():
    screen.fill(GREEN)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    print("Game Over! Final Score:")
    # 10 Sekunden warten, während Fenster offen bleibt
    start_time = time.time()
    while time.time() - start_time < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(30)
    pygame.quit()
    sys.exit()

verloren()