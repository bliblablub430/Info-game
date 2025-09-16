import pygame
import random 
import Characters

pygame.init()
pygame.Rect

roulette_X = 760
roulette_Y = 560
roulette_Breite = 50
roulette_Höhe = 50
roulette_trigger_zone = pygame.Rect(roulette_X, roulette_Y, roulette_Breite, roulette_Höhe)
running = True
roulettechance = random.randint(0,36)
würfelchance = random.randint(1,6)
game_state = "normal"

def escaperoulette(game_state, event):
    if game_state == "roulette" and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q: # 'Q' zum Beenden
            game_state = "normal"
    return game_state

def rouletteloop(game_state):
    if game_state == "normal":
        dx, dy = Characters.get_movement_vector()

        Characters.x += dx * Characters.speed
        Characters.y += dy * Characters.speed
        
        # --- KOLLISIONS-CHECK ---
        # Prüft, ob sich das Spieler-Rechteck und die Zone überlappen
        aktuelles_spieler_rect = pygame.Rect(Characters.x, Characters.y, Characters.h, Characters.l)
        if aktuelles_spieler_rect.colliderect(roulette_trigger_zone):
            # !! TRIGGER !!
            # Der Spieler hat die Zone betreten. Wechsle den Zustand.
            print("Willkommen beim Roulette! Drücke 'Q' zum Verlassen.")
            game_state = "roulette"

    elif game_state == "roulette":
            roulettespiel()
    return game_state

def roulettespiel():
    print("drücke r um auf Rot zu setzen" \
    "drücke s um Schwarz zu setzen" \
    "drücke t um auf die Zahlen 1-18 (lower) zu setzen oder h um auf 19-36 zu setzen (higher)" \
    "drücke g um auf die geraden Zahlen zu setzen oder u um auf die Ungeraden zu setzen" \
    "drücke c um auf das erste Drittel zu setzen oder auf v um auf das zweite Drittel zu setzten oder auf b für das dritte Drittel" \
    "drücke y um auf eine belibige Zahl zu setzten")
    wunsch = input("Bets please:")
    if wunsch == "r":
        wunsch = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    elif wunsch == "s":
        wunsch = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    elif wunsch == "t":
        wunsch = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    elif wunsch == "h":
        wunsch = [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
    elif wunsch == "g":
        wunsch = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
    elif wunsch == "u":
        wunsch = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
    elif wunsch == "c":
        wunsch = [1,2,3,4,5,6,7,8,9,10,11,12]
    elif wunsch == "v":
        wunsch = [13,14,15,16,17,18,19,20,21,22,23,24]
    elif wunsch == "b":
        wunsch = [25,26,27,28,29,30,31,32,33,34,35,36]
    else:
        wunsch = list(wunsch)
    zusäztlichebets = int(input("auf wie viele Zahlen willst du noch setzten?"))
    for i in range(zusäztlichebets):
        bet = int(input("auf welche Zahl möchtest du setzen:"))
        wunsch.append(bet)
    if roulettechance in wunsch:
        print("you win")
    else:
        print("you lose")
    erneut = input("drücke y um nochmals zu spielen")
    if erneut == "y":
        roulettespiel()
    else:
        print("drücke q um das Spiel zu verlassen")