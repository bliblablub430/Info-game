overlay = pygame.Surface(surface.get_size()) # Macht eine neue Fläche, so gross wie der Bildschirm
overlay.fill((200,0,0)) # Färbt die Fläche rot
surface.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD) # Legt die rote Fläche über das Bild