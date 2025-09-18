# Reaktion.py
import pygame
import time
import Characters
import musik # Annahme, dass du später Musik hinzufügen willst

pygame.init()
pygame.font.init()

# --- Konstanten und Schriftarten ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
font = pygame.font.SysFont(None, 48)
font_large = pygame.font.SysFont(None, 80)

# --- Trigger-Zone ---
reaktion_X = 1000
reaktion_Y = 1000
reaktion_Breite = 50
reaktion_Höhe = 50
reaktion_trigger_zone = pygame.Rect(reaktion_X, reaktion_Y, reaktion_Breite, reaktion_Höhe)

# --- Globale Spielvariablen ---
# Diese Variablen speichern den Zustand des Minispiels
spiel_zeit = 10
zahlen_liste = list(range(1, 11))
aktuelle_index = 0
wechselzahl = 1
letzter_wechsel = 0
user_input = ""
start_zeit = 0
game_over = False
ergebnis_text = ""

# --- Hilfsfunktion ---
def unterschied(a, b):
    return abs(a - b)

# --- Hauptfunktionen (bereit für main.py) ---

def reaktion_reset():
    """Setzt alle Spielvariablen für eine neue Runde zurück."""
    global aktuelle_index, wechselzahl, letzter_wechsel, user_input, start_zeit, game_over, ergebnis_text
    
    aktuelle_index = 0
    wechselzahl = zahlen_liste[aktuelle_index]
    letzter_wechsel = time.time()
    user_input = ""
    start_zeit = time.time()
    game_over = False
    ergebnis_text = ""

def escapereaktion(game_state, event):
    """Verlässt das Minispiel mit 'Q'."""
    if game_state == "Reaktion" and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            game_state = "normal"
    return game_state

def reaktionloop(game_state):
    """Startet das Spiel, wenn der Spieler die Zone betritt."""
    if game_state == "normal":
        if Characters.character.rect.colliderect(reaktion_trigger_zone):
            game_state = "Reaktion"
            reaktion_reset() # Spiel beim Betreten zurücksetzen
    return game_state

def reaktion_logik(events):
    """Verarbeitet die Logik des Reaktionsspiels (Timer, Eingaben, etc.)."""
    global aktuelle_index, wechselzahl, letzter_wechsel, user_input, start_zeit, game_over, ergebnis_text

    # Logik nur ausführen, wenn das Spiel nicht vorbei ist
    if not game_over:
        # 1. Eingaben verarbeiten # AI
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    user_input += event.unicode
                elif event.key == pygame.K_RETURN and user_input != "":
                    zahl = int(user_input)
                    
                    if 1 <= zahl <= 10:
                        if zahl == wechselzahl:
                            ergebnis_text = "Reaktionszeit einer Gazelle"
                        elif 0 < unterschied(zahl, wechselzahl) < 3:
                            ergebnis_text = "Reaktionszeit von Frau Lehmann"
                        elif 3 < unterschied(zahl, wechselzahl) < 6:
                            ergebnis_text = "Reaktionszeit von Thong Cena"
                        else:
                            ergebnis_text = "Reaktionszeit von einem Faultier"
                    else:
                        ergebnis_text = "Zahl nicht im Bereich!"
                    
                    game_over = True

        # 2. Zahl wechseln (ca. alle 0.1 Sekunden)
        if time.time() - letzter_wechsel > 0.1:
            aktuelle_index = (aktuelle_index + 1) % len(zahlen_liste)
            wechselzahl = zahlen_liste[aktuelle_index]
            letzter_wechsel = time.time()
            
        # 3. Countdown prüfen
        if int(time.time() - start_zeit) >= spiel_zeit:
            ergebnis_text = "Zeit abgelaufen!"
            game_over = True
    
    # Wenn das Spiel vorbei ist, auf Neustart warten (z.B. mit Leertaste)
    else:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reaktion_reset() # Spiel neu starten

def reaktion_zeichnen(screen):
    """Zeichnet die Oberfläche des Reaktionsspiels."""
    
    # Ein Panel als Hintergrund zeichnen, damit es sich vom Hauptspiel abhebt
    panel = pygame.Rect(0, 0, 800, 400)
    panel.center = (screen.get_width() / 2, screen.get_height() / 2)
    pygame.draw.rect(screen, BLACK, panel)
    pygame.draw.rect(screen, WHITE, panel, 2)
    
    # Verbleibende Zeit anzeigen
    verbleibend = max(0, spiel_zeit - int(time.time() - start_zeit))
    timer_surface = font.render(f"Zeit: {verbleibend}", True, WHITE)
    screen.blit(timer_surface, (panel.left + 20, panel.top + 20))
    
    # Eingabe anzeigen
    eingabe_surface = font.render(f"Eingabe: {user_input}", True, WHITE)
    screen.blit(eingabe_surface, (panel.left + 20, panel.top + 150))
    
    # Wenn Spiel läuft, wechselnde Zahl anzeigen
    if not game_over:
        wechsel_surface = font_large.render(str(wechselzahl), True, RED)
        wechsel_rect = wechsel_surface.get_rect(center=(panel.centerx, panel.centery))
        screen.blit(wechsel_surface, wechsel_rect)
    
    # Wenn Spiel vorbei, Ergebnis anzeigen
    if game_over:
        ergebnis_surface = font.render(ergebnis_text, True, RED)
        ergebnis_rect = ergebnis_surface.get_rect(center=(panel.centerx, panel.centery + 100))
        screen.blit(ergebnis_surface, ergebnis_rect)
        
        # Hinweis zum Neustarten
        if ergebnis_text: # Nur anzeigen, wenn es ein Ergebnis gibt
            neustart_surface = font.render("Drücke [LEERTASTE] zum Neustarten", True, WHITE)
            neustart_rect = neustart_surface.get_rect(center=(panel.centerx, panel.bottom - 40))
            screen.blit(neustart_surface, neustart_rect)