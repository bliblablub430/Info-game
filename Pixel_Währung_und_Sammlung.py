# Pixel-Währung + Sammeln + HUD  (Mithilfe von Chatgpt und Copilot)
import pygame

surface = pygame.display.set_mode((150, 100))
hudx = 250
hudy = 100

# Wallet (Währung) – speichert, wie viele Pixel du hast
class PixelBank:  
    def __init__(self, start=50):
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

# HUD: Anzeige oben rechts/links # von Chatgpt
def menu(surface, hudx, hudy, amount, size=150, gap=6):
    # kleines "Pixel"-Icon (einfarbiges Quadrat)
    icon = pygame.Surface((size + 50, size))
    icon.fill((120, 220, 255))  # hellblau = Pixel
    surface.blit(icon, (hudx, hudy))

    font = pygame.font.Font(None, size + 8)
    text = font.render(f"x {amount}", True, (0, 0, 0))
    surface.blit(text, (hudx - gap, hudy))