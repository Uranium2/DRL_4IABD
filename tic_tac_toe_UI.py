import pygame


def display_grid_tic_tac(win, w, h):
    background_img = pygame.image.load("images/grid_cell.png").convert_alpha()
    win.fill((0, 0, 0))
    x_pos = 0
    y_pos = 0
    #myfont = pygame.font.SysFont('Comic Sans MS', 15)
    i = 0
    for y in range(0, h):
        for x in range(0, w):
            win.blit(background_img, (x_pos, y_pos))
            #textsurface = myfont.render(str(i), False, (0, 0, 0))
            #win.blit(textsurface, (x_pos + 2, y_pos + 2))
            i += 1
            x_pos += 100
        y_pos += 100
        x_pos = 0

def display_players(win, state, w, h, sp):
    playerX_img = pygame.image.load("images/X.png").convert_alpha()
    playerO_img = pygame.image.load("images/O.png").convert_alpha()
    playerX_img = pygame.transform.scale(playerX_img, (40, 40))
    playerO_img = pygame.transform.scale(playerO_img, (40, 40))

    game_map = sp[0][state]

    for i, x in enumerate(game_map):
        for j, y in enumerate(x):
            if y == [0, 1, 0]:
                win.blit(playerX_img, (j * 100 + 30, i * 100 + 30))
            elif y == [0, 0, 1]:
                win.blit(playerO_img, (j * 100 + 30, i * 100 + 30))
    pygame.display.flip()