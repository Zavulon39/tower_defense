from enum import Enum
import pygame.image
from pygame import Surface
from src.tools.image_sprite import ImageSprite

BASE_PATH = 'assets/enemies/'
health_ending = 0


class EnemyType(Enum):
    GHOST = 'GHOST'


class Enemy(ImageSprite):

    def __init__(self, x: int, y: int, type_: EnemyType, wave: int):
        self.type = type_.value
        self.speed = 2 if wave % 10 == 0 else 1

        if self.type == EnemyType.GHOST.value:
            self.health = 10 + health_ending
            self.initial_health = 10 + health_ending
            self.prize = 10

        image_uri = BASE_PATH + self.type.lower() + '.png'
        width, height, = pygame.image.load(image_uri).get_size()
        super().__init__(x, y, width, height, image_uri)

    @classmethod
    def get_enemy(cls, x: int, y: int, type_: EnemyType, idx: int, wave: int):
        e = cls(x, y, type_, wave)
        e.x -= e.width * idx
        e.x -= e.width * idx // 3
        return e

    def draw(self, surface: Surface):
        if self.x < 150:
            self.x += self.speed
        elif 150 <= self.x <= 170 and self.y > 150:
            self.y -= self.speed
        elif 150 <= self.y <= 170 and self.x < 380:
            self.x += self.speed
        elif 379 <= self.x <= 400 and self.y < 445:
            self.y += self.speed
        elif 444 <= self.y <= 470 and self.x < 660:
            self.x += self.speed
        elif 659 <= self.x <= 670 and self.y > 300:
            self.y -= self.speed
        elif 299 <= self.y <= 320:
            self.x += self.speed

        super().draw(surface)
        self.draw_hitbox(surface)

    def draw_hitbox(self, surface: Surface):
        pygame.draw.rect(surface, (33, 36, 37), (self.x, self.y - 15, self.width, 10))
        pygame.draw.rect(surface, (255, 0, 46),
                         (self.x, self.y - 15, (self.health / self.initial_health) * self.width, 10))


class EnemyManager:

    @staticmethod
    def get_enemies(wave: int):
        global health_ending

        if wave % 5 == 0:
            health_ending += 1

        return [Enemy.get_enemy(-60, 370, EnemyType.GHOST, i, wave) for i in range(wave)]
