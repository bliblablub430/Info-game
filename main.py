import pygame
import Gambling
import Characters
import musik
import ostblock
import mapinteraction

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidtmann_Hunter69")
clock = pygame.time.Clock()
ostblock.wallcreation()

# Player variables
x, y = 700, 500
dx, dy = 0, 0

running = True
game_state = "normal" # Die EINZIGE game_state Variable
current_state = "waiting_for_bet" # für Roulette
musik.play_music("assets/sfx/main_theme.mp3", loop=True, volume=0.5)

while running:
    
    # Events *einmal* pro Frame holen
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Events an die Funktionen übergeben, die sie brauchen
        game_state = Gambling.escaperoulette(game_state, event)

    # RUFE die rouletteloop auf und fange den neuen State auf
    if game_state == "normal":
            x, y, dx, dy = mapinteraction.wallinteraction(x, y, dx, dy)
            game_state,current_state = Gambling.rouletteloop(game_state, current_state, events)
            Characters.steps = Characters.npcmovement(Characters.npc, Characters.steps, Characters.npcspeed)

    elif game_state == "roulette":
         current_state = Gambling.roulettespiel_logik(current_state, events)
    
    # --- ZEICHNEN ---
    screen.fill((255, 255, 255)) # Hintergrund
    pygame.draw.rect(screen, (255, 0, 0), Gambling.roulette_trigger_zone)
    Characters.drawing(screen, Characters.character, Characters.npc, Characters.pixles) 
    if game_state == "roulette":
        Gambling.roulettespiel_zeichnen(current_state, screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()