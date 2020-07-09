import numpy as np
import pygame


def is_terminal(state: int, T) -> bool:
    return state in T

def tabular_uniform_random_policy(space_size: int, action_size: int):
    return np.ones((space_size, action_size)) / action_size

def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
