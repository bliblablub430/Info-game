import pygame
import Gambling
import Characters
import musik
import ostblock
import mapinteraction
import Slots
import black_jack
import Pixel_Währung_und_Sammlung
import coordinaten_system

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidtmann_Hunter69")
clock = pygame.time.Clock()

almosteverything = mapinteraction.add_to_almosteverything([ostblock.wallcreation(), Gambling.roulette_trigger_zone, Characters.npc, Slots.slot_trigger_zone, black_jack.blackjack_trigger_zone], mapinteraction.almosteverything)

last_pixel = 0

# Player variables
x, y = 700, 500
dx, dy = 0, 0

running = True
game_state = "normal" # Die EINZIGE game_state Variable
current_state = "waiting_for_bet" # für Roulette
slots_state = "auf_Start_warten" # für Slots
bj_state = "bj_waiting"
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
        game_state = Slots.escapeslot(game_state, event)
        game_state = black_jack.escapeblackjack(game_state, event)

    # RUFE die rouletteloop auf und fange den neuen State auf
    if game_state == "normal":
            x, y, dx, dy = mapinteraction.wallinteraction(x, y, dx, dy, almosteverything) #Wall collition plus Character Movement
            game_state,current_state = Gambling.rouletteloop(game_state, current_state, events)
            game_state,slots_state = Slots.slotloop(game_state,slots_state, events)
            game_state,bj_state = black_jack.blackjackloop(game_state, bj_state, events)
            Characters.steps = Characters.npcmovement(Characters.npc, Characters.steps, Characters.npcspeed)

    elif game_state == "roulette":
         current_state = Gambling.roulettespiel_logik(current_state, events)

    elif game_state == "slot":
         slots_state = Slots.ergebnisseslot(slots_state, events)

    elif game_state == "blackjack":
         bj_state = black_jack.blackjackspiel_logik(bj_state, events, dt=1.0)
    
    # --- ZEICHNEN ---
    screen.fill((255, 255, 255)) # Hintergrund
    pygame.draw.rect(screen, (255, 0, 0), Gambling.roulette_trigger_zone)
    last_pixel = Characters.drawing(screen, Characters.character, Characters.npc, Characters.pixles, last_pixel) 
    pygame.draw.rect(screen,(255,0,0),Slots.slot_trigger_zone)
    pygame.draw.rect(screen,(255,0,0),black_jack.blackjack_trigger_zone)
    Pixel_Währung_und_Sammlung.menu(Pixel_Währung_und_Sammlung.surface, Pixel_Währung_und_Sammlung.hudx, Pixel_Währung_und_Sammlung.hudy, Pixel_Währung_und_Sammlung.wallet.get(), size=150, gap=6)
    coordinaten_system.draw_coords(coordinaten_system.surface, Characters.character, font_size=24, padding=5)
    if game_state == "roulette":
        Gambling.roulettespiel_zeichnen(current_state, screen)
    elif game_state == "slot":
         Slots.slotszeichnen(screen, slots_state, Slots.Ergebnisliste, Slots.Mitteilung)
    elif game_state == "blackjack":
         black_jack.blackjackspiel_zeichnen(bj_state, screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()