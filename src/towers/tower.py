from typing import List, Callable
import pygame.image
from pygame import Surface
from src.enemies.enemy import Enemy
from src.tools.image_sprite import ImageSprite
from enum import Enum
from src.tools.timer import Timer

BASE_PATH = 'assets/towers/'
idx = 0


class TowerType(Enum):
    FIRE = 'FIRE'
    FOREST = 'FOREST'
    ICE = 'ICE'
    INFERNO = 'INFERNO'


class TowerImage(Enum):
    FIRE1 = BASE_PATH + 'fire1.png'
    ICE1 = BASE_PATH + 'ice1.png'
    FIRE2 = BASE_PATH + 'fire2.png'
    ICE2 = BASE_PATH + 'ice2.png'
    FIRE3 = BASE_PATH + 'fire3.png'
    ICE3 = BASE_PATH + 'ice3.png'


class Tower(ImageSprite):
    def __init__(self, x: int, y: int, type_: TowerType, image: TowerImage):
        global idx
        idx += 1

        self.level = 1
        self.has_build = False
        self.type = type_.value
        self.idx = idx

        if self.type == TowerType.FIRE.value:
            self.damage = .035
            self.cost = 50
            self.delay = 0
        if self.type == TowerType.ICE.value:
            self.damage = .5
            self.cost = 100
            self.delay = 30
            self.kill_num = 3

        width, height = pygame.image.load(image.value).get_size()
        self.raycast = ImageSprite(0, 0, 200, 200, 'assets/raycast.png')
        super().__init__(x, y, width, height, image.value)

    def draw(self, surface: Surface, mx=0, my=0, draw_raycast=False):
        if not self.has_build:
            self.update(mx - self.width // 2, my - self.height // 2, self.width, self.height)
            self.raycast.update(
                mx - self.raycast.width // 2,
                my - self.raycast.height // 2,
                self.raycast.width,
                self.raycast.height
            )
        elif draw_raycast:
            self.raycast.draw(surface)

        super(Tower, self).draw(surface)

    def attack_enemies(self, enemies: List[Enemy], surface: Surface, kill_callback: Callable):
        if self.type == TowerType.ICE.value:
            if Timer.get(self) % self.delay == 0:
                for i in self.raycast.collidelistall(enemies)[:self.kill_num]:
                    enemy = enemies[i]
                    if enemy.health <= 0:
                        kill_callback(enemy.prize)
                        return enemies.pop(i)
                    enemy.health -= self.damage
                    pygame.draw.line(surface, (0, 114, 255), start_pos=(self.x + self.width // 2, self.y),
                                     end_pos=(enemy.x + enemy.width // 2, enemy.y), width=7)
            return

        for i in self.raycast.collidelistall(enemies):
            enemy = enemies[i]
            if enemy.health <= 0:
                kill_callback(enemy.prize)
                return enemies.pop(i)
            if self.type == TowerType.FIRE.value:
                enemy.health -= self.damage
                return pygame.draw.line(surface, (255, 0, 0), start_pos=(self.x + self.width // 2, self.y),
                                        end_pos=(enemy.x + enemy.width // 2, enemy.y), width=5)

    def update_level(self):
        self.level += 1

        if self.level == 2:
            if self.type == TowerType.FIRE.value:
                self.damage = .05
                self.image = pygame.image.load(TowerImage.FIRE2.value)
                self.width, self.height = self.image.get_size()
            if self.type == TowerType.ICE.value:
                self.damage = .6
                self.delay = 25
                self.kill_num = 4
                self.image = pygame.image.load(TowerImage.ICE2.value)
                self.width, self.height = self.image.get_size()
        elif self.level == 3:
            if self.type == TowerType.FIRE.value:
                self.damage = .065
                self.image = pygame.image.load(TowerImage.FIRE3.value)
                self.width, self.height = self.image.get_size()
            if self.type == TowerType.ICE.value:
                self.damage = .7
                self.delay = 20
                self.kill_num = 5
                self.image = pygame.image.load(TowerImage.ICE3.value)
                self.width, self.height = self.image.get_size()

    def __hash__(self):
        return self.idx
