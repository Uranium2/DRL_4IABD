from time import sleep, time
import numpy as np
import pygame

from algo import iterative_policy_evaluation, policy_iteration, value_iteration, \
    monte_carlo_with_exploring_starts_control, monte_carlo_with_exploring_starts_control_2
from common_func import tabular_uniform_random_policy, is_terminal, event_loop
from grid_world import create_grid_world, step, reset_grid
from grid_world_UI import display_grid, display_reward_grid, display_mouse_grid

from line_world import create_line_world, reset_line
from line_world_UI import display_line,  display_reward_line, display_mouse_line


## policy_evaluation
from tic_tac_toe import create_tic_tac, is_terminate_tic_tac, step_tic_tac, check_terminal_states
from tic_tac_toe_UI import display_grid_tic_tac

import itertools


def test_line_iterative_policy_evaluation():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)
    Pi = tabular_uniform_random_policy(S.shape[0], A.shape[0])

    start_time = time()
    V = iterative_policy_evaluation(S, A, P, T, Pi)
    print("--- %s seconds ---" % (time() - start_time))

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

    start_time = time()
    V = iterative_policy_evaluation(S, A, P, T, Pi)
    print("--- %s seconds ---" % (time() - start_time))


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

## policy_iteration
def test_grid_policy_iteration():
    pygame.init()

    w = 6
    h = 5
    rewards = ((24, 1),
               (2, -1),
               (11, -1),
               (27, -1))

    terminal = [2, 11, 24]
    new_pos = {"top": 2, "bot": 3, "left": 0, "right": 1}

    S, A, T, P = create_grid_world(w, h, rewards, terminal)

    start_time = time()
    V, Pi = policy_iteration(S, A, P, T)
    print("--- %s seconds ---" % (time() - start_time))


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

def test_line_policy_iteration():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)

    start_time = time()
    V, Pi = policy_iteration(S, A, P, T)
    print("--- %s seconds ---" % (time() - start_time))

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
        elif V[st + 1] < V[st - 1] or V[st - 1] == 0:
            a = 0
        st, r, term = step(st, a, T, S, P)

    display_line(win, num_states)
    display_reward_line(win, rewards,num_states)
    display_mouse_line(win, st, num_states)
    sleep(1)

## value_iteration
def test_line_value_iteration():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)

    start_time = time()
    V, Pi = value_iteration(S, A, P, T)
    print("--- %s seconds ---" % (time() - start_time))

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
        elif V[st + 1] < V[st - 1] or V[st - 1] == 0:
            a = 0
        st, r, term = step(st, a, T, S, P)

    display_line(win, num_states)
    display_reward_line(win, rewards,num_states)
    display_mouse_line(win, st, num_states)
    sleep(1)

def test_grid_value_iteration():
    pygame.init()

    w = 6
    h = 5
    rewards = ((24, 1),
               (2, -1),
               (11, -1),
               (27, -1))

    terminal = [2, 11, 24]
    new_pos = {"top": 2, "bot": 3, "left": 0, "right": 1}

    S, A, T, P = create_grid_world(w, h, rewards, terminal)

    start_time = time()
    V, Pi = value_iteration(S, A, P, T)
    print("--- %s seconds ---" % (time() - start_time))


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

# Monte Carlo

def test_line_monte_carlo_es():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)

    start_time = time()
    Q, Pi = monte_carlo_with_exploring_starts_control(T, S, P, len(S), len(A), is_terminal, step,
                                                      episodes_count=10000, max_steps_per_episode=100)
    print("--- %s seconds ---" % (time() - start_time))
    for i in range(num_states):
        print(Q[i], end=" ")


    win = pygame.display.set_mode((num_states * 100, 100))

    st = reset_line(num_states)

    while not is_terminal(st, T):
        display_line(win, num_states)
        event_loop()
        display_reward_line(win, rewards, num_states)
        display_mouse_line(win, st, num_states)
        sleep(1)

        a = np.argmax(Q[st])

        st, r, term = step(st, a, T, S, P)

    display_line(win, num_states)
    display_reward_line(win, rewards,num_states)
    display_mouse_line(win, st, num_states)
    sleep(1)


def test_grid_monte_carlo_es():
    pygame.init()

    w = 6
    h = 5
    rewards = ((24, 1),
               (2, -1),
               (11, -1),
               (27, -1))

    terminal = [2, 11, 24]

    new_pos = {"top": 2, "bot": 3, "left": 0, "right": 1}

    S, A, T, P = create_grid_world(w, h, rewards, terminal)

    start_time = time()
    Q, Pi = monte_carlo_with_exploring_starts_control_2(len(S), len(A), is_terminal, step,
                                                      episodes_count=10000, max_steps_per_episode=100)
    print("--- %s seconds ---" % (time() - start_time))


    win = pygame.display.set_mode((w * 100, h * 100))


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

        a = np.argmax(Q[st])
        st, r, term = step(st, a, T, S, P)
    display_grid(win, w, h)
    display_reward_grid(win, rewards, w, h)
    display_mouse_grid(win, st, w, h)


def test_tic_tac_monte_carlo_es():
    w = 3
    h = 3
    # pygame.init()
    # win = pygame.display.set_mode((w * 100, h * 100))
    # create_tic_tac()

    player = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    S = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(player, repeat=9)]

    s_terminal = [(i, check_terminal_states(s)) for i, s in enumerate(S)]
    s_terminal = dict(s_terminal)

    A = np.arange(h * w)

    Q, Pi = monte_carlo_with_exploring_starts_control_2(s_terminal, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
                                                      episodes_count=10000, max_steps_per_episode=100)
    # while (True):
    #     display_grid_tic_tac(win, w, h)
    #     pygame.display.flip()


if __name__ == '__main__':
    #test_grid_iterative_policy_evaluation()
    #test_line_iterative_policy_evaluation()

    #test_grid_policy_iteration()
    #test_line_policy_iteration()

    #test_line_value_iteration()
    #test_grid_policy_iteration()

    #test_line_monte_carlo_es()
    #test_grid_policy_iteration_2()
    #test_grid_monte_carlo_es()

    test_tic_tac_monte_carlo_es()
