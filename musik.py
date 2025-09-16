import pygame 

pygame.mixer.init()

def play_music(path, loop=True, volume=0.5):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
    except pygame.error as e:
        print(f"Fehler beim Laden der Musik: {e}")

def stop_music():
    pygame.mixer.music.stop()