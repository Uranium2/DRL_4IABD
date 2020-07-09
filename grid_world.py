import numpy as np

def create_grid_world(w, h, reward_list, terminal):
    num_states = w * h

    S = np.arange(num_states)
    A = np.array([0, 1, 2, 3])  # 0: left, 1 : right, 2: top, 3: bot
    T = np.array(terminal)  # Terminal State ( position)
    P = np.zeros((len(S), len(A), len(S), 2))

    for s in S:
        if (s % w) == 0:
            P[s, 0, s, 0] = 1.0
        else:
            P[s, 0, s - 1, 0] = 1.0
        if (s + 1) % w == 0:
            P[s, 1, s, 0] = 1.0
        else:
            P[s, 1, s + 1, 0] = 1.0
        if s < w:
            P[s, 2, s, 0] = 1.0
        else:
            P[s, 2, s - w, 0] = 1.0
        if s >= (num_states - w):
            P[s, 3, s, 0] = 1.0
        else:
            P[s, 3, s + w, 0] = 1.0

    for r in reward_list:
        set_reward(P, r, w, h)
    return S, A, T, P

def set_reward(P, reward_tuple, n, m):
    if (reward_tuple[0] + 1) % n != 0: # case de Droite
        P[reward_tuple[0] + 1, 0,reward_tuple[0], 1] = reward_tuple[1]

    if (reward_tuple[0] - 1) % n != 0: # case de Gauche
        P[reward_tuple[0] - 1, 1, reward_tuple[0], 1] = reward_tuple[1]

    if reward_tuple[0] - n >= n: #  case du top
        P[reward_tuple[0] - n, 3, reward_tuple[0], 1] = reward_tuple[1]

    if reward_tuple[0] + n < n * m - n: # case du bot
        P[reward_tuple[0] + n, 2, reward_tuple[0], 1] = reward_tuple[1]

def reset_grid(w, h) -> int:
    return w * h // 2


def step(state: int, a: int, T, S, P) -> (int, float, bool):
    assert (state not in T)

    s_p = np.random.choice(S, p=P[state, a, :, 0])  # trouve ta position d'arrivée
    r = P[state, a, s_p, 1]  # recupere reward
    return s_p, r, (s_p in T)  # position, reward, si terminal