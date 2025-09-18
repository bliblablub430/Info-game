# Pixel-Währung + Sammeln + HUD
import pygame

amount = 10
surface = pygame.display.set_mode((150, 100))
hudx = 250
hudy = 100

# Wallet (Währung) – speichert, wie viele Pixel du hast
class PixelBank:
    def __init__(self, start=10):
        self.amount = int(start)

    def add(self, n=1):  # Pixel hinzufügen
        self.amount += max(0, int(n))

    def can_spend(self, n):  # Prüfen, ob genug Pixel da sind
        return self.amount >= int(n)

    def spend(self, n):  # Pixel ausgeben
        n = int(n)
        if self.can_spend(n):
            self.amount -= n
            return True
        return False

    def get(self):  # Anzahl Pixel abfragen
        return self.amount
    
wallet = PixelBank()

# HUD: Anzeige oben rechts/links 
def menu(surface, hudx, hudy, amount, size=150, gap=6):
    # kleines "Pixel"-Icon (einfarbiges Quadrat)
    icon = pygame.Surface((size + 50, size))
    icon.fill((120, 220, 255))  # hellblau = Pixel
    surface.blit(icon, (hudx, hudy))

    font = pygame.font.Font(None, size + 8)
    text = font.render(f"x {amount}", True, (0, 0, 0))
    surface.blit(text, (hudx - gap, hudy))

# Sammelbare Pixel an festen Positionen erzeugen
def make_pickup_rects(positions, size=12):
   # Erzeugt kleine Rechtecke an Positionen [(x,y), ...]
    return [pygame.Rect(px, py, size, size) for (px, py) in positions]

def draw_pickups(surface, pickups, color=(120, 220, 255)):
    # Zeichnet alle Pixel auf die Map
    for r in pickups:
        surface.fill(color, r)

def collect_from_rects(player_rect, pickups, bank, per_pickup=1, sfx: pygame.mixer.Sound | None = None):
    # Wenn Player ein Pixel berührt, wird es eingesammelt und entfernt
    kept = []
    for r in pickups:
        if player_rect.colliderect(r):
            bank.add(per_pickup)  # Pixel zur Währung hinzufügen
            if sfx: sfx.play()    # Sound abspielen (optional)
        else:
            kept.append(r)        # Pixel bleibt auf der Map
    pickups[:] = kept             # Liste aktualisieren

# --- NEU: Immer 10 Pixel auf der Map halten ---
import random  # Für zufällige Positionen

MAP_WIDTH = 800    # Breite deiner Map (anpassen!)
MAP_HEIGHT = 600   # Höhe deiner Map (anpassen!)
PIXEL_SIZE = 12    # Größe der Pixel
ANZAHL_PICKUPS = 10  # Immer 10 Pixel auf der Map

def spawn_random_pixel(size=PIXEL_SIZE):
    # Erzeugt ein Rechteck an einer zufälligen Position
    x = random.randint(0, MAP_WIDTH - size)
    y = random.randint(0, MAP_HEIGHT - size)
    return pygame.Rect(x, y, size, size)

# Am Anfang: 10 Pixel zufällig erzeugen
pickups = [spawn_random_pixel() for _ in range(ANZAHL_PICKUPS)]

def collect_and_respawn(player_rect, pickups, bank, per_pickup=1, sfx: pygame.mixer.Sound | None = None):
    # Wenn Player ein Pixel einsammelt, wird sofort ein neues Pixel an einer neuen zufälligen Position erzeugt
    kept = []
    for r in pickups:
        if player_rect.colliderect(r):
            bank.add(per_pickup)      # Pixel zur Währung hinzufügen
            if sfx: sfx.play()        # Sound abspielen (optional)
            kept.append(spawn_random_pixel())  # Neues Pixel spawnen
        else:
            kept.append(r)            # Pixel bleibt auf der Map
    pickups[:] = kept                 # Liste aktualisieren