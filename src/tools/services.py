from typing import Union, Tuple

import pygame


def get_built_towers(towers: list) -> list:
    t = towers.copy()
    t.pop()
    return t


def draw_text(win: pygame.Surface, idx: int, text: str, color: Union[Tuple[int, int, int], str]='#ffffff'):
    font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 18)
    message = font.render(text, True, color)
    win.blit(message, (10, 30 * idx + 5))
