from time import sleep

import pygame

from algo import iterative_policy_evaluation
from grid_world import create_grid_world, tabular_uniform_random_policy, step, reset, is_terminal
from grid_world_UI import display_grid, event_loop, display_reward, display_mouse

from line_world import create_line_world, tabular_uniform_random_policy, step, reset, is_terminal
from line_world_UI import display_line, event_loop, display_reward, display_mouse



def test_line_iterative_policy_evaluation():
    pygame.init()

    num_states = 7
    rewards = ((0, -1),
               (6, 1))

    terminal = [0, 6]

    S, A, T, P = create_line_world(num_states, rewards, terminal)
    Pi = tabular_uniform_random_policy(S.shape[0], A.shape[0])

    V = iterative_policy_evaluation(S, A, P, T, Pi)
    print(V)


    win = pygame.display.set_mode((num_states * 100, 100))

    st = reset(num_states)

    while not is_terminal(st, T):
        display_line(win, num_states)
        event_loop()
        display_reward(win, rewards, num_states)
        display_mouse(win, st, num_states)
        sleep(1)

        if V[st + 1] > V[st - 1] or V[st + 1] == 0:
            a = 1
        elif V[st + 1] <  V[st - 1] or V[st - 1] == 0:
            a = 0
        st, r, term = step(st, a, T, S, P)

    display_line(win, num_states)
    display_reward(win, rewards,num_states)
    display_mouse(win, st, num_states)
    sleep(1)

def test_grid_iterative_policy_evaluation():
    pygame.init()

    w = 1
    h = 5
    rewards = ((24, 1),
               (2, -1),
               (11, -1))

    terminal = [2, 11, 24]

    S, A, T, P = create_grid_world(w, h, rewards, terminal)
    Pi = tabular_uniform_random_policy(S.shape[0], A.shape[0])

    V = iterative_policy_evaluation(S, A, P, T, Pi)


    win = pygame.display.set_mode((w * 100, h * 100))
    for i in range(w * h):
        if i % 5 == 0 and i != 0:
            print("")
        print(round(V[i], 7), end=" ")
    st = reset(w, h)

    while not is_terminal(st, T):
        display_grid(win, w, h)
        event_loop()
        display_reward(win, rewards, w, h)
        display_mouse(win, st, w, h)
        sleep(1)

        if V[st + 1] > V[st - 1] and V[st + 1] > V[st - w] and V[st + 1] > V[st + w]:
            a = 1
        elif V[st - 1] > V[st + 1] and V[st - 1] > V[st - w] and V[st - 1] > V[st + w]:
            a = 0
        elif V[st - w] > V[st + 1] and V[st - w] > V[st - 1] and V[st - w] > V[st + w]:
            a = 2
        else:
            a = 3
        st, r, term = step(st, a, T, S, P)
    display_grid(win, w, h)
    display_reward(win, rewards, w, h)
    display_mouse(win, st, w, h)
    sleep(1)

if __name__ == '__main__':
    #test_grid_iterative_policy_evaluation()
    test_line_iterative_policy_evaluation()

