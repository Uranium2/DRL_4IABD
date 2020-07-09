from time import sleep

import pygame

from algo import iterative_policy_evaluation, policy_iteration
from common_func import tabular_uniform_random_policy, is_terminal, event_loop
from grid_world import create_grid_world, step, reset_grid
from grid_world_UI import display_grid, display_reward_grid, display_mouse_grid

from line_world import create_line_world, reset_line
from line_world_UI import display_line,  display_reward_line, display_mouse_line


def test_line_iterative_policy_evaluation():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)
    Pi = tabular_uniform_random_policy(S.shape[0], A.shape[0])

    V = iterative_policy_evaluation(S, A, P, T, Pi)
    print(V)


    win = pygame.display.set_mode((num_states * 100, 100))

    st = reset_line(num_states)

    while not is_terminal(st, T):
        display_line(win, num_states)
        event_loop()
        display_reward_line(win, rewards, num_states)
        display_mouse_line(win, st, num_states)
        sleep(1)

        if V[st + 1] > V[st - 1] or V[st + 1] == 0:
            a = 1
        elif V[st + 1] <  V[st - 1] or V[st - 1] == 0:
            a = 0
        st, r, term = step(st, a, T, S, P)

    display_line(win, num_states)
    display_reward_line(win, rewards,num_states)
    display_mouse_line(win, st, num_states)
    sleep(1)

def test_grid_iterative_policy_evaluation():
    pygame.init()

    w = 6
    h = 5
    rewards = ((24, 1),
               (2, -1),
               (11, -1))

    terminal = [2, 11, 24]
    new_pos = {"top": 2, "bot": 3, "left": 0, "right": 1}

    S, A, T, P = create_grid_world(w, h, rewards, terminal)
    Pi = tabular_uniform_random_policy(S.shape[0], A.shape[0])

    V = iterative_policy_evaluation(S, A, P, T, Pi)


    win = pygame.display.set_mode((w * 100, h * 100))
    for i in range(w * h):
        if i % w == 0 and i != 0:
            print("")
        print(round(V[i], 7), end=" ")
    print("")
    st = reset_grid(w, h)

    while not is_terminal(st, T):
        display_grid(win, w, h)
        event_loop()
        display_reward_grid(win, rewards, w, h)
        display_mouse_grid(win, st, w, h)
        sleep(1)
        print("st " + str(st))

        positions = {"top": st - w,
                "bot": st + w,
                "left": st - 1,
                "right": st + 1
                }

        positions = {key: V[value] for key, value in positions.items() if 0 <= value < w * h}
        action = max(positions, key=positions.get)

        a = new_pos[action]

        st, r, term = step(st, a, T, S, P)
    display_grid(win, w, h)
    display_reward_grid(win, rewards, w, h)
    display_mouse_grid(win, st, w, h)

def test_grid_policy_iteration():
    pygame.init()

    w = 6
    h = 5
    rewards = ((24, 1),
               (2, -1),
               (13, 1),
               (11, -1))

    terminal = [2, 11, 24]
    new_pos = {"top": 2, "bot": 3, "left": 0, "right": 1}

    S, A, T, P = create_grid_world(w, h, rewards, terminal)

    V, Pi = policy_iteration(S, A, P, T)


    win = pygame.display.set_mode((w * 100, h * 100))
    for i in range(w * h):
        if i % w == 0 and i != 0:
            print("")
        print(round(V[i], 7), end=" ")
    print("")

    for i in range(w * h):
        if i % w == 0 and i != 0:
            print("")
        print(Pi[i], end=" ")

    st = reset_grid(w, h)

    while not is_terminal(st, T):
        display_grid(win, w, h)
        event_loop()
        display_reward_grid(win, rewards, w, h)
        display_mouse_grid(win, st, w, h)
        sleep(1)

        positions = {"top": st - w,
                "bot": st + w,
                "left": st - 1,
                "right": st + 1
                }

        positions_bis = {key: Pi[st][new_pos[key]] for key, value in positions.items() if 0 <= value < w * h and Pi[st][new_pos[key]] > 0}
        action = max(positions_bis, key=positions_bis.get)

        a = new_pos[action]

        st, r, term = step(st, a, T, S, P)
    display_grid(win, w, h)
    display_reward_grid(win, rewards, w, h)
    display_mouse_grid(win, st, w, h)

if __name__ == '__main__':
    #test_grid_iterative_policy_evaluation()
    test_line_iterative_policy_evaluation()
    #test_grid_policy_iteration()

