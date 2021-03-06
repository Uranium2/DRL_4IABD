import pygame

def display_line(win, num_states):
    background_img = pygame.image.load("images/grid_cell.png").convert_alpha()
    win.fill((0, 0, 0))
    x_pos = 0
    for y in range(0, num_states):
        win.blit(background_img, (x_pos, 0))
        x_pos += 100



def display_mouse_line(win, st, num_states):
    cheese_img = pygame.image.load("images/mouse.png").convert_alpha()
    cheese_img = pygame.transform.scale(cheese_img, (40, 40))

    win.blit(cheese_img, (st * 100 + 30, 35))
    pygame.display.flip()

def display_reward_line(win, rewards, num_states):
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
            win.blit(cheese_img, (r[0] * 100 + 35, 35))
        if r[1] == -1:
            win.blit(poison_img, (r[0] * 100 + 35, 35))


