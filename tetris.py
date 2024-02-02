import pygame
from copy import deepcopy
from random import choice

H, W = 20, 10
TILE = 30
FPS = 30

Game_zone = W * TILE + 200, H * TILE

Game_field = W * TILE, H * TILE

pygame.init()

pygame.display.set_caption('Tetris')

BackGround = pygame.display.set_mode(Game_zone)
screen = pygame.Surface(Game_field)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

field = [[0 for i in range(W)] for j in range(H)]

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

anim_count, anim_speed, anim_lim = 0, 5, 4000

font = pygame.font.SysFont('Impact', 30)

title_score = font.render('score:', False, pygame.Color('white'))
title_next = font.render('next figure', False, pygame.Color('white'))
title_record = font.render('record:', False, pygame.Color('white'))
title_game_over = font.render('Game  restart  1  s', False, pygame.Color('white'))

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx = 0
    rotate = False
    BackGround.fill((0, 0, 0))
    BackGround.blit(screen, (0, 0))
    screen.fill((0, 0, 0))

    for i in range(lines):
        pygame.time.wait(200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                dx = 1
            elif event.key == pygame.K_a:
                dx = -1
            elif event.key == pygame.K_s:
                anim_lim = 400
            elif event.key == pygame.K_w:
                rotate = True

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
                for j in range(4):
                    field[figure_old[j].y][figure_old[j].x] = pygame.Color('white')
                figure = next_figure
                next_figure = deepcopy(choice(figures))
                anim_lim = 4000
                break

    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not borders():
                figure = deepcopy(figure_old)
                break

    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            # anim_speed += 3
            lines += 1

    score += scores[lines]
    # draw grid
    [pygame.draw.rect(screen, (40, 40, 40), i, 1) for i in grid]

    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(screen, (255, 255, 255), figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(screen, col, figure_rect)

    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 240
        figure_rect.y = next_figure[i].y * TILE + 130
        pygame.draw.rect(BackGround, (255, 255, 255), figure_rect)

    # titles
    BackGround.blit(title_next, (330, 80))
    BackGround.blit(title_score, (350, 300))
    BackGround.blit(font.render(str(score), False, pygame.Color('white')), (350, 340))
    BackGround.blit(title_record, (350, 460))
    BackGround.blit(font.render(record, False, pygame.Color('white')), (350, 500))

    # game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_lim = 0, 5, 4000
            score = 0

            BackGround.fill((0, 0, 0))
            BackGround.blit(title_game_over, (W * TILE / 2, H * TILE / 2 - 200))
            pygame.display.flip()

            pygame.time.wait(1200)

    pygame.display.flip()
    clock.tick()
