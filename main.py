import pygame
import Gambling
import Characters
import musik
import ostblock
import mapinteraction
import Slots
import black_jack
import herz_system
import Pixel_Währung_und_Sammlung
import shop_system
import Reaktion
import Titel_effect

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidtmann_Hunter69")
clock = pygame.time.Clock()
#all rect objects or sprites that arent the player are added here
almosteverything = mapinteraction.add_to_almosteverything([ostblock.wallcreation(), Gambling.roulette_trigger_zones, Characters.npcs, Slots.slot_trigger_zones, black_jack.blackjack_trigger_zones, ostblock.map_imgsp, Reaktion.reaktion_trigger_zone], mapinteraction.almosteverything)

# variables for remembering things between frames
last_pixel = 0
last_renzo = "Renzo/Renzo_1.png"
last_interaction = 0
stepsw = 0
stepsp = 0

lives = 3

# Player variables
x, y = 700, 500
dx, dy = 0, 0

running = True
sprint_unlocked = False
game_state = "normal" # Die EINZIGE game_state Variable
current_state = "waiting_for_bet" # für Roulette
slots_state = "auf_Start_warten" # für Slots
bj_state = "bj_waiting"
Titel_effect.show_game_title_fade(screen, title="Frau_Weidtmann_Hunter69", duration=7)
musik.play_music("assets/sfx/main_theme.mp3", loop=True, volume=0.5)
#main loop
while running:
    
     # Events *einmal* pro Frame holen
     events = pygame.event.get()
    
     for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #game stops when ESCAPE is pressed
                    running = False
                if event.key == pygame.K_p and game_state == "normal":
                    shop_system.shop.toggle()
        if shop_system.shop.open:
            lives, sprint_unlocked, shop_message = shop_system.shop.handle_event(
                event,
                Pixel_Währung_und_Sammlung.wallet,
                lives,
                shop_system.max_lives,
                sprint_unlocked
            )

        # Events an die Funktionen übergeben, die sie brauchen
        game_state = Gambling.escaperoulette(game_state, event)
        game_state = Slots.escapeslot(game_state, event)
        game_state = black_jack.escapeblackjack(game_state, event)
        game_state = Reaktion.escapereaktion(game_state, event)

     if game_state == "normal":
            x, y, dx, dy = mapinteraction.wallinteraction(x, y, dx, dy, almosteverything, sprint_unlocked) #Wall collition plus Character Movement
            game_state,current_state = Gambling.rouletteloop(game_state, current_state, events)
            game_state,slots_state = Slots.slotloop(game_state,slots_state, events)
            game_state,bj_state = black_jack.blackjackloop(game_state, bj_state, events)
            Characters.stepsw, Characters.stepsp, xw, yw, xp, yp = Characters.npcmovement(Characters.npcs, Characters.stepsw, Characters.npcspeedw, Characters.stepsp, Characters.npcspeedp) #moving npcs
            lives, last_interaction = Characters.npcinteraction(lives, last_interaction)
            game_state = Reaktion.reaktionloop(game_state)

     elif game_state == "roulette":
         current_state = Gambling.roulettespiel_logik(current_state, events)

     elif game_state == "slot":
         slots_state = Slots.ergebnisseslot(slots_state, events)

     elif game_state == "blackjack":
         bj_state = black_jack.blackjackspiel_logik(bj_state, events, dt=1.0)
     
     elif game_state == "Reaktion":
          Reaktion.reaktion_logik(events)

     # ZEICHNEN
     screen.fill((255, 255, 255)) # Hintergrund
     ostblock.drawmap(ostblock.map_imgup)

     Gambling.draw_roulette_trigger(Gambling.roulette_trigger_zones, screen)
     Slots.draw_slots_trigger(screen, Slots.slot_trigger_zones)
     black_jack.blackjack_draw_trigger(screen, black_jack.blackjack_trigger_zones)
     pygame.draw.rect(screen,(255,141,161), Reaktion.reaktion_trigger_zone)
     last_pixel, last_renzo, stepsw, stepsp = Characters.drawing(screen, Characters.character, Characters.npcs, Characters.pixles, last_pixel, last_renzo, stepsw, stepsp, xw, yw, xp, yp)
     lives = herz_system.draw_lives(screen, lives)
     if lives == 0:
          pygame.quit()
    #hier werden verschiedene Menus und icons gerendered
     Pixel_Währung_und_Sammlung.menu(Pixel_Währung_und_Sammlung.surface, Pixel_Währung_und_Sammlung.hudx, Pixel_Währung_und_Sammlung.hudy, Pixel_Währung_und_Sammlung.wallet.get(), size=150, gap=6)
     shop_system.draw_shop_icon(shop_system.surface, shop_system.sx, shop_system.sy, size = 200)
     shop_system.shop.draw(screen, Pixel_Währung_und_Sammlung.wallet)
    
     if game_state == "roulette":
          Gambling.roulettespiel_zeichnen(current_state, screen)
     elif game_state == "slot":
          Slots.slotszeichnen(screen, slots_state, Slots.Ergebnisliste, Slots.Mitteilung)
     elif game_state == "blackjack":
          black_jack.blackjackspiel_zeichnen(bj_state, screen)
     elif game_state == "Reaktion":
          Reaktion.reaktion_zeichnen(screen)
    
     pygame.display.update()
     clock.tick(60)

pygame.quit()