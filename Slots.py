import pygame
import random
import Characters
import Pixel_Währung_und_Sammlung

pygame.init()
pygame.Rect

screen = pygame.display.set_mode((1920, 1080))
minecraftfont = pygame.font.Font("assets/Fonts/minedings.ttf", 50)
font_medium = pygame.font.SysFont('Arial', 30)

slot_X = 100
slot_Y = 200
slot_Breite = 50
slot_Höhe = 50
slot_trigger_zone = pygame.Rect(slot_X, slot_Y, slot_Breite, slot_Höhe)

slotliste = ["I","I","I","I","I","I","I","I","I","A","A","A","A","A","A","T","T","T"]
Ergebnisliste = []
Mitteilung = ""

def escapeslot(game_state, event):
    global Ergebnisliste, Mitteilung

    if game_state == "slot" and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q: # 'Q' zum Beenden
            game_state = "normal"
    return game_state

def slotloop(game_state, slot_state, events):
    if game_state == "normal":
        # --- KOLLISIONS-CHECK ---
        if Characters.character.colliderect(slot_trigger_zone): #Trigger
                if Pixel_Währung_und_Sammlung.wallet.get() < 50:
                    game_state = "normal"
                else:
                    game_state = "slot"
                    slot_state = "auf_Start_warten"
    return game_state, slot_state

def ergebnisseslot(slots_state, events):
    # Diese globalen Variablen müssen deklariert werden, damit die Funktion sie ändern kann.
    global Ergebnisliste, Mitteilung

    if Pixel_Währung_und_Sammlung.wallet.get() < 50:
        game_state = "normal"
        return game_state

    if slots_state == "auf_Start_warten":
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    Pixel_Währung_und_Sammlung.wallet.spend(50)
                    Ergebnisliste = []
                    return "viel_Glück" # Zustand ändern und zurückgeben
            
    if slots_state == "viel_Glück":
        for i in range(3):
            Ergebnisliste.append(random.choice(slotliste))

        a, b, c = Ergebnisliste[0], Ergebnisliste[1], Ergebnisliste[2]

        if a == "T" and b == "T" and c == "T":
            Mitteilung = "BOOM Hauptgewinn"
            Pixel_Währung_und_Sammlung.wallet.add(1000)
        elif a == "A" and b == "A" and c == "A":
            Mitteilung = "Hoher Gewinn"
            Pixel_Währung_und_Sammlung.wallet.add(500)
        elif a == "I" and b == "I" and c == "I":
            Mitteilung = "Normaler Gewinn"
            Pixel_Währung_und_Sammlung.wallet.add(250)
        else:
            Mitteilung = "Verloren du Opfer"
            
        return "Ergebnisse" # Direkt zum nächsten Zustand wechseln

    if slots_state == "Ergebnisse":
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "auf_Start_warten" # Zurück zum Start
                    
    return slots_state # Wenn nichts passiert, den aktuellen Zustand beibehalten

def slotszeichnen(screen, slots_state, Ergebnisliste, Mitteilung):
    # Zustand 1: Warten auf den Start des Spiels
    if slots_state == "auf_Start_warten":
        text1 = font_medium.render("SLOT MASCHINE", True, (0, 0, 0))
        text2 = font_medium.render("Zahle 50 Pixel, [Y] zum Starten", True, (0, 0, 0))
        screen.blit(text1, (850, 400))
        screen.blit(text2, (830, 450))

    # Zustand 2: "Drehung" (wird sehr schnell übersprungen)
    elif slots_state == "viel_Glück":
        text1 = font_medium.render("...Walzen drehen sich...", True, (0, 0, 0))
        screen.blit(text1, (800, 450))

    # Zustand 3: Ergebnis anzeigen
    elif slots_state == "Ergebnisse":
        # Die Symbole aus der Ergebnisliste mit der Minedings-Schriftart zeichnen
        ergebnis_string = " ".join(Ergebnisliste) # Macht z.B. "A I T" aus ['A', 'I', 'T']
        symbol_text = minecraftfont.render(ergebnis_string, True, (0, 0, 0))
        
        # Die Gewinn/Verlust-Mitteilung zeichnen
        mitteilung_text = font_medium.render(Mitteilung, True, (0, 0, 0))
        
        # Anweisung zum Weiterspielen
        weiter_text = font_medium.render("Drücke [LEERTASTE] zum Weiterspielen", True, (0, 0, 0))

        screen.blit(symbol_text, (880, 400))
        screen.blit(mitteilung_text, (820, 500))
        screen.blit(weiter_text, (750, 550))