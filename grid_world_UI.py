
import pygame
def display_grid(win, h, w):
    background_img = pygame.image.load("images/grid_cell.png").convert_alpha()
    win.fill((0, 0, 0))
    x_pos = 0
    y_pos = 0
    for y in range(0, h):
        for x in range(0, w):
            win.blit(background_img, (y_pos, x_pos))
            x_pos += 100
        y_pos += 100
        x_pos = 0


def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()


def display_mouse(win, st, w, h):
    cheese_img = pygame.image.load("images/mouse.png").convert_alpha()
    cheese_img = pygame.transform.scale(cheese_img, (40, 40))

    win.blit(cheese_img, ((st // w) * 100 + 30, (st % h) * 100 + 30))
    pygame.display.flip()

def display_reward(win, rewards, w, h):
    cheese_img = pygame.image.load("images/cheese.png").convert_alpha()
    cheese_img = pygame.transform.scale(cheese_img, (30, 30))

    cheese2_img = pygame.image.load("images/cheese2.png").convert_alpha()
    cheese2_img = pygame.transform.scale(cheese2_img, (30, 30))

    cheese3_img = pygame.image.load("images/cheese3.png").convert_alpha()
    cheese3_img = pygame.transform.scale(cheese3_img, (30, 30))

    poison_img = pygame.image.load("images/poison.png").convert_alpha()
    poison_img = pygame.transform.scale(poison_img, (30, 30))
    for r in rewards:
        if r[1] == 1:
            win.blit(cheese_img, ((r[0] // w) * 100 + 35, (r[0] % h) * 100 + 35))
        if r[1] == -1:
            win.blit(poison_img, ((r[0] // w) * 100 + 35, (r[0] % h) * 100 + 35))


