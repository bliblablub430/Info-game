import pygame
import Gambling
import Characters

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

running = True
game_state = "normal" # Die EINZIGE game_state Variable

while running:
    
    # Events *einmal* pro Frame holen
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # Events an die Funktionen übergeben, die sie brauchen
        game_state = Gambling.escaperoulette(game_state, event)

    # RUFE die rouletteloop auf und fange den neuen State auf
    # Übergib das Characters-Objekt, damit die Funktion es bewegen kann
    game_state = Gambling.rouletteloop(game_state)

    # --- ZEICHNEN ---
    # Dieser Block wird jetzt erreicht!
    screen.fill((0, 0, 0)) # Hintergrund
    
    # Dieser Print wird jetzt funktionieren
    print(f"Zeichne Trigger-Zone bei: {Gambling.roulette_trigger_zone}") 
    
    # Zeichne die Trigger-Zone (Rot)
    pygame.draw.rect(screen, (255, 0, 0), Gambling.roulette_trigger_zone)
    
    # Zeichne den Spieler (Blau)
    pygame.draw.rect(screen, (0, 0, 255), (Characters.x, Characters.y, Characters.h, Characters.l)) 
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()