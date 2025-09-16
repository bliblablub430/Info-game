import pygame 

pygame.mixer.init()

def play_music(path, loop=True, volume=0.5): #loop = True (Enlosschleife) und loop = False ( einmal abspielen)
    try:
        pygame.mixer.music.load(path) # Lädt die Musikdatei
        pygame.mixer.music.set_volume(volume) # Setzt die Lautstärke
        pygame.mixer.music.play(-1 if loop else 0)  # Startet die Wiedergabe (-1 = Endlosschleife, 0 = einmal)
    except pygame.error as e:
        print(f"Fehler beim Laden der Musik: {e}")  # Gibt eine Fehlermeldung aus, falls etwas schiefgeht

def stop_music():
    pygame.mixer.music.stop()  # Stoppt die aktuell laufende Musik