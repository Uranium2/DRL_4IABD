from time import sleep, time
import numpy as np
import pygame

from algo import iterative_policy_evaluation, policy_iteration, value_iteration, \
    monte_carlo_with_exploring_starts_control, monte_carlo_with_exploring_starts_control_2, \
    on_policy_first_visit_monte_carlo_control, off_policy_monte_carlo_control, tabular_sarsa_control, \
    tabular_sarsa_control_2, tabular_q_learning_control, tabular_q_learning_control_2
from common_func import tabular_uniform_random_policy, is_terminal, event_loop
from grid_world import create_grid_world, step, reset_grid
from grid_world_UI import display_grid, display_reward_grid, display_mouse_grid

from line_world import create_line_world, reset_line
from line_world_UI import display_line,  display_reward_line, display_mouse_line


## policy_evaluation
from tic_tac_toe import create_tic_tac, is_terminate_tic_tac, step_tic_tac, check_terminal_states, reset_tic_tac
from tic_tac_toe_UI import display_grid_tic_tac, display_players, display_win, display_players_2

import settings_tic_tac

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





def test_tic_tac_monte_carlo_es(display=1):
    w = 3
    h = 3
    if display == 1:
        pygame.init()
        win = pygame.display.set_mode((w * 100, h * 100))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
    s_terminal, s_sp, S, A = create_tic_tac(w, h)


    Q0, Pi0 = monte_carlo_with_exploring_starts_control_2(s_terminal, s_sp, 0, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
                                                      episodes_count=10000, max_steps_per_episode=100)

    # Q1, Pi1 = monte_carlo_with_exploring_starts_control_2(s_terminal, s_sp, 1, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
    #                                                   episodes_count=10000, max_steps_per_episode=100)
    game_map = s_sp[0][0]
    state = s_sp[1][str(game_map)]
    is_terminal = False
    while (not is_terminal):
        if display == 1:
            display_grid_tic_tac(win, w, h)
            pygame.display.flip()
            event_loop()
        a = np.argmax(Q0[state])
        state, r0, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 0)

        if display == 1:
            display_players(win, state, w, h, s_sp)
        sleep(0.3)
        if r0 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r0 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r0 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
        a = np.random.choice(np.arange(9))
        state, r1, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 1)

        # a = np.argmax(Q1[state])
        #
        # print("J2 action " + str(a))
        # print(Q1[state])
        # state, r, is_terminal = step_tic_tac(state, a, s_terminal, s_sp, 1)
        if display == 1:
            display_players(win, state, w, h, s_sp)
            sleep(0.3)
        if r1 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r1 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r1 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
    sleep(10)

def test_tic_tac_on_policy_monte_carlo(display=1):
    w = 3
    h = 3
    if display == 1:
        pygame.init()
        win = pygame.display.set_mode((w * 100, h * 100))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
    s_terminal, s_sp, S, A = create_tic_tac(w, h)



    Q0, Pi0 = on_policy_first_visit_monte_carlo_control(s_terminal, s_sp, 0, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
                                                      episodes_count=10000, max_steps_per_episode=100)

    # Q1, Pi1 = monte_carlo_with_exploring_starts_control_2(s_terminal, s_sp, 1, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
    #                                                   episodes_count=10000, max_steps_per_episode=100)

    game_map = s_sp[0][0]
    state = s_sp[1][str(game_map)]
    is_terminal = False
    while (not is_terminal):
        if display == 1:
            display_grid_tic_tac(win, w, h)
            pygame.display.flip()
            event_loop()
        a = np.argmax(Q0[state])
        state, r0, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 0)

        if display == 1:
            display_players(win, state, w, h, s_sp)
        sleep(0.3)
        if r0 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r0 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r0 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
        a = np.random.choice(np.arange(9))
        state, r1, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 1)


        # a = np.argmax(Q1[state])
        #
        # print("J2 action " + str(a))
        # print(Q1[state])
        # state, r, is_terminal = step_tic_tac(state, a, s_terminal, s_sp, 1)
        if display == 1:
            display_players(win, state, w, h, s_sp)
            sleep(0.3)
        if r1 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r1 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r1 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
    sleep(10)


def  test_tic_tac_off_policy_monte_carlo(display=1):
    w = 3
    h = 3
    if display == 1:
        pygame.init()
        win = pygame.display.set_mode((w * 100, h * 100))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
    s_terminal, s_sp, S, A = create_tic_tac(w, h)


    Q0, Pi0 = off_policy_monte_carlo_control(s_terminal, s_sp, 0, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
                                                      episodes_count=10000, max_steps_per_episode=100)

    # Q1, Pi1 = monte_carlo_with_exploring_starts_control_2(s_terminal, s_sp, 1, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
    #                                                   episodes_count=10000, max_steps_per_episode=100)

    game_map = s_sp[0][0]
    state = s_sp[1][str(game_map)]
    is_terminal = False
    while (not is_terminal):
        if display == 1:
            display_grid_tic_tac(win, w, h)
            pygame.display.flip()
            event_loop()
        a = np.argmax(Q0[state])
        state, r0, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 0)

        if display == 1:
            display_players(win, state, w, h, s_sp)
        sleep(0.3)
        if r0 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r0 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r0 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
        a = np.random.choice(np.arange(9))
        state, r1, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 1)


        # a = np.argmax(Q1[state])
        #
        # print("J2 action " + str(a))
        # print(Q1[state])
        # state, r, is_terminal = step_tic_tac(state, a, s_terminal, s_sp, 1)
        if display == 1:
            display_players(win, state, w, h, s_sp)
            sleep(0.3)
        if r1 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r1 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r1 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
    sleep(10)




def test_line_sarsa():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)

    start_time = time()

    Q, Pi = tabular_sarsa_control(T, S, P, len(S), len(A), reset_line, is_terminal, step,
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

def test_grid_sarsa():
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
    Q, Pi = tabular_sarsa_control(T, S, P, len(S), len(A), reset_line, is_terminal, step,
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



def test_tic_tac_sarsa(display=1):
    w = 3
    h = 3
    if display == 1:
        pygame.init()
        win = pygame.display.set_mode((w * 100, h * 100))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
    s_terminal, s_sp, S, A = create_tic_tac(w, h)



    Q0, Pi0 = tabular_sarsa_control_2(s_terminal, s_sp, 0, len(S), len(A), reset_tic_tac, is_terminate_tic_tac, step_tic_tac,
                                                      episodes_count=10000, max_steps_per_episode=100)

    # Q1, Pi1 = monte_carlo_with_exploring_starts_control_2(s_terminal, s_sp, 1, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
    #                                                   episodes_count=10000, max_steps_per_episode=100)

    game_map = s_sp[0][0]
    state = s_sp[1][str(game_map)]
    is_terminal = False
    while (not is_terminal):
        if display == 1:
            display_grid_tic_tac(win, w, h)
            pygame.display.flip()
            event_loop()
        a = np.argmax(Q0[state])
        state, r0, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 0)

        if display == 1:
            display_players(win, state, w, h, s_sp)
        sleep(0.3)
        if r0 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r0 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r0 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
        a = np.random.choice(np.arange(9))
        state, r1, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 1)


        # a = np.argmax(Q1[state])
        #
        # print("J2 action " + str(a))
        # print(Q1[state])
        # state, r, is_terminal = step_tic_tac(state, a, s_terminal, s_sp, 1)
        if display == 1:
            display_players(win, state, w, h, s_sp)
            sleep(0.3)
        if r1 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r1 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r1 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
    sleep(10)

def test_line_q_learning():
    pygame.init()

    num_states = 15
    rewards = ((0, -1),
               (14, 1))

    terminal = [0, 14]

    S, A, T, P = create_line_world(num_states, rewards, terminal)

    start_time = time()

    Q, Pi = tabular_q_learning_control(T, S, P, len(S), len(A), reset_line, is_terminal, step,
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

def test_grid_q_learning():
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
    Q, Pi = tabular_q_learning_control(T, S, P, len(S), len(A), reset_line, is_terminal, step,
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

def log_tic_tac():
    win_0 = 0
    win_1 = 0
    draw = 0
    rounds = 300
    for i in range(rounds):
        if i % 100 == 0:
            print(i)
        winner = test_tic_tac_q_learning(0)
        if winner == 0:
            win_0 = win_0 + 1
        elif winner == 1:
            win_1 = win_1 + 1
        elif winner == -1:
            draw = draw + 1
    print("winner 0 :" + str(win_0 / rounds))
    print("winner 1 :" + str(win_1 / rounds))
    print("draw :" + str(draw / rounds))

def test_tic_tac_q_learning(display=1):
    w = 3
    h = 3
    if display == 1:
        pygame.init()
        win = pygame.display.set_mode((w * 100, h * 100))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
    s_terminal, s_sp, S, A = create_tic_tac(w, h)



    Q0, Pi0 = tabular_q_learning_control_2(s_terminal, s_sp, 0, len(S), len(A), reset_tic_tac, is_terminate_tic_tac, step_tic_tac,
                                                      episodes_count=10000, max_steps_per_episode=100)

    # Q1, Pi1 = monte_carlo_with_exploring_starts_control_2(s_terminal, s_sp, 1, len(S), len(A), is_terminate_tic_tac, step_tic_tac,
    #                                                   episodes_count=10000, max_steps_per_episode=100)

    game_map = s_sp[0][0]
    state = s_sp[1][str(game_map)]
    is_terminal = False
    while (not is_terminal):
        if display == 1:
            display_grid_tic_tac(win, w, h)
            pygame.display.flip()
            event_loop()
        a = np.argmax(Q0[state])
        state, r0, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 0)

        if display == 1:
            display_players(win, state, w, h, s_sp)
        sleep(0.3)
        if r0 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r0 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r0 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
        a = np.random.choice(np.arange(9))
        state, r1, is_terminal, a = step_tic_tac(state, a, s_terminal, s_sp, 1)


        # a = np.argmax(Q1[state])
        #
        # print("J2 action " + str(a))
        # print(Q1[state])
        # state, r, is_terminal = step_tic_tac(state, a, s_terminal, s_sp, 1)
        if display == 1:
            display_players(win, state, w, h, s_sp)
            sleep(0.3)
        if r1 == settings_tic_tac.reward_win:
            if display == 1:
                display_win(win, 1, state, s_sp)
            return 1
            break
        elif r1 == settings_tic_tac.reward_lose:
            if display == 1:
                display_win(win, 0, state, s_sp)
            return 0
            break
        elif r1 == settings_tic_tac.reward_draw:
            if display == 1:
                display_win(win, -1, state, s_sp)
            return -1
            break
    sleep(10)

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

    #test_tic_tac_monte_carlo_es()
    #test_tic_tac_on_policy_monte_carlo()

    #test_tic_tac_off_policy_monte_carlo(display=1)

    #test_line_sarsa()
    #test_grid_sarsa()
    #test_tic_tac_sarsa()


    #log_tic_tac()
    #test_grid_q_learning()
    #test_line_q_learning()
    #test_tic_tac_q_learning()

