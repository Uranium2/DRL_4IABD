
import pygame
def display_grid(win, w, h):
    background_img = pygame.image.load("images/grid_cell.png").convert_alpha()
    win.fill((0, 0, 0))
    x_pos = 0
    y_pos = 0
    myfont = pygame.font.SysFont('Comic Sans MS', 15)
    i = 0
    for y in range(0, h):
        for x in range(0, w):
            win.blit(background_img, (x_pos, y_pos))
            textsurface = myfont.render(str(i), False, (0, 0, 0))
            win.blit(textsurface, (x_pos + 2, y_pos + 2))
            i += 1
            x_pos += 100
        y_pos += 100
        x_pos = 0



def display_mouse_grid(win, st, w, h):
    mouse_img = pygame.image.load("images/mouse.png").convert_alpha()
    mouse_img = pygame.transform.scale(mouse_img, (40, 40))

    win.blit(mouse_img, ((st % w) * 100 + 30, (st // w) * 100 + 30))
    pygame.display.flip()

def display_reward_grid(win, rewards, w, h):
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
            win.blit(cheese_img, ((r[0] % w) * 100 + 35, (r[0] // w) * 100 + 35))
        if r[1] == -1:
            win.blit(poison_img, ((r[0] % w) * 100 + 35, (r[0] // w) * 100 + 35))


