# Pixel-Währung + Sammeln + HUD
import pygame

# Wallet (Währung)
class PixelBank:
    def __init__(self, start=0):
        self.amount = int(start)

    def add(self, n=1):
        self.amount += max(0, int(n))

    def can_spend(self, n):
        return self.amount >= int(n)

    def spend(self, n):
        n = int(n)
        if self.can_spend(n):
            self.amount -= n
            return True
        return False

    def get(self):
        return self.amount

# HUD: Anzeige oben rechts/links 
def draw_pixels(surface, x, y, amount, size=16, gap=6):
    # kleines "Pixel"-Icon (einfarbiges Quadrat)
    icon = pygame.Surface((size, size))
    icon.fill((120, 220, 255))  # hellblau = Pixel
    surface.blit(icon, (x, y))

    font = pygame.font.Font(None, size + 8)
    text = font.render(f"x {amount}", True, (255, 255, 255))
    surface.blit(text, (x + size + gap, y))

#  Sammelbare Pixel
def make_pickup_rects(positions, size=12):
   # Erzeugt kleine Rechtecke an Positionen [(x,y), ...]
    return [pygame.Rect(px, py, size, size) for (px, py) in positions]

def draw_pickups(surface, pickups, color=(120, 220, 255)):
    for r in pickups:
        surface.fill(color, r)

def collect_from_rects(player_rect, pickups, bank, per_pickup=1, sfx: pygame.mixer.Sound | None = None):
    # Wenn Player einsammeln -> Pixel add + Rechteck entfernen (in-place).
    kept = []
    for r in pickups:
        if player_rect.colliderect(r):
            bank.add(per_pickup)
            if sfx: sfx.play()
        else:
            kept.append(r)
    pickups[:] = kept