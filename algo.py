import time
from typing import Callable

import numpy as np

from common_func import tabular_uniform_random_policy, step_until_the_end_of_the_episode_and_return_history, step_until_the_end_of_the_episode_and_return_history_2
from tic_tac_toe import reset_tic_tac


def iterative_policy_evaluation(
        S: np.ndarray,
        A: np.ndarray,
        P: np.ndarray,
        T: np.ndarray,
        Pi: np.ndarray,
        gamma: float = 0.99,
        theta: float = 0.0001, # accuracy
        V: np.ndarray = None
) -> np.ndarray:

    assert 0 <= gamma <= 1
    assert theta > 0
    if V is None:
        V = np.random.random((S.shape[0],))
        V[T] = 0.0
    while True:
        delta = 0
        for s in S:
            v_temp = V[s]
            tmp_sum = 0
            for a in A:
                for s_p in S: # proba x faisabilité x (reward + longterme x Value s')
                    tmp_sum += Pi[s, a] * P[s, a, s_p, 0] * (
                            P[s, a, s_p, 1] + gamma * V[s_p]
                    )
            V[s] = tmp_sum
            delta = np.maximum(delta, np.abs(tmp_sum - v_temp))
        if delta < theta:
            break
    return V

def policy_iteration(
        S: np.ndarray,
        A: np.ndarray,
        P: np.ndarray,
        T: np.ndarray,
        gamma: float = 0.99,
        theta: float = 0.000001
) -> (np.ndarray, np.ndarray):
    Pi = tabular_uniform_random_policy(S.shape[0], A.shape[0])
    V = np.random.random((S.shape[0],))
    V[T] = 0.0
    while True:
        V = iterative_policy_evaluation(S, A, P, T, Pi, gamma, theta, V)
        policy_stable = True
        for s in S:
            old_action = np.argmax(Pi[s])
            best_action = 0
            best_action_score = -9999999999999
            for a in A:
                tmp_sum = 0
                for s_p in S:
                    tmp_sum += P[s, a, s_p, 0] * (
                            P[s, a, s_p, 1] + gamma * V[s_p]
                    )
                if tmp_sum > best_action_score:
                    best_action = a
                    best_action_score = tmp_sum
            Pi[s] = 0.0
            Pi[s, best_action] = 1.0
            if best_action != old_action:
                policy_stable = False
        if policy_stable:
            break
    return V, Pi

def value_iteration(
        S: np.ndarray,
        A: np.ndarray,
        P: np.ndarray,
        T: np.ndarray,
        gamma: float = 0.99,
        theta: float = 0.000001
) -> (np.ndarray, np.ndarray):
    assert 0 <= gamma <= 1
    assert theta > 0

    V = np.random.random((S.shape[0],))
    V[T] = 0.0
    while True:
        delta = 0
        for s in S:
            v_temp = V[s]
            best_score = -9999999999
            for a in A:
                tmp_sum = 0
                for s_p in S:
                    tmp_sum += P[s, a, s_p, 0] * (
                            P[s, a, s_p, 1] + gamma * V[s_p]
                    )
                if best_score < tmp_sum:
                    best_score = tmp_sum
            V[s] = best_score
            delta = np.maximum(delta, np.abs(V[s] - v_temp))
        if delta < theta:
            break

    Pi = np.zeros((S.shape[0], A.shape[0]))
    for s in S:
        best_action = 0
        best_action_score = -9999999999999
        for a in A:
            tmp_sum = 0
            for s_p in S:
                tmp_sum += P[s, a, s_p, 0] * (
                        P[s, a, s_p, 1] + gamma * V[s_p]
                )
            if tmp_sum > best_action_score:
                best_action = a
                best_action_score = tmp_sum
        Pi[s] = 0.0
        Pi[s, best_action] = 1.0
    return V, Pi

def monte_carlo_with_exploring_starts_control(
        T,
        S,
        P,
        states_count: int,
        actions_count: int,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 10000,
        max_steps_per_episode: int = 10,
        gamma: float = 0.99,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    actions = np.arange(actions_count)
    pi = tabular_uniform_random_policy(states_count, actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, T):
            q[s, :] = 0.0
            pi[s, :] = 0.0

    returns = np.zeros((states_count, actions_count))
    returns_count = np.zeros((states_count, actions_count))
    for episode_id in range(episodes_count):

        s0 = np.random.choice(states)

        if is_terminal_func(s0, T):
            continue

        a0 = np.random.choice(actions)

        s1, r1, t1 = step_func(s0, a0, T, S, P)

        s_list, a_list, _, r_list = step_until_the_end_of_the_episode_and_return_history(T, S, P, s1, pi, is_terminal_func,
                                                                                         step_func,
                                                                                         max_steps_per_episode)
        s_list = [s0] + s_list
        a_list = [a0] + a_list
        r_list = [r1] + r_list

        G = 0
        for t in reversed(range(len(s_list))):
            G = gamma * G + r_list[t]
            st = s_list[t]
            at = a_list[t]

            if (st, at) in zip(s_list[0:t], a_list[0:t]):
                continue
            returns[st, at] += G
            returns_count[st, at] += 1
            q[st, at] = returns[st, at] / returns_count[st, at]
            pi[st, :] = 0.0
            pi[st, np.argmax(q[st, :])] = 1.0
    return q, pi


def monte_carlo_with_exploring_starts_control_2(
        s_terminal,
        s_sp,
        player,
        states_count: int,
        actions_count: int,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 10000,
        max_steps_per_episode: int = 10,
        gamma: float = 0.99,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    actions = np.arange(actions_count)
    pi = tabular_uniform_random_policy(states_count, actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, s_terminal):
            q[s, :] = 0.0
            pi[s, :] = 0.0

    returns = np.zeros((states_count, actions_count))
    returns_count = np.zeros((states_count, actions_count))
    for episode_id in range(episodes_count):

        s0 = np.random.choice(states)

        if is_terminal_func(s0, s_terminal):
            continue

        a0 = np.random.choice(actions)

        s1, r1, t1, a0 = step_func(s0, a0, s_terminal, s_sp, player)
        
        s_list, a_list, _, r_list = step_until_the_end_of_the_episode_and_return_history_2(s_terminal,
                                                                                        s_sp,
                                                                                        player,
                                                                                        s1,
                                                                                        pi,
                                                                                        is_terminal_func,
                                                                                        step_func,
                                                                                        max_steps_per_episode)
        s_list = [s0] + s_list
        a_list = [a0] + a_list
        r_list = [r1] + r_list

        G = 0
        for t in reversed(range(len(s_list))):
            G = gamma * G + r_list[t]
            st = s_list[t]
            at = a_list[t]

            if (st, at) in zip(s_list[0:t], a_list[0:t]):
                continue
            returns[st, at] += G
            returns_count[st, at] += 1
            q[st, at] = returns[st, at] / returns_count[st, at]
            pi[st, :] = 0.0
            pi[st, np.argmax(q[st, :])] = 1.0
    return q, pi




def on_policy_first_visit_monte_carlo_control(
        s_terminal,
        s_sp,
        player,
        states_count: int,
        actions_count: int,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 10000,
        max_steps_per_episode: int = 10,
        gamma: float = 0.99,
        epsilon: float = 0.2,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    pi = tabular_uniform_random_policy(states_count, actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, s_terminal):
            q[s, :] = 0.0
            pi[s, :] = 0.0

    returns = np.zeros((states_count, actions_count))
    returns_count = np.zeros((states_count, actions_count))
    for episode_id in range(episodes_count):
        s0 = reset_tic_tac(s_sp)

        s_list, a_list, _, r_list = step_until_the_end_of_the_episode_and_return_history_2(s_terminal,
                                                                                        s_sp,
                                                                                        player,
                                                                                        s0,
                                                                                        pi,
                                                                                        is_terminal_func,
                                                                                        step_func,
                                                                                        max_steps_per_episode)
        G = 0
        for t in reversed(range(len(s_list))):
            G = gamma * G + r_list[t]
            st = s_list[t]
            at = a_list[t]

            if (st, at) in zip(s_list[0:t], a_list[0:t]):
                continue
            returns[st, at] += G
            returns_count[st, at] += 1
            q[st, at] = returns[st, at] / returns_count[st, at]
            pi[st, :] = epsilon / actions_count
            pi[st, np.argmax(q[st, :])] = 1.0 - epsilon + epsilon / actions_count
    return q, pi


def off_policy_monte_carlo_control(
        s_terminal,
        s_sp,
        player,
        states_count: int,
        actions_count: int,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 10000,
        max_steps_per_episode: int = 10,
        gamma: float = 0.99,
        epsilon: float = 0.2,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    b = tabular_uniform_random_policy(states_count, actions_count)
    pi = np.zeros((states_count, actions_count))
    C = np.zeros((states_count, actions_count))
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, s_terminal):
            q[s, :] = 0.0
            pi[s, :] = 0.0
        pi[s, :] = 0.0
        pi[s, np.argmax(q[s, :])] = 1.0

    for episode_id in range(episodes_count):
        s0 = reset_tic_tac(s_sp)

        s_list, a_list, _, r_list = step_until_the_end_of_the_episode_and_return_history_2(s_terminal,
                                                                                        s_sp,
                                                                                        player,
                                                                                        s0,
                                                                                        pi,
                                                                                        is_terminal_func,
                                                                                        step_func,
                                                                                        max_steps_per_episode)

        G = 0
        W = 1
        for t in reversed(range(len(s_list))):
            G = gamma * G + r_list[t]
            st = s_list[t]
            at = a_list[t]

            C[st, at] += W

            q[st, at] += W / C[st, at] * (G - q[st, at])
            pi[st, :] = 0.0
            pi[st, np.argmax(q[st, :])] = 1.0

            if at != np.argmax(q[st, :]):
                break

            W = W / b[st, at]

    return q, pi


def tabular_sarsa_control(
        T, S, P,
        states_count: int,
        actions_count: int,
        reset_func: Callable,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 50000,
        max_steps_per_episode: int = 10,
        epsilon: float = 0.2,
        alpha: float = 0.1,
        gamma: float = 0.99,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    actions = np.arange(actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, T):
            q[s, :] = 0.0

    for episode_id in range(episodes_count):
        s = reset_func(states_count)
        rdm = np.random.random()
        a = np.random.choice(actions) if rdm < epsilon else np.argmax(q[s, :])
        step = 0
        while not is_terminal_func(s, T) and step < max_steps_per_episode:
            (s_p, r, t) = step_func(s, a, T, S, P)
            rdm = np.random.random()
            a_p = np.random.choice(actions) if rdm < epsilon else np.argmax(q[s_p, :])
            q[s, a] += alpha * (r + gamma * q[s_p, a_p] - q[s, a])
            s = s_p
            a = a_p
            step += 1

    pi = np.zeros_like(q)
    for s in states:
        pi[s, :] = epsilon / actions_count
        pi[s, np.argmax(q[s, :])] = 1.0 - epsilon + epsilon / actions_count

    return q, pi


def tabular_sarsa_control_2(
        s_terminal,
        s_sp,
        player,
        states_count: int,
        actions_count: int,
        reset_func: Callable,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 50000,
        max_steps_per_episode: int = 10,
        epsilon: float = 0.2,
        alpha: float = 0.1,
        gamma: float = 0.99,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    actions = np.arange(actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, s_terminal):
            q[s, :] = 0.0

    for episode_id in range(episodes_count):
        s0 = reset_tic_tac(s_sp)
        rdm = np.random.random()
        a = np.random.choice(actions) if rdm < epsilon else np.argmax(q[s, :])
        step = 0
        while not is_terminal_func(s, s_terminal) and step < max_steps_per_episode:
            (s_p, r, t) = step_func(s0, a, s_terminal, s_sp, player)

            rdm = np.random.random()
            a_p = np.random.choice(actions) if rdm < epsilon else np.argmax(q[s_p, :])
            q[s, a] += alpha * (r + gamma * q[s_p, a_p] - q[s, a])
            s = s_p
            a = a_p
            step += 1

    pi = np.zeros_like(q)
    for s in states:
        pi[s, :] = epsilon / actions_count
        pi[s, np.argmax(q[s, :])] = 1.0 - epsilon + epsilon / actions_count

    return q, pi

def tabular_q_learning_control_2(
        s_terminal,
        s_sp,
        player,
        states_count: int,
        actions_count: int,
        reset_func: Callable,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 50000,
        max_steps_per_episode: int = 10,
        epsilon: float = 0.2,
        alpha: float = 0.1,
        gamma: float = 0.99,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    actions = np.arange(actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, s_terminal):
            q[s, :] = 0.0

    for episode_id in range(episodes_count):
        s0 = reset_func(s_sp)
        step = 0
        while not is_terminal_func(s, s_terminal) and step < max_steps_per_episode:
            rdm = np.random.random()
            a = np.random.choice(actions) if rdm < epsilon else np.argmax(q[s, :])
            (s_p, r, t) = step_func(s0, a, s_terminal, s_sp, player)
            q[s, a] += alpha * (r + gamma * np.max(q[s_p, :]) - q[s, a])
            s = s_p
            step += 1

    pi = np.zeros_like(q)
    for s in states:
        pi[s, :] = 0.0
        pi[s, np.argmax(q[s, :])] = 1.0

    return q, pi

def tabular_q_learning_control(
        T, S, P,
        states_count: int,
        actions_count: int,
        reset_func: Callable,
        is_terminal_func: Callable,
        step_func: Callable,
        episodes_count: int = 50000,
        max_steps_per_episode: int = 10,
        epsilon: float = 0.2,
        alpha: float = 0.1,
        gamma: float = 0.99,
) -> (np.ndarray, np.ndarray):
    states = np.arange(states_count)
    actions = np.arange(actions_count)
    q = np.random.random((states_count, actions_count))
    for s in states:
        if is_terminal_func(s, T):
            q[s, :] = 0.0

    for episode_id in range(episodes_count):
        s = reset_func(states_count)
        step = 0
        while not is_terminal_func(s, T) and step < max_steps_per_episode:
            rdm = np.random.random()
            a = np.random.choice(actions) if rdm < epsilon else np.argmax(q[s, :])
            (s_p, r, t) = step_func(s, a, T, S, P)
            q[s, a] += alpha * (r + gamma * np.max(q[s_p, :]) - q[s, a])
            s = s_p
            step += 1

    pi = np.zeros_like(q)
    for s in states:
        pi[s, :] = 0.0
        pi[s, np.argmax(q[s, :])] = 1.0

    return q, pi
