from typing import List
import pygame
from src.bg_shape import BgShape
from src.enemies.enemy import EnemyManager, Enemy
from src.tools.console_color import RainbowPrint, ConsoleColor
from src.tools.image_sprite import ImageSprite
from src.tools.services import get_built_towers, draw_text
from src.tools.timer import Timer
from src.towers.tower import Tower, TowerType, TowerImage

pygame.init()

W, H = 1100, 733

win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Tower Defence')
pygame.mouse.set_visible(False)

bg = pygame.image.load('assets/bg.png')
menu = pygame.image.load('assets/menu.jpg')
game_over = pygame.sprite.Sprite()
game_over.image = pygame.image.load('assets/gameover.png')
game_over.rect = game_over.image.get_rect()
game_over.rect.x = -W
castle = ImageSprite(940, 230, 150, 135, 'assets/castle.png')
cursor = ImageSprite(0, 0, 30, 33, 'assets/cursor.png')
circle = ImageSprite(0, 0, 200, 200, 'assets/circle.png')
btn_start_wave = ImageSprite(W - 210, 10, 200, 67, 'assets/button.png')
collision_circle = pygame.Rect(0, 0, 100, 100)
wave = 0
money = 100
health = 100
draw_circle = False
draw_raycast = False
has_collision = False

towers: List[Tower] = []
enemies: List[Enemy] = []


def run_wave():
    global wave
    wave += 1
    enemies.extend(EnemyManager.get_enemies(wave))


def increase_money(amount: int):
    global money
    money += amount


while True:
    mx, my = pygame.mouse.get_pos()

    if health <= 0:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        win.fill((163, 121, 79))
        win.blit(bg, (0, 0))
        win.blit(menu, (430, 5))
        castle.draw(win)
        pygame.draw.rect(win, (33, 36, 37), (castle.x, castle.y - 15, castle.width, 10))
        pygame.draw.rect(win, (255, 0, 46),
                         (castle.x, castle.y - 15, (health / 100) * castle.width, 10))

        for enemy in enemies:
            enemy.draw(win)

        for tower in towers:
            tower.draw(win, mx, my, draw_raycast)

        win.blit(game_over.image, game_over.rect)

        if game_over.rect.x != 0:
            game_over.rect.x += 50

        pygame.display.flip()

        continue

    pygame.time.delay(15)
    Timer.tick()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if btn_start_wave.collidepoint(mx, my):  # and not enemies
                    run_wave()
            elif e.button == 2:
                for i, t in enumerate(towers):
                    if t.collidepoint(mx, my) and money - t.cost >= 0 and t.has_build and t.level < 3:
                        money -= t.cost
                        t.update_level()
                        break
            elif e.button == 3:
                for i, t in enumerate(towers):
                    if t.collidepoint(mx, my) and t.has_build:
                        money += t.cost // 2 * t.level
                        towers.pop(i)
                        break
            if e.button == 1 and draw_circle and not has_collision:
                towers[-1].has_build = True
                money -= towers[-1].cost
                draw_circle = False
                Timer.add(towers[-1])

        elif e.type == pygame.KEYDOWN:
            if e.unicode == '1':
                if not draw_circle:
                    t = Tower(mx, my, TowerType.FIRE, TowerImage.FIRE1)
                    if money - t.cost >= 0:
                        towers.append(t)
                        draw_circle = True
            if e.unicode == '2':
                if not draw_circle:
                    t = Tower(mx, my, TowerType.ICE, TowerImage.ICE1)
                    if money - t.cost >= 0:
                        towers.append(t)
                        draw_circle = True
            elif e.unicode == '\x1b':
                draw_circle = False
                if len(towers) and not towers[-1].has_build:
                    towers.pop(-1)
            elif e.unicode == '\t':
                draw_raycast = True
            elif e.unicode == '\r':
                run_wave()
        elif e.type == pygame.KEYUP:
            if e.unicode == '\t':
                draw_raycast = False

    for i in castle.collidelistall(enemies):
        enemies.pop(i)
        health -= 10

    win.fill((163, 121, 79))
    win.blit(bg, (0, 0))
    win.blit(menu, (430, 5))
    btn_start_wave.draw(win)
    castle.draw(win)
    pygame.draw.rect(win, (33, 36, 37), (castle.x, castle.y - 15, castle.width, 10))
    pygame.draw.rect(win, (255, 0, 46),
                     (castle.x, castle.y - 15, (health / 100) * castle.width, 10))

    for enemy in enemies:
        enemy.draw(win)

    for tower in towers:
        tower.draw(win, mx, my, draw_raycast)
        if tower.has_build:
            tower.attack_enemies(enemies, win, increase_money)

    if draw_circle:
        circle.update(mx - circle.width // 2, my - circle.height // 2, circle.width, circle.height)
        collision_circle.update(
            mx - collision_circle.width // 2,
            my - collision_circle.height // 2,
            collision_circle.width,
            collision_circle.height
        )

        draw_text(win, 0, f'Wave: {wave}')
        draw_text(win, 1, f'Money: {money}')

        circle.draw(win)

        if BgShape.check_collision(collision_circle) or collision_circle.collidelistall(get_built_towers(towers)):
            has_collision = True
            circle.set_image('assets/circle_red.png')
        else:
            has_collision = False
            circle.set_image('assets/circle.png')
    else:
        cursor.update(mx - cursor.width // 2, my - cursor.height // 2, cursor.width, cursor.height)

        draw_text(win, 0, f'Wave: {wave}')
        draw_text(win, 1, f'Money: {money}')

        if pygame.mouse.get_focused():
            cursor.draw(win)

    pygame.display.update()
