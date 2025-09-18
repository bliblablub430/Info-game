import pygame

def draw_coords(surface, rect):
    """Zeigt die Koordinaten eines Rects unten links an."""
    font = pygame.font.Font(None, 20)
    color = (255, 255, 255)
    bg_color = (0, 0, 0, 120)
    pad = 6

    text = f"xc: {int(rect.x)}  yc: {int(rect.y)}"
    txt = font.render(text, True, color)
    rect_txt = txt.get_rect()
    rect_txt.bottomleft = (0, surface.get_height())

    bg_rect = pygame.Rect(0, 0, rect_txt.width + pad * 2, rect_txt.height + pad * 2)
    bg_rect.bottomleft = (rect_txt.left - pad, rect_txt.bottom + pad)
    bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    bg_surf.fill(bg_color)
    surface.blit(bg_surf, bg_rect.topleft)

    surface.blit(txt, rect_txt.topleft)