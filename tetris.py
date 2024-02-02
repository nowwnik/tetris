import pygame

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

figure = figures[1]

while True:
    dx = 0

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx = 1
            elif event.type == pygame.K_LEFT:
                dx = -1

        # move
    for i in range(4):
        figure[i].x += dx

    # draw grid
    [pygame.draw.rect(screen, (40, 40, 40), i, 1) for i in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(screen, (255, 255, 255), figure_rect)

    pygame.display.flip()
    clock.tick()
