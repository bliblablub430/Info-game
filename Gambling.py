import pygame
import random 
import Characters
import musik

pygame.init()
pygame.Rect

pygame.font.init() # Stellt sicher, dass Fonts geladen sind
font_medium = pygame.font.SysFont('Arial', 30)
font_large = pygame.font.SysFont('Arial', 50)

# Globale Variablen, um den Spielstand zwischenzufspeichern
spieler_bet = []
gewinn_zahl = -1
ergebnis_text = ""
input_string = ""

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
            musik.stop_music()
            musik.play_music("assets/sfx/main_theme.mp3", loop=True, volume=0.5)
    return game_state

def rouletteloop(game_state, current_state, events):
    if game_state == "normal":
        # --- KOLLISIONS-CHECK ---
        # Prüft, ob sich das Spieler-Rechteck und die Zone überlappen
        if Characters.character.colliderect(roulette_trigger_zone): #Trigger
            musik.stop_music()
            musik.play_music("assets/sfx/gambling_theme.mp3", loop=True, volume=0.5)
            game_state = "roulette"
            current_state = "waiting_for_bet"
    return game_state, current_state

def roulettespiel_logik(current_state, events):
         
    # Wir brauchen global, da wir sie von außerhalb der Funktion ändern
    global spieler_bet, gewinn_zahl, ergebnis_text, input_string
    
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
                if event.key == pygame.K_h:
                    spieler_bet = [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
                    bet_made = True
                
                # c für erstes Drittel
                if event.key == pygame.K_c:
                    spieler_bet = [1,2,3,4,5,6,7,8,9,10,11,12]
                    bet_made = True

                # v für zweites Drittel
                if event.key == pygame.K_v:
                    spieler_bet = [13,14,15,16,17,18,19,20,21,22,23,24]
                    bet_made = True

                # b für drittes Drittel
                if event.key == pygame.K_b:
                    spieler_bet = [25,26,27,28,29,30,31,32,33,34,35,36]
                    bet_made = True

                elif event.key == pygame.K_y:
                    input_string = "" # Eingabefeld zurücksetzen
                    return "waiting_for_number_input"

                if bet_made:
                    return "spinning" # Nächster Zustand: Rad dreht sich
    
    if current_state == "waiting_for_number_input":
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Eingabe mit ENTER bestätigen
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    try:
                        # Versuche, die Eingabe in eine Liste von Zahlen umzuwandeln
                        # Wir erlauben Kommas, um mehrere Zahlen zu trennen
                        numbers_as_strings = input_string.split(',')
                        bet_list = []
                        
                        for num_str in numbers_as_strings:
                            num = int(num_str.strip()) # .strip() entfernt Leerzeichen
                            
                            if 0 <= num <= 36:
                                bet_list.append(num)
                            else:
                                raise ValueError # Zahl außerhalb des Bereichs
                        
                        if not bet_list: # Wenn Eingabe leer war
                            raise ValueError

                        spieler_bet = bet_list
                        input_string = ""
                        return "spinning"

                    except ValueError:
                        # Wenn die Eingabe ungültig war
                        input_string = "UNGÜLTIG!" # Feedback an Spieler
                        # Wir bleiben in diesem Zustand, bis die Eingabe gültig ist
                
                # Mit BACKSPACE löschen
                elif event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1] # Letztes Zeichen entfernen
                
                # Normales Tippen (Zahlen und Komma)
                elif event.unicode.isdigit() or event.unicode == ',':
                    # Füge nur Zahlen oder ein Komma zur Eingabe hinzu
                    input_string += event.unicode
        
        return current_state # Bleibe im Eingabe-Zustand
                
    # ----- ZUSTAND 2: RAD DREHT SICH (ERGEBNIS BERECHNEN) -----
    if current_state == "spinning":
        gewinn_zahl = random.randint(0, 36)
        
        if gewinn_zahl in spieler_bet:
            ergebnis_text = f"GEWONNEN! Die Zahl ist {gewinn_zahl}"
            musik.play_music("assets/sfx/gambling_win.mp3", loop=False, volume=0.7)
        else:
            ergebnis_text = f"Verloren. Die Zahl ist {gewinn_zahl}"
            musik.play_music("assets/sfx/gambling_loose.mp3", loop=False, volume=0.7)
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
        text2 = font_medium.render("Drücke [R] für Rot oder [S] für Schwarz" \
        "[G] für gerade Zahlen, [U] für ungerade Zahlen", True, (255, 255, 255))
        text3 = font_medium.render("[T] für Zahlen unter 18 und [H] für Zahlen über 18", True, (255,255,255))
        text4 = font_medium.render("[C] für das erste Drittel der Zahlen, [V] für das zweite Drittel und [B] für das dritte Drittel", True,(255,255,255))
        text5 = font_medium.render("Drücke [Y], um auf einzelne Zahlen zu setzen", True, (255, 255, 0)) # Gelb hervorgehoben
        screen.blit(text1, (700, 600))
        screen.blit(text2, (550, 650))
        screen.blit(text3, (600, 700))
        screen.blit(text4, (500,750))
        screen.blit(text5, (550,800))
        
    elif current_state == "waiting_for_number_input":
        text1 = font_medium.render("Gib Zahlen (0-36) ein, getrennt durch Komma:", True, (255, 255, 255))
        
        # Dies ist dein "Textfeld", das anzeigt, was du tippst
        input_text_surface = font_large.render(input_string, True, (255, 255, 0))
        
        text2 = font_medium.render("Drücke [ENTER] zum Bestätigen oder [BACKSPACE] zum Löschen", True, (200, 200, 200))

        screen.blit(text1, (600, 600))
        screen.blit(input_text_surface, (600, 650))
        screen.blit(text2, (600, 700))

    elif current_state == "spinning":
        text1 = font_large.render("...Rad dreht sich...", True, (255, 255, 0))
        screen.blit(text1, (700, 600))
        
    elif current_state == "show_result":
        text1 = font_large.render(ergebnis_text, True, (255, 255, 255))
        text2 = font_medium.render("Drücke [LEERTASTE] zum Weiterspielen", True, (200, 200, 200))
        screen.blit(text1, (700, 600))
        screen.blit(text2, (700, 650))