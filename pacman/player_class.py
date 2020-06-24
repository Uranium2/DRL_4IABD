import pygame
from pygame.math import Vector2 as vec
from settings import *

class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = vec(self.grid_pos.x * self.app.cell_width, self.grid_pos.y * self.app.cell_height)
        self.direction = vec(-1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.god_mode_timer = 0

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.pix_pos.x  % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                if self.stored_direction != None:
                    self.direction = self.stored_direction
                self.able_to_move = self.can_move()
        
        if self.pix_pos.y  % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                if self.stored_direction != None:
                    self.direction = self.stored_direction
                self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()
        if self.on_food():
            self.eat_food()

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_pos.x) + self.app.cell_width // 2, int(self.pix_pos.y) + self.app.cell_height // 2), self.app.cell_width // 3)
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0] * self.app.cell_width,
        #     self.grid_pos[1] * self.app.cell_height,
        #     self.app.cell_width,
        #     self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            return True
        return False
    
    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def on_food(self):
        if self.grid_pos in self.app.food:
            return True
        return False
    
    def eat_food(self):
        self.app.food.remove(self.grid_pos)
        self.current_score += 10
        self.app.god_mode = True
        self.app.god_mode_timer = 240
        self.app.god_trigger = True


    def move(self, direction):
        self.stored_direction = direction

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True