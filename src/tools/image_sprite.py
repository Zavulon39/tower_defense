import pygame.image
from pygame import Rect, Surface


class ImageSprite(Rect):

    def __init__(self, x: int, y: int, width: int, height: int, image_uri: str):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_uri)

    def set_image(self, image_uri: str):
        self.image = pygame.image.load(image_uri)

    def draw(self, surface: Surface):

        surface.blit(self.image, (self.x, self.y))
