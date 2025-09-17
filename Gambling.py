import pygame
import random 
import Characters

pygame.init()
pygame.Rect

pygame.font.init() # Stellt sicher, dass Fonts geladen sind
font_medium = pygame.font.SysFont('Arial', 30)
font_large = pygame.font.SysFont('Arial', 50)

# Globale Variablen, um den Spielstand zwischenzufspeichern
spieler_bet = []
gewinn_zahl = -1
ergebnis_text = ""

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

def rouletteloop(game_state, current_state, events):
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
            game_state = "roulette"
            current_state = "waiting_for_bet"

    elif game_state == "roulette":
        current_state = roulettespiel_logik(current_state, events)
    return game_state, current_state

def roulettespiel_logik(current_state, events):
         
    # Wir brauchen global, da wir sie von außerhalb der Funktion ändern
    global spieler_bet, gewinn_zahl, ergebnis_text
    
    # ----- ZUSTAND 1: WARTEN AUF EINSATZ -----
    if current_state == "waiting_for_bet":
        for event in events:
            if event.type == pygame.KEYDOWN:
                bet_made = False
                
                # 'r' für Rot
                if event.key == pygame.K_r:
                    spieler_bet = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
                    bet_made = True
                
                # 's' für Schwarz
                elif event.key == pygame.K_s:
                    spieler_bet = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
                    bet_made = True
                
                # g für gerade
                elif event.key == pygame.K_g:
                    spieler_bet = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
                    bet_made = True
                
                # u für ungerade
                if event.key == pygame.K_u:
                    spieler_bet = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
                    bet_made = True
                
                # t für tiefer als 18
                if event.key == pygame.K_t:
                    spieler_bet = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
                    bet_made = True

                # h für über 18
                if event.key == pygame.K_r:
                    spieler_bet = [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
                    bet_made = True
                
                if bet_made:
                    return "spinning" # Nächster Zustand: Rad dreht sich
                
    # ----- ZUSTAND 2: RAD DREHT SICH (ERGEBNIS BERECHNEN) -----
    if current_state == "spinning":
        gewinn_zahl = random.randint(0, 36)
        
        if gewinn_zahl in spieler_bet:
            ergebnis_text = f"GEWONNEN! Die Zahl ist {gewinn_zahl}"
        elif gewinn_zahl == 0:
            ergebnis_text = f"Verloren. Die Zahl ist 0 (Grün)" # nicht nötig
        else:
            ergebnis_text = f"Verloren. Die Zahl ist {gewinn_zahl}"
            
        spieler_bet = [] # Einsatz zurücksetzen
        return "show_result" # Nächster Zustand: Ergebnis anzeigen
    
    # ----- ZUSTAND 3: ERGEBNIS ANZEIGEN -----
    if current_state == "show_result":
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "waiting_for_bet"

    return current_state 

def roulettespiel_zeichnen(current_state, screen):
    
    if current_state == "waiting_for_bet":
        text1 = font_medium.render("PLATZIERE DEINE WETTE:", True, (255, 255, 255))
        text2 = font_medium.render("Drücke [R] für Rot oder [S] für Schwarz", True, (200, 200, 200))
        screen.blit(text1, (700, 600))
        screen.blit(text2, (700, 650))
        
    elif current_state == "spinning":
        text1 = font_large.render("...Rad dreht sich...", True, (255, 255, 0))
        screen.blit(text1, (700, 600))
        
    elif current_state == "show_result":
        text1 = font_large.render(ergebnis_text, True, (255, 255, 255))
        text2 = font_medium.render("Drücke [LEERTASTE] zum Weiterspielen", True, (200, 200, 200))
        screen.blit(text1, (700, 600))
        screen.blit(text2, (700, 650))