import pygame.draw
from pygame import Rect, Surface

_rectangles = [
    Rect(0, 370, 210, 65),
    Rect(150, 150, 60, 220),
    Rect(210, 150, 160, 65),
    Rect(370, 150, 60, 350),
    Rect(430, 445, 240, 60),
    Rect(665, 300, 60, 200),
    Rect(730, 300, 370, 60),
    Rect(950, 230, 150, 135)
]


class BgShape:

    @staticmethod
    def check_collision(rect: Rect):
        return rect.collidelistall(_rectangles)

    @staticmethod
    def draw_rectangles(surface: Surface):
        for rect in _rectangles:
            pygame.draw.rect(surface, (0, 0, 0), rect, 5)
