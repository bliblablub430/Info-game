import pygame

surface = pygame.display.set_mode((1920, 1080))

sx = 1900
sy = 1000
max_lives = 3

def draw_shop_icon(surface, sx, sy, size=200):
    # Shop Symbol unten rechts zeichnen
    icon_surface = pygame.Surface((size, size))
    icon_surface.fill((255, 220, 0))  # Gelbe Farbe

    # Text "SHOP" rendern
    font = pygame.font.Font(None, size-150)
    text_surface = font.render("SHOP", True, (255, 255, 255))

    # Positionen für rechts unten berechnen
    total_width = size + 5 + text_surface.get_width()
    total_height = max(size, text_surface.get_height())

    icon_x = sx - total_width
    icon_y = sy - total_height

    text_x = icon_x
    text_y = sy - icon_surface.get_height()

    # Icon und Text zeichnen
    surface.blit(icon_surface, (icon_x, icon_y))
    surface.blit(text_surface, (text_x, text_y))

# shop_system.py — kleines Shop Menü (Pixels -> Sprint / +1 Herz)
from herz_system import gain_life

class Shop:
    # Shop Klasse
    def __init__(self):
        self.open = False  # Shop geschlossen
        self.sel = 0       # Auswahl Index
        self.items = [
            {"id": "sprint", "name": "Sprint freischalten", "cost": 15},
            {"id": "life",   "name": "+1 Herz",            "cost": 8},
        ]
        # Schriftarten vorbereiten
        pygame.font.init()
        self.font  = pygame.font.Font(None, 32)
        self.small = pygame.font.Font(None, 24)

    def toggle(self):
        # Shop öffnen oder schließen
        self.open = not self.open

    def handle_event(self, event, bank, lives, max_lives, sprint_unlocked):
        """Verarbeitet Tasten, wenn Shop offen ist. Gibt (lives, sprint_unlocked, msg) zurück."""
        msg = ""
        if not self.open or event.type != pygame.KEYDOWN:
            return lives, sprint_unlocked, msg

        # Auswahl nach oben bewegen
        if event.key in (pygame.K_UP, pygame.K_w):
            self.sel = (self.sel - 1) % len(self.items)
        # Auswahl nach unten bewegen
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.sel = (self.sel + 1) % len(self.items)
        # Kauf bestätigen
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            it = self.items[self.sel]
            # Prüfen ob genug Pixels vorhanden sind
            if not bank.spend(it["cost"]):
                msg = "Zu wenig Pixels!"
            else:
                # +1 Herz kaufen
                if it["id"] == "life":
                    lives = gain_life(lives, max_lives=max_lives)
                    msg = "+1 Herz gekauft"
                # Sprint freischalten
                elif it["id"] == "sprint":
                    if sprint_unlocked:
                        msg = "Sprint schon frei"
                    else:
                        sprint_unlocked = True
                        msg = "Sprint freigeschaltet (Shift halten)"
        # Shop schließen
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            self.open = False

        return lives, sprint_unlocked, msg

    def draw(self, surface, bank):
        """Zeichnet das Shop Fenster, wenn offen."""
        if not self.open:
            return

        w, h = surface.get_size()
        pw, ph = 420, 220
        panel = pygame.Rect((w - pw) // 2, (h - ph) // 2, pw, ph)

        # Hintergrund und Rahmen zeichnen
        pygame.draw.rect(surface, (20, 22, 28), panel)
        pygame.draw.rect(surface, (90, 100, 120), panel, 2)

        # Titel "SHOP" zeichnen
        title = self.font.render("SHOP", True, (255, 255, 0))
        surface.blit(title, (panel.x + 16, panel.y + 12))

        # Items auflisten
        y = panel.y + 60
        for i, it in enumerate(self.items):
            line = f"{it['name']}  -  {it['cost']} px"
            col = (255, 255, 255) if i == self.sel else (200, 200, 200)
            txt = self.small.render(line, True, col)
            surface.blit(txt, (panel.x + 24, y))
            # Auswahlpunkt zeichnen
            if i == self.sel:
                pygame.draw.circle(surface, (255, 255, 0), (panel.x + 10, y + 10), 4)
            y += 30

        # Pixel-Anzeige und Hinweistext zeichnen
        bal  = self.small.render(f"Pixels: {bank.get()}", True, (0, 255, 140))
        hint = self.small.render("↑/↓ wählen  Enter kaufen  Q schließen", True, (180, 180, 180))
        surface.blit(bal,  (panel.x + 24, panel.bottom - 48))
        surface.blit(hint, (panel.x + 24, panel.bottom - 28))
shop = Shop()