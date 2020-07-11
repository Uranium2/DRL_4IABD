from typing import Callable

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

def step_until_the_end_of_the_episode_and_return_history(
        T,
        S,
        P,
        s0: int,
        pi: np.ndarray,
        is_terminal_func: Callable,
        step_func: Callable,
        max_steps: int = 10
) -> \
        ([int], [int], [int], [float]):
    s_list = []
    a_list = []
    s_p_list = []
    r_list = []
    st = s0
    actions = np.arange(pi.shape[1])
    steps_count = 0
    while not is_terminal_func(st, T) and steps_count < max_steps:
        at = np.random.choice(actions, p=pi[st])
        st_p, rt_p, t = step_func(st, at, T, S, P)
        s_list.append(st)
        a_list.append(at)
        s_p_list.append(st_p)
        r_list.append(rt_p)
        st = st_p
        steps_count += 1
    return s_list, a_list, s_p_list, r_list

def step_until_the_end_of_the_episode_and_return_history_2(
        s_terminal,
        s_sp,
        player,
        st: int,
        pi: np.ndarray,
        is_terminal_func: Callable,
        step_func: Callable,
        max_steps: int = 10
) -> \
        ([int], [int], [int], [float]):
    s_list = []
    a_list = []
    s_p_list = []
    r_list = []
    actions = np.arange(pi.shape[1])
    steps_count = 0
    while not is_terminal_func(st, s_terminal) and steps_count < max_steps:
        at = np.random.choice(actions, p=pi[st])
        st_p, rt_p, t = step_func(st, at, s_terminal, s_sp, player)
        s_list.append(st)
        a_list.append(at)
        s_p_list.append(st_p)
        r_list.append(rt_p)
        st = st_p
        steps_count += 1
    return s_list, a_list, s_p_list, r_list
