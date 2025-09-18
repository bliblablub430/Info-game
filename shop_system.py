import pygame

def draw_shop_icon(surface, sx, sy, size=20):
    # Create the icon surface
    icon_surface = pygame.Surface((size, size))
    icon_surface.fill((255, 220, 0))  # Yellow color

    # Render the text "SHOP"
    font = pygame.font.Font(None, size)
    text_surface = font.render("SHOP", True, (255, 255, 255))

    # Calculate positions to align bottom right
    total_width = size + 5 + text_surface.get_width()
    total_height = max(size, text_surface.get_height())

    icon_x = sx - total_width
    icon_y = sy - total_height

    text_x = icon_x + size + 5
    text_y = sy - text_surface.get_height()

    # Blit icon and text
    surface.blit(icon_surface, (icon_x, icon_y))
    surface.blit(text_surface, (text_x, text_y))

# shop_system.py — tiny menu shop (Pixels -> sprint / +1 heart)
from herz_system import gain_life

class Shop:
    def __init__(self):
        self.open = False
        self.sel = 0
        self.items = [
            {"id": "sprint", "name": "Sprint freischalten", "cost": 15},
            {"id": "life",   "name": "+1 Herz",            "cost": 8},
        ]
        # fonts
        pygame.font.init()
        self.font  = pygame.font.Font(None, 32)
        self.small = pygame.font.Font(None, 24)

    def toggle(self):
        self.open = not self.open

    def handle_event(self, event, bank, lives, max_lives, sprint_unlocked):
        """Process keys when shop is open. Returns (lives, sprint_unlocked, msg)."""
        msg = ""
        if not self.open or event.type != pygame.KEYDOWN:
            return lives, sprint_unlocked, msg

        if event.key in (pygame.K_UP, pygame.K_w):
            self.sel = (self.sel - 1) % len(self.items)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.sel = (self.sel + 1) % len(self.items)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            it = self.items[self.sel]
            if not bank.spend(it["cost"]):
                msg = "Zu wenig Pixels!"
            else:
                if it["id"] == "life":
                    lives = gain_life(lives, max_lives=max_lives)
                    msg = "+1 Herz gekauft"
                elif it["id"] == "sprint":
                    if sprint_unlocked:
                        msg = "Sprint schon frei"
                    else:
                        sprint_unlocked = True
                        msg = "Sprint freigeschaltet (Shift halten)"
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            self.open = False

        return lives, sprint_unlocked, msg

    def draw(self, surface, bank):
        """Draws the shop overlay when open."""
        if not self.open:
            return

        w, h = surface.get_size()
        pw, ph = 420, 220
        panel = pygame.Rect((w - pw) // 2, (h - ph) // 2, pw, ph)

        pygame.draw.rect(surface, (20, 22, 28), panel)
        pygame.draw.rect(surface, (90, 100, 120), panel, 2)

        title = self.font.render("SHOP", True, (255, 255, 0))
        surface.blit(title, (panel.x + 16, panel.y + 12))

        y = panel.y + 60
        for i, it in enumerate(self.items):
            line = f"{it['name']}  -  {it['cost']} px"
            col = (255, 255, 255) if i == self.sel else (200, 200, 200)
            txt = self.small.render(line, True, col)
            surface.blit(txt, (panel.x + 24, y))
            if i == self.sel:
                pygame.draw.circle(surface, (255, 255, 0), (panel.x + 10, y + 10), 4)
            y += 30

        bal  = self.small.render(f"Pixels: {bank.get()}", True, (0, 255, 140))
        hint = self.small.render("↑/↓ wählen  Enter kaufen  Q schließen", True, (180, 180, 180))
        surface.blit(bal,  (panel.x + 24, panel.bottom - 48))
        surface.blit(hint, (panel.x + 24, panel.bottom - 28))