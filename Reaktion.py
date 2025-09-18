import pygame
import time
import Characters
 
pygame.init()

reaktion_X = 500
reaktion_Y = 500
reaktion_Breite = 50
reaktion_Höhe = 50
Reaktiontriggerzone = pygame.Rect(reaktion_X, reaktion_Y, reaktion_Breite, reaktion_Höhe)

def escapereaktion(game_state, event):
    if game_state == "Reaktion" and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q: # 'Q' zum Beenden
            game_state = "normal"
    return game_state

def reaktionloop(game_state):
    if game_state == "normal":
        if Characters.character.colliderect(Reaktiontriggerzone):
            game_state = "Reaktion"
        return game_state

def Reaktionsgeschwindigkeittester():
    # Fenster erstellen
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zahlraten-Spiel")
    # Farben
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    GREEN = (0, 150, 0)
    # Schriftart und grösse
    font = pygame.font.SysFont(None, 48)
    # Funktion für Abstand zweier Zahlen
    def unterschied(a, b):
        return abs(a - b)
    # Spielvariablen->nur provisorisch
    zeit = 10
 
    zahlen_liste = list(range(1, 11))  # Zahlen von 1 bis 10
    aktuelle_index = 0
    wechselzahl = zahlen_liste[aktuelle_index]
    letzter_wechsel = time.time()
    user_input = ""
    clock = pygame.time.Clock()
 
    start_time = time.time()
    game_over = False
    ergebnis_text = ""
 
    # Spielschleife
    running = True
    while running:
        screen.fill(BLACK)
 
        # --- Eingaben abfragen ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            if not game_over and event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    user_input += event.unicode
                elif event.key == pygame.K_RETURN and user_input != "":
                    zahl = int(user_input)
 
                    # Bereich prüfen
                    if zahl < 1 or zahl > 10:
                        ergebnis_text = "Zahl nicht im Bereich!"
                    else:
                        # Bewertung der Reaktionszeit
                        if zahl == wechselzahl:
                            ergebnis_text = "Reaktionszeit einer Gazelle"
                        elif 0 < unterschied(zahl, wechselzahl) < 3:
                            ergebnis_text = "Reaktionszeit von Frau Lehmann"
                        elif 3 < unterschied(zahl, wechselzahl) < 6:
                            ergebnis_text = "Reaktionszeit von Thong Cena"
                        elif 6 <= unterschied(zahl, wechselzahl) <= 10:
                            ergebnis_text = "Reaktionszeit von einem Faultier"
 
                    game_over = True
 
        # Zahl wechseln (alle 0.2 Sekunden)
        if not game_over and time.time() - letzter_wechsel > 0.1:
            aktuelle_index = (aktuelle_index + 1) % len(zahlen_liste)
            wechselzahl = zahlen_liste[aktuelle_index]
            letzter_wechsel = time.time()
 
        #Countdown
        if not game_over:
            vergangen = int(time.time() - start_time)
            verbleibend = max(0, zeit - vergangen)
        else:
            verbleibend = 0
 
        if verbleibend == 0 and not game_over:
            ergebnis_text = "Zeit abgelaufen!"
            game_over = True
 
        # Anzeige wie viu zyt
        timer_surface = font.render(f"Zeit: {verbleibend}", True, WHITE)
        screen.blit(timer_surface, (20, 20))
        # Eingabe auf surface azeige
        eingabe_surface = font.render(f"Eingabe: {user_input}", True, WHITE)
        screen.blit(eingabe_surface, (20, 150))
        # ->Wenn Spiel nicht vorbei, wechselnde Zahl anzeigen
        if not game_over:
            wechsel_surface = font.render(f"Zahl: {wechselzahl}", True, RED)
            screen.blit(wechsel_surface, (400, 150))
        # ->Wenn Spiel vorbei, Ergebnis anzeigen
        if ergebnis_text:
            ergebnis_surface = font.render(ergebnis_text, True, RED)
            screen.blit(ergebnis_surface, (20, 220))
 
        pygame.display.flip() #Aktualisiert den gesamten Bildschirm, sodass alle neu gezeichneten Elemente sichtbar werden.
        clock.tick(60)

if __name__ == "__main__":
    Reaktionsgeschwindigkeittester()