import pygame
from copy import deepcopy
from random import choice, randrange

H, W = 20, 10
TILE = 30
FPS = 30

Game_field = W * TILE, H * TILE

pygame.init()
screen = pygame.display.set_mode(Game_field)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, -1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

field = [[0 for i in range(W)] for j in range(H)]

figure = deepcopy(choice(figures))

anim_count, anim_speed, anim_lim = 0, 20, 2000


def borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


while True:
    dx = 0

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_DOWN:
                anim_lim = 100

    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not borders():
            figure = deepcopy(figure_old)
            break

    # falling
    anim_count += anim_speed
    if anim_count > anim_lim:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = pygame.color('white')
                figure = deepcopy(choice(figures))
                anim_lim = 2000
                break

    # draw grid
    [pygame.draw.rect(screen, (40, 40, 40), i, 1) for i in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(screen, (255, 255, 255), figure_rect)
    #draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x*TILE, y*TILE
                pygame.draw.rect(screen,col,figure_rect)

    pygame.display.flip()
    clock.tick()
