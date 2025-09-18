import pygame

class Sprites(pygame.sprite.Sprite):
    def __init__(self, image_path, rect):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = rect