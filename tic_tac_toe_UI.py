import pygame



def display_grid_tic_tac(win, w, h):
    background_img = pygame.image.load("images/grid_cell.png").convert_alpha()
    win.fill((0, 0, 0))
    x_pos = 0
    y_pos = 0
    i = 0
    for y in range(0, h):
        for x in range(0, w):
            win.blit(background_img, (x_pos, y_pos))
            i += 1
            x_pos += 100
        y_pos += 100
        x_pos = 0


def display_players_win(win, state, w, h, sp, surface):
    playerX_img = pygame.image.load("images/X.png").convert_alpha()
    playerO_img = pygame.image.load("images/O.png").convert_alpha()
    playerX_img = pygame.transform.scale(playerX_img, (40, 40))
    playerO_img = pygame.transform.scale(playerO_img, (40, 40))

    game_map = sp[0][state]

    for i, x in enumerate(game_map):
        for j, y in enumerate(x):
            if y == [0, 1, 0]:
                surface.blit(playerX_img, (j * 100 + 30, i * 100 + 30))
            elif y == [0, 0, 1]:
                surface.blit(playerO_img, (j * 100 + 30, i * 100 + 30))
    pygame.display.flip()

def display_win(win, winner, state, sp):
    background_img = pygame.image.load("images/grid_cell.png").convert_alpha()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    if winner == 0:
        textsurface = myfont.render("Player X Wins !", True, (0, 0, 0))
    elif winner == 1:
        textsurface = myfont.render("Player O Wins !", True, (0, 0, 0))
    else:
        textsurface = myfont.render("Draw !", True, (0, 0, 0))

    surface_grid = pygame.Surface((300, 300))
    win.fill((200, 200, 200))
    # surface_grid.fill((255, 255, 255))
    x_pos = 0
    y_pos = 0
    i = 0
    for y in range(0, 3):
        for x in range(0, 3):
            surface_grid.blit(background_img, (x_pos, y_pos))
            i += 1
            x_pos += 100
        y_pos += 100
        x_pos = 0

    display_players_win(win, state, 3, 3, sp, surface_grid)
    surface_grid.set_alpha(80)

    win.blit(surface_grid, (0, 0))
    win.blit(textsurface, (50, 120))
    pygame.display.flip()


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

def display_players_2(win, game_map):
    playerX_img = pygame.image.load("images/X.png").convert_alpha()
    playerO_img = pygame.image.load("images/O.png").convert_alpha()
    playerX_img = pygame.transform.scale(playerX_img, (40, 40))
    playerO_img = pygame.transform.scale(playerO_img, (40, 40))

    for i, x in enumerate(game_map):
        for j, y in enumerate(x):
            if y == [0, 1, 0]:
                win.blit(playerX_img, (j * 100 + 30, i * 100 + 30))
            elif y == [0, 0, 1]:
                win.blit(playerO_img, (j * 100 + 30, i * 100 + 30))
    pygame.display.flip()