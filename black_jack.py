# black_jack.py von Chatgpt, wurde von Luc in main.py implementiert
import pygame
import random
import Characters
import musik
import Pixel_Währung_und_Sammlung

pygame.init()
pygame.font.init()

# --- Schriftarten ---
font_medium = pygame.font.SysFont('Arial', 30)
font_large  = pygame.font.SysFont('Arial', 50)

# --- Trigger-Zone für Blackjack (Position und Größe anpassen) ---
blackjack_X, blackjack_Y = 900, 560
blackjack_BREITE, blackjack_HOEHE = 50, 50
blackjack_trigger_zone = pygame.Rect(blackjack_X, blackjack_Y, blackjack_BREITE, blackjack_HOEHE)

# --- Globale Variablen / Zustände für Blackjack ---
spieler_bet = []
input_string = ""
bj_player_cards = []
bj_dealer_cards = []
bj_msg = ""
bj_result_text = ""
bj_delay_timer = 0.0

# --- Funktionen für Blackjack-Logik ---

def bj_draw_card():
    """Zieht eine Karte (1-13) und gibt den Blackjack-Wert zurück (Ass=11, Bildkarten=10)."""
    v = random.randint(1, 13)
    if v == 1:   # Ass
        return 11
    if v >= 11:  # Bube, Dame, König
        return 10
    return v

def bj_total(cards):
    """Berechnet die Summe der Karten mit Soft-Ace-Logik (Ass als 1 statt 11, falls > 21)."""
    s = sum(cards)
    aces = cards.count(11)
    while s > 21 and aces > 0:
        s -= 10
        aces -= 1
    return s

def bj_reset_round():
    """Startet eine neue Blackjack-Runde mit zwei Karten für Spieler und Dealer."""
    global bj_player_cards, bj_dealer_cards, bj_msg, bj_result_text, bj_delay_timer
    bj_player_cards = [bj_draw_card(), bj_draw_card()]
    bj_dealer_cards = [bj_draw_card(), bj_draw_card()]
    bj_msg = "H=Hit  S=Stand  R=Restart  Q=Exit"
    bj_result_text = ""
    bj_delay_timer = 0.0

# --- NEU HINZUGEFÜGT: Funktion zum Prüfen auf einen Natural Blackjack ---
def bj_check_for_blackjack():
    """Prüft nach dem Austeilen auf einen sofortigen Blackjack und gibt den neuen Zustand zurück."""
    global bj_msg, bj_result_text
    p_total = bj_total(bj_player_cards)
    d_total = bj_total(bj_dealer_cards)

    if p_total == 21 and d_total == 21:
        bj_result_text = "Push (beide Blackjack)"
        bj_msg = "Unentschieden. (R=Restart  Q=Exit)"
        return "bj_result"
    elif p_total == 21:
        bj_result_text = "BLACKJACK! Player gewinnt!"
        bj_msg = "BLACKJACK! (R=Restart  Q=Exit)"
        try:
            musik.play_music("assets/sfx/gambling_win.mp3", loop=False, volume=0.7)
        except Exception:
            pass
        return "bj_result"
    elif d_total == 21:
        bj_result_text = "Dealer hat Blackjack!"
        bj_msg = "Dealer gewinnt! (R=Restart  Q=Exit)"
        try:
            musik.play_music("assets/sfx/gambling_loose.mp3", loop=False, volume=0.7)
        except Exception:
            pass
        return "bj_result"
    
    return "waiting_for_number_input"

# ----- Zustand: Escape / Verlassen des Blackjack-Modus -----
def escapeblackjack(game_state, event):
    """Beendet Blackjack bei Q-Taste, setzt Musik zurück und wechselt zurück zum normalen Spiel."""
    if game_state == "blackjack" and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            game_state = "normal"
            musik.stop_music()
            musik.play_music("assets/sfx/main_theme.mp3", loop=True, volume=0.5)
    return game_state

# ----- Zustand: Wechsel in den Blackjack-Modus -----
def blackjackloop(game_state, bj_state, events):
    """Wechselt in Blackjack, wenn der Spieler die Trigger-Zone betritt."""
    if game_state == "normal":
        if Characters.character.colliderect(blackjack_trigger_zone):
            if Pixel_Währung_und_Sammlung.wallet.get() == 0:
                game_state = "normal"
            else:
                musik.stop_music()
                musik.play_music("assets/sfx/gambling_theme.mp3", loop=True, volume=0.5)
                game_state = "blackjack"
                bj_reset_round()
                bj_state = bj_check_for_blackjack()
    return game_state, bj_state

# ----- Zustand: Blackjack-Spiel-Logik -----
def blackjackspiel_logik(bj_state, events, dt=0.0):
    """State-Machine für Blackjack: Steuerung der Spielphasen und Eingaben."""
    global bj_player_cards, bj_dealer_cards, bj_msg, bj_result_text, bj_delay_timer, spieler_bet, input_string

    if bj_state == "waiting_for_number_input":
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
                            bet_list.append(num)
                        
                        if not bet_list: # Wenn Eingabe leer war
                            raise ValueError

                        spieler_bet = bet_list
                        Pixel_Währung_und_Sammlung.wallet.spend(spieler_bet[0])
                        input_string = ""
                        return "bj_player"

                    except ValueError:
                        # Wenn die Eingabe ungültig war
                        input_string = "UNGÜLTIG!" # Feedback an Spieler
                
                # Mit BACKSPACE löschen
                elif event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1] # Letztes Zeichen entfernen
                
                # Normales Tippen (Zahlen und Komma)
                elif event.unicode.isdigit() or event.unicode == ',':
                    # Füge nur Zahlen oder ein Komma zur Eingabe hinzu
                    input_string += event.unicode

    # --- bj_player: Spieler entscheidet Hit oder Stand ---
    if bj_state == "bj_player":
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_h:   # Hit: Karte ziehen
                    bj_player_cards.append(bj_draw_card())
                    if bj_total(bj_player_cards) > 21:
                        bj_msg = "Bust! Dealer wins. (R=Restart  Q=Exit)"
                        return "bj_result"
                elif e.key == pygame.K_s: # Stand: Dealer ist dran
                    bj_msg = "Dealer spielt..."
                    bj_delay_timer = 0.0 # Timer zurücksetzen
                    return "bj_dealer"
                elif e.key == pygame.K_r: # Runde neu starten
                    bj_reset_round()
                    # --- GEÄNDERT: Nach Reset erneut auf Blackjack prüfen ---
                    return bj_check_for_blackjack()
        return bj_state

    # --- bj_dealer: Dealer zieht Karten bis mindestens 17 ---
    if bj_state == "bj_dealer":
        bj_delay_timer += dt
        if bj_delay_timer < 0.3:  # kurzer Delay für bessere Darstellung
            return bj_state

        # Diese Schleife ist korrekt und zieht so lange, bis >= 17 erreicht ist.
        while bj_total(bj_dealer_cards) < 17:
            bj_dealer_cards.append(bj_draw_card())

        p = bj_total(bj_player_cards)
        d = bj_total(bj_dealer_cards)
        if d > 21 or p > d:
            bj_result_text = "Player gewinnt!"
            Pixel_Währung_und_Sammlung.wallet.add(2*spieler_bet[0])
            bj_msg = "Player gewinnt! (R=Restart  Q=Exit)"
            try:
                musik.play_music("assets/sfx/gambling_win.mp3", loop=False, volume=0.7)
            except Exception:
                pass
        elif p < d:
            bj_result_text = "Dealer gewinnt!"
            bj_msg = "Dealer gewinnt! (R=Restart  Q=Exit)"
            try:
                musik.play_music("assets/sfx/gambling_loose.mp3", loop=False, volume=0.7)
            except Exception:
                pass
        else:
            bj_result_text = "Push (Unentschieden)"
            bj_msg = "Unentschieden. (R=Restart  Q=Exit)"
        return "bj_result"

    # --- bj_result: Ergebnis anzeigen und auf neue Runde warten ---
    if bj_state == "bj_result":
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE or e.key == pygame.K_r: # Neue Runde starten
                    bj_reset_round()
                    # --- GEÄNDERT: Nach Reset erneut auf Blackjack prüfen ---
                    return bj_check_for_blackjack()
        return bj_state
    
    if Pixel_Währung_und_Sammlung.wallet.get() == 0:
        game_state = "normal"
        return game_state

    return bj_state

# ----- Zustand: Zeichnen des Blackjack-Panels -----
def blackjackspiel_zeichnen(bj_state, screen):
    """Zeichnet das Blackjack-Panel mit Karten, Texten und Status."""
    
    # 1. Das Haupt-Panel und der Titel werden immer gezeichnet
    panel = pygame.Rect(560, 520, 700, 260)
    pygame.draw.rect(screen, (25, 28, 35), panel)
    pygame.draw.rect(screen, (80, 90, 110), panel, 2)
    screen.blit(font_large.render("BLACKJACK", True, (255, 255, 0)), (panel.x + 20, panel.y + 10))
    
    # 2. Prüfen, ob wir im Texteingabe-Modus sind
    if bj_state == "waiting_for_number_input":
        # Wenn ja, zeichne das Eingabefeld zentriert im Panel
        
        # Anweisungstext
        anweisung_text = font_medium.render("Gib deinen Einsatz ein:", True, (255, 255, 255))
        anweisung_rect = anweisung_text.get_rect(center=(panel.centerx, panel.y + 80))
        screen.blit(anweisung_text, anweisung_rect)

        # Das sichtbare Textfeld
        input_box_rect = pygame.Rect(0, 0, 300, 50)
        input_box_rect.center = panel.center
        pygame.draw.rect(screen, (10, 10, 10), input_box_rect)

        # Der getippte Text (Annahme: globale Variable 'input_string' existiert)
        input_surface = font_large.render(input_string, True, (255, 255, 0))
        screen.blit(input_surface, (input_box_rect.x + 15, input_box_rect.y + 5))
        
        # Ein blinkender Cursor für besseres Feedback
        if (pygame.time.get_ticks() // 500) % 2 == 1:
            cursor_pos = input_box_rect.x + 15 + input_surface.get_width()
            cursor_rect = pygame.Rect(cursor_pos, input_box_rect.y + 10, 3, input_box_rect.height - 20)
            pygame.draw.rect(screen, (255, 255, 255), cursor_rect)
            
    else:
        # 3. Wenn NICHT im Texteingabe-Modus, zeichne das normale Spielbrett
        
        # Dealer-Karten (zweite Karte verdeckt, solange Spieler dran ist)
        dy = panel.y + 70
        if bj_state == "bj_player":
            dealer_label = f"Dealer: {bj_dealer_cards[0]}  ?"
        else:
            dealer_label = f"Dealer: {' '.join(map(str, bj_dealer_cards))} = {bj_total(bj_dealer_cards)}"
        screen.blit(font_medium.render(dealer_label, True, (220, 220, 220)), (panel.x + 20, dy))

        # Spieler-Karten und Summe
        py = dy + 40
        player_label = f"Player: {' '.join(map(str, bj_player_cards))} = {bj_total(bj_player_cards)}"
        screen.blit(font_medium.render(player_label, True, (220, 220, 220)), (panel.x + 20, py))

        # Steuerungs-Hinweise
        my = py + 40
        screen.blit(font_medium.render(bj_msg, True, (200, 230, 255)), (panel.x + 20, my))

        # Ergebnis-Text (nur im Ergebnis-Zustand)
        if bj_state == "bj_result":
            ry = my + 40
            screen.blit(font_medium.render(bj_result_text, True, (255, 255, 255)), (panel.x + 20, ry))