import pygame
# to use Sprites (images) like rect objects (to adapt to the rest of the code)
class Sprites(pygame.sprite.Sprite):
    def __init__(self, image_path, rect):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = rect #give rect attributes to sprites
        