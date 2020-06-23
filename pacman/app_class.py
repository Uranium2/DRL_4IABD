import pygame
from settings import *
import sys
from player_class import *
from enemy_class import *
from pygame.math import Vector2 as vec

pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "playing"
        self.cell_width = WIDTH // COLS
        self.cell_height = HEIGHT// ROWS
        with open(FOLDER_PATH + "/high_score.txt") as f:
            self.high_score = int(f.readline())
        self.walls = []
        self.coins = []
        self.enemies_pos = []
        self.food = []
        self.player_pos = None
        self.load() #charge img walls, coins, enemies and player pos
        self.player = Player(self, self.player_pos)
        self.enemies = self.make_enemies()
        self.god_mode_timer = 0
        self.god_trigger = False

    def run(self):
        while self.running:
            if self.state == "playing":
                self.clock.tick(FPS)
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
    
    def load(self):
        self.background = pygame.image.load(FOLDER_PATH + '/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        with open(FOLDER_PATH + "/walls.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(x, y))
                    elif char == "C":
                        self.coins.append(vec(x, y))
                    elif char == "P":
                        self.player_pos = vec(x, y)
                    elif char in ["2", "3", "4", "5"]:
                        self.enemies_pos.append(vec(x, y))
                    elif char == "F":
                        self.food.append(vec(x, y))

    def make_enemies(self):
        list_en = []
        for i, pos in enumerate(self.enemies_pos):
            list_en.append(Enemy(self, pos, i))
        return list_en

    def draw_cells(self, list_items, color):
        for item in list_items:
            pygame.draw.rect(self.screen, color, (item.x * self.cell_width, item.y * self.cell_height, self.cell_width, self.cell_height))
        
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.screen, GRAY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.screen, GRAY, (0, x * self.cell_height), (WIDTH,  x * self.cell_height))
        
        self.draw_cells(self.walls, GRAY)
        self.draw_cells(self.coins, YELLOW)

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (125, 125, 10),
                               (int(coin.x * self.cell_width) + self.cell_width // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2),
                                4)
    def draw_food(self):
        for f in self.food:
            pygame.draw.circle(self.screen, RED,
                               (int(f.x * self.cell_width) + self.cell_width // 2,
                                int(f.y * self.cell_height) + self.cell_height // 2),
                                4)

    def draw_text(self, msg, screen, position, size, color, font_name, center=False):
        font = pygame.font.SysFont(font_name, size)
        msg = font.render(msg, False, color)
        msg_size = msg.get_size()
        if center:
            position[0] = position[0] - msg_size[0] / 2
            position[1] = position[1] - msg_size[1] / 2
        screen.blit(msg, position)

    def playing_events(self):

        ## ICI FAIRE l'INTERFACE AVEC l'IA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))


        
    def playing_update(self):
        pygame.event.pump()
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos and self.god_mode_timer == 0:
                self.update_high_score()
                self.reset_game()
            if enemy.grid_pos == self.player.grid_pos and self.god_mode_timer >= 0:
                print("Eating ennemy")
                enemy.reset()
        
        if self.god_mode_timer > 0:
            self.god_mode_timer -= 1


        if self.god_mode_timer > 0 and self.god_trigger:
            for enemy in self.enemies:
                enemy.personality = "scared"
                enemy.color = BLUE
        elif self.god_mode_timer == 0 and self.god_trigger:
            self.god_trigger = False
            for enemy in self.enemies:
                enemy.personality = enemy.set_personality()
                enemy.color = enemy.get_color()

    def update_high_score(self):
        with open(FOLDER_PATH + "/high_score.txt") as f:
            high_score_file = int(f.readline())
        if high_score_file < self.player.current_score:
            with open(FOLDER_PATH + "/high_score.txt", "w") as f:
                f.write(str(self.player.current_score))



    def reset_game(self):
        with open(FOLDER_PATH + "/high_score.txt") as f:
            self.high_score = f.readline()
        self.walls = []
        self.coins = []
        self.enemies_pos = []
        self.player_pos = None
        self.load()
        self.player = Player(self, self.player_pos)
        self.enemies = self.make_enemies()
        self.state == "playing"
        self.god_mode_timer = 0
        self.god_trigger = False

    def playing_draw(self):
        self.screen.blit(self.background, (0,0))
        # self.draw_grid()
        self.draw_coins()
        self.draw_food()
        self.draw_text("SCORE {}".format(self.player.current_score), self.screen, [0, 0], TEXT_SIZE, (255, 255, 255), FONT)
        self.draw_text("HIGH SCORE {}".format(self.high_score), self.screen, [WIDTH - 300, 0], TEXT_SIZE, (255, 255, 255), FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()