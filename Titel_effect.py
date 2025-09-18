import pygame
import musik

def show_game_title_fade(screen, title="Frau_Weidtmann_Hunter69", duration=7):
    font = pygame.font.Font(None, 72)
    text = font.render(title, True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    clock = pygame.time.Clock()
    total_frames = duration * 60
    musik.play_music("assets/sfx/intro_theme.mp3", loop=False, volume=0.5)

    for frame in range(total_frames):
        alpha = 255
        if frame < 60:  # 1 Sek Fade-In
            alpha = int(255 * (frame/60))
        elif frame > total_frames - 60:  # 1 Sek Fade-Out
            alpha = int(255 * ((total_frames-frame)/60))

        screen.fill((30,30,40))
        text.set_alpha(alpha)
        screen.blit(text, rect)
        pygame.display.flip()
        clock.tick(60)
