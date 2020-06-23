import pygame
from settings import *
from pygame.math import Vector2 as vec
import random
import time

class Enemy:
    def __init__(self, app, pos, nb):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = vec(self.grid_pos.x * self.app.cell_width, self.grid_pos.y * self.app.cell_height)
        self.nb = nb
        self.color = self.get_color()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.speed = self.set_speed()
        self.target = None
        self.init_pos = vec(pos.x, pos.y)

    def update(self):
        
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()
        
        self.grid_pos[0] = (self.pix_pos[0] - self.app.cell_width // 2 ) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - self.app.cell_height // 2 ) // self.app.cell_height + 1

    def reset(self):
        start = time.time()
        self.grid_pos = vec(self.init_pos.x, self.init_pos.y)
        self.pix_pos = vec(self.grid_pos.x * self.app.cell_width, self.grid_pos.y * self.app.cell_height)
        self.color = self.get_color()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.speed = self.set_speed()
        self.target = None
        print(time.time() - start)

    def get_color(self):
        color = None
        if self.nb == 0:
            color = (43, 220, 250)
        if self.nb == 1:
            color = (197, 200, 27)
        if self.nb == 2:
            color = (189, 29, 29)
        if self.nb == 3:
            color = (215, 159, 33)
        return color

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color, (int(self.pix_pos.x + self.app.cell_width // 2) , int(self.pix_pos.y + self.app.cell_height // 2)) , int(self.app.cell_width // 2.3))


    def set_target(self):
        if self.personality == "fast" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)
            if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    def time_to_move(self):
        if self.pix_pos.x % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if self.pix_pos.y % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x = next_cell[0] - self.grid_pos[0]
        y = next_cell[1] - self.grid_pos[1]
        return vec(x, y)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(COLS)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < COLS and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "fast":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_random_direction(self):
        x = None
        y = None
        while True:
            nb = random.randint(0, 4)
            if nb == 0:
                x = 1
                y = 0
            if nb == 1:
                x = 0
                y = 1
            if nb == 2:
                x = -1
                y = 0
            if nb == 3:
                x = 0
                y = -1
            if nb == 4:
                x =  self.direction.x
                y =  self.direction.y
            next_pos = vec(self.grid_pos.x + x, self.grid_pos.y + y)
            if next_pos not in self.app.walls:
                break
        return vec(x, y)


    def set_speed(self):
        if self.nb == 0:
            return 2
        if self.nb == 1:
            return 1
        if self.nb == 2:
            return 1
        return 2    

    def set_personality(self):
        if self.nb == 0:
            return "fast"
        if self.nb == 1:
            return "slow"
        if self.nb == 2:
            return "random"
        return "scared"