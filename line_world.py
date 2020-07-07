import numpy as np

def create_line_world(num_states, rewards, terminal):
    S = np.arange(num_states)
    A = np.array([0, 1])  # 0: left, 1 : right
    T = np.array(terminal) # Terminal State ( position)
    P = np.zeros((len(S), len(A), len(S), 2))


    for s in S[1:-1]: #  possible action
        P[s, 0, s - 1, 0] = 1.0
        P[s, 1, s + 1, 0] = 1.0

    for r in rewards:
        set_reward(P, r, num_states)
    return S, A, T, P

def tabular_uniform_random_policy(space_size: int, action_size: int):
    return np.ones((space_size, action_size)) / action_size

def set_reward(P, reward_tuple, num_states):
    if (reward_tuple[0] + 1) % num_states != 0: # case de Droite
        P[reward_tuple[0] + 1, 0,reward_tuple[0], 1] = reward_tuple[1]

    if (reward_tuple[0] - 1) % num_states != 0: # case de Gauche
        P[reward_tuple[0] - 1, 1, reward_tuple[0], 1] = reward_tuple[1]

def reset(num_states) -> int:
    return num_states // 2

def is_terminal(state: int, T) -> bool:
    return state in T

def step(state: int, a: int, T, S, P ) -> (int, float, bool):
    assert (state not in T)
    s_p = np.random.choice(S, p=P[state, a, :, 0])  # trouve ta position d'arrivée
    r = P[state, a, s_p, 1]  # recupere reward
    return s_p, r, (s_p in T)  # position, reward, si terminal