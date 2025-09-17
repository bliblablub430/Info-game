import pygame
import Gambling
import Characters

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

running = True
game_state = "normal" # Die EINZIGE game_state Variable
current_state = "waiting_for_bet" # für Roulette

while running:
    
    # Events *einmal* pro Frame holen
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # Events an die Funktionen übergeben, die sie brauchen
        game_state = Gambling.escaperoulette(game_state, event)

    # RUFE die rouletteloop auf und fange den neuen State auf
    game_state, current_state = Gambling.rouletteloop(game_state, current_state, events)
    Characters.steps = Characters.npcmovement(Characters.npc, Characters.steps, Characters.npcspeed)
    Characters.drawing(screen, Characters.character, Characters.npc, Characters.pixles)
    
    # --- ZEICHNEN ---
    screen.fill((0, 0, 0)) # Hintergrund
    pygame.draw.rect(screen, (255, 0, 0), Gambling.roulette_trigger_zone)
    pygame.draw.rect(screen, (0, 0, 255), (Characters.x, Characters.y, Characters.h, Characters.l)) 
    if game_state == "roulette":
        Gambling.roulettespiel_zeichnen(current_state, screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()