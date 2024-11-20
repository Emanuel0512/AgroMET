import pygame
from pygame.sprite import Sprite

from pygame.sprite import Group

class NPC(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)