import pygame
import random 
import Characters
import musik
import Pixel_Währung_und_Sammlung
import mapinteraction

pygame.init()
pygame.Rect

pygame.font.init() # Stellt sicher, dass Fonts geladen sind
font_medium = pygame.font.SysFont('Arial', 30)
font_large = pygame.font.SysFont('Arial', 50)

# Globale Variablen, um den Spielstand zwischenzufspeichern
spieler_bet = []
spieler_bet2 = []
gewinn_zahl = -1
ergebnis_text = ""
input_string = ""
input_string2 = ""

roulette_X = 800
roulette_Y = 800
roulette_Breite = 50
roulette_Höhe = 50
running = True
roulettechance = random.randint(0,36)
game_state = "normal"
roulette_trigger_zones = [pygame.Rect(roulette_X, roulette_Y, roulette_Breite, roulette_Höhe), pygame.Rect(roulette_X + 1000, roulette_Y + 200, roulette_Breite, roulette_Höhe), pygame.Rect(roulette_X + 100, roulette_Y + 700, roulette_Breite, roulette_Höhe)]


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
        for i in range(len(roulette_trigger_zones)):
            if Characters.character.rect.colliderect(roulette_trigger_zones[i]): #Trigger
                if Pixel_Währung_und_Sammlung.wallet.get() == 0:
                    game_state = "normal"
                else:
                    musik.stop_music()
                    musik.play_music("assets/sfx/gambling_theme.mp3", loop=True, volume=0.5)
                    game_state = "roulette"
                    current_state = "waiting_for_number_input2"
    return game_state, current_state

def roulettespiel_logik(current_state, events):
         
    # Wir brauchen global, da wir sie von außerhalb der Funktion ändern
    global spieler_bet, gewinn_zahl, ergebnis_text, input_string, spieler_bet2, input_string2
    
    # ----- ZUSTAND 1: WARTEN AUF EINSATZ -----
    
    if current_state == "waiting_for_number_input2": # Idee von AI, bearbeitet von Human
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Eingabe mit ENTER bestätigen
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    try:
                        # Versuche, die Eingabe in eine Liste von Zahlen umzuwandeln
                        # Wir erlauben Kommas, um mehrere Zahlen zu trennen
                        numbers_as_strings = input_string2.split(',')
                        bet_list = []
                        
                        for num_str in numbers_as_strings:
                            num = int(num_str.strip()) # .strip() entfernt Leerzeichen
                            bet_list.append(num)
                        
                        if not bet_list: # Wenn Eingabe leer war
                            raise ValueError

                        spieler_bet2 = bet_list
                        Pixel_Währung_und_Sammlung.wallet.spend(spieler_bet2[0])    #Human generated
                        input_string2 = ""
                        return "waiting_for_bet"

                    except ValueError:
                        # Wenn die Eingabe ungültig war
                        input_string2 = "UNGÜLTIG!" # Feedback an Spieler
                
                # Mit BACKSPACE löschen
                elif event.key == pygame.K_BACKSPACE:
                    input_string2 = input_string2[:-1] # Letztes Zeichen entfernen
                
                # Normales Tippen (Zahlen und Komma)
                elif event.unicode.isdigit() or event.unicode == ',':
                    # Füge nur Zahlen oder ein Komma zur Eingabe hinzu
                    input_string2 += event.unicode

    if current_state == "waiting_for_bet":
        for event in events:
            if event.type == pygame.KEYDOWN:
                bet_made = False
                
                # 'r' für Rot # AI
                if event.key == pygame.K_r:
                    spieler_bet = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
                    bet_made = True
                
                # 's' für Schwarz # AI
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

                elif event.key == pygame.K_y: #AI
                    input_string = "" # Eingabefeld zurücksetzen
                    return "waiting_for_number_input"

                if bet_made:
                    return "spinning" # Nächster Zustand: Rad dreht sich
    
    if current_state == "waiting_for_number_input": # AI
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
            Pixel_Währung_und_Sammlung.wallet.add((36/len(spieler_bet))*spieler_bet2[0]) # Formel zur berechnung vom Gewinn
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
                    return "waiting_for_number_input2"
                
    if Pixel_Währung_und_Sammlung.wallet.get() == 0:
        game_state = "normal"
        return game_state
    
    return current_state 

def draw_roulette_trigger(roulette_trigger_zones, screen):
    for i in range(len(roulette_trigger_zones)):
        pygame.draw.rect(screen, (127,0,255), roulette_trigger_zones[i])

def roulettespiel_zeichnen(current_state, screen): # aus black_jack.py übernommen, wobei jenes File viel AI enthält, angepasst auf dieses File von Luc
    """
    Zeichnet das Roulette-Panel sauber und strukturiert.
    Die Eingabe für Einsatz und Zahlen ist jetzt in zwei getrennten Schritten.
    """
    # 1. Panel definieren und zeichnen 
    panel = pygame.Rect(0, 0, 850, 400)
    panel.center = (screen.get_width() / 2, screen.get_height() / 2 + 100)
    pygame.draw.rect(screen, (25, 28, 35), panel)
    pygame.draw.rect(screen, (80, 90, 110), panel, 3)                          
    titel_surface = font_large.render("ROULETTE", True, (255, 255, 0))
    screen.blit(titel_surface, (panel.x + 20, panel.y + 15))

    # --- ZUSTAND 1: EINSATZ EINGEBEN --- 
    if current_state == "waiting_for_number_input2":
        # Anweisungstext
        anweisung_text = font_medium.render("Gib deinen Einsatz ein:", True, (255, 255, 255))
        anweisung_rect = anweisung_text.get_rect(center=(panel.centerx, panel.y + 120))
        screen.blit(anweisung_text, anweisung_rect)

        # Sichtbares Textfeld
        input_box_rect = pygame.Rect(0, 0, 300, 50)
        input_box_rect.center = panel.center
        pygame.draw.rect(screen, (10, 10, 10), input_box_rect)

        # Getippter Text für den Einsatz
        input_surface = font_large.render(input_string2, True, (255, 255, 0))
        screen.blit(input_surface, (input_box_rect.x + 15, input_box_rect.y + 5))
        
        # Blinkender Cursor
        if (pygame.time.get_ticks() // 500) % 2 == 1:
            cursor_pos = input_box_rect.x + 15 + input_surface.get_width()
            cursor_rect = pygame.Rect(cursor_pos, input_box_rect.y + 10, 4, input_box_rect.height - 20)
            pygame.draw.rect(screen, (255, 255, 255), cursor_rect)
            
        # Hilfetext
        hilfe_text = font_medium.render("Drücke [ENTER] zum Bestätigen", True, (200, 200, 200))
        hilfe_rect = hilfe_text.get_rect(center=(panel.centerx, panel.bottom - 60))
        screen.blit(hilfe_text, hilfe_rect)

    # --- ZUSTAND 2: ZAHLEN AUSWÄHLEN --- 
    elif current_state == "waiting_for_number_input":
        # Anweisungstext
        anweisung_text = font_medium.render("Gib Zahlen (0-36) ein, getrennt durch Komma:", True, (255, 255, 255))
        anweisung_rect = anweisung_text.get_rect(center=(panel.centerx, panel.y + 120))
        screen.blit(anweisung_text, anweisung_rect)

        # Sichtbares Textfeld
        input_box_rect = pygame.Rect(0, 0, 600, 60)
        input_box_rect.center = panel.center
        pygame.draw.rect(screen, (10, 10, 10), input_box_rect)

        # Getippter Text für die Zahlen
        input_surface = font_large.render(input_string, True, (255, 255, 0))
        screen.blit(input_surface, (input_box_rect.x + 15, input_box_rect.y + 5))
        
        # Blinkender Cursor
        if (pygame.time.get_ticks() // 500) % 2 == 1:
            cursor_pos = input_box_rect.x + 15 + input_surface.get_width()
            cursor_rect = pygame.Rect(cursor_pos, input_box_rect.y + 10, 4, input_box_rect.height - 20)
            pygame.draw.rect(screen, (255, 255, 255), cursor_rect)
        
        # Hilfetext
        hilfe_text = font_medium.render("Drücke [ENTER] zum Bestätigen oder [BACKSPACE] zum Löschen", True, (200, 200, 200))
        hilfe_rect = hilfe_text.get_rect(center=(panel.centerx, panel.bottom - 60))
        screen.blit(hilfe_text, hilfe_rect)

    # --- ZUSTAND: AUF GRUPPEN-WETTE WARTEN ---
    elif current_state == "waiting_for_bet":
        instructions = [
            "PLATZIERE DEINE WETTE:", "",
            "[R] Rot  |  [S] Schwarz",              #Formatierung von AI
            "[G] Gerade  |  [U] Ungerade",
            "[T] Niedrig (1-18)  |  [H] Hoch (19-36)",
            "[C] 1. Dutzend | [V] 2. Dutzend | [B] 3. Dutzend"
        ]
        
        start_y = panel.y + 80
        line_height = 40
        for i, text in enumerate(instructions): #AI
            text_surface = font_medium.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(centerx=panel.centerx, y=start_y + i * line_height)
            screen.blit(text_surface, text_rect)
            
        y_text_surface = font_medium.render("Drücke [Y], um auf einzelne Zahlen zu setzen & Einsatz zu wählen", True, (255, 255, 0))
        y_text_rect = y_text_surface.get_rect(centerx=panel.centerx, y=panel.bottom - 50)
        screen.blit(y_text_surface, y_text_rect)

    # --- ZUSTAND: RAD DREHT SICH --- 
    elif current_state == "spinning":
        text_surface = font_large.render("...Rad dreht sich...", True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=panel.center)
        screen.blit(text_surface, text_rect)
        
    # --- ZUSTAND: ERGEBNIS ANZEIGEN ---
    elif current_state == "show_result":
        ergebnis_surface = font_large.render(ergebnis_text, True, (255, 255, 255))
        ergebnis_rect = ergebnis_surface.get_rect(center=(panel.centerx, panel.y + 120))
        screen.blit(ergebnis_surface, ergebnis_rect)
        
        weiter_surface = font_medium.render("Drücke [LEERTASTE] zum Weiterspielen", True, (200, 200, 200))
        weiter_rect = weiter_surface.get_rect(center=(panel.centerx, panel.bottom - 80))
        screen.blit(weiter_surface, weiter_rect)