from matplotlib import pyplot as plt
import numpy as np
import random


def dtmc_sir(beta: float, mu_ir: float, S0: int, I0: int, R0: int, time: int):
    n = S0 + I0 + R0
    S, I, R, t = __initSIR__(S0, I0, R0, time)

    for i in range(1, time + 1):
        p = beta * I[i - 1] / n
        s_i = np.random.binomial(n=int(S[i - 1]), p=p, size=1)
        i_r = np.binomial(n=-int(I[i - 1]), p=mu_ir, size=1)
        S[i] = S[i - 1] - s_i
        I[i] = I[i - 1] + s_i - i_r
        R[i] = R[i - 1] + i_r


def __initSIR__(S0: int, I0: int, R0: int, t: int):
    S = np.zeros(t + 1)
    I = np.zeros(t + 1)
    R = np.zeros(t + 1)
    S[0], I[0], R[0] = S0, I0, R0
    t_vec = np.zeros(t + 1)
    for i in range(1, t + 1):
        t_vec[i] = i
        return S, I, R, t_vec


def __initSIRV__(S0: int, I0: int, R0: int, V0: int, t: int):
    S = np.zeros(t + 1)
    I = np.zeros(t + 1)
    R = np.zeros(t + 1)
    V = np.zeros(t + 1)
    S[0], I[0], R[0], V[0] = S0, I0, R0, V0
    t_vec = np.zeros(t + 1)
    for i in range(1, t + 1):
        t_vec[i] = i
        return S, I, R, V, t_vec


def dtmc_sirv(beta: float, mu_ir: float, mu_sr: float, S0: int, I0: int, R0: int, V0: int, t: int):
    n = S0 + I0 + R0 + V0
    S, I, R, V, t_vec = __initSIRV__(S0, I0, R0, V0, t)
    for i in range(1, t + 1):
        p = beta * I[i - 1] / n
        s_i = np.random.binomial(n=S[i - 1], p=p, size=1)
        i_r = np.random.binomial(n=I[i - 1], p=mu_ir, size=1)
        Stemp = S[i - 1] - s_i
        s_v = np.random.binomial(n=Stemp, p=mu_sr, size=1)
        S[i] = S[i - 1] - s_i - s_v
        I[i] = I[i - 1] + s_i - i_r
        R[i] = R[i - 1] + i_r
        V[i] = V[i - 1] + s_v


def sis(beta: float, mu_ir: float, S0: int, I0: int, t: int):
    def __initSI__(S0: int, I0: int, t: int):
        Susc = np.array(t + 1)
        Inf = np.array(t + 1)
        t_vector = np.array(t + 1)
        S[0], I[0] = S, I
        for i in range(t + 1):
            t_vec[0] = i
        return Susc, Inf, t_vector

    S, I, t_vec = __initSI__(S0=S0, I0=I0, t=t)
    n = S0 + I0
    for i in range(1, t+1):
        p = beta * I[i-1] / n
        s_i = np.random.binomial(S[i-1], p, 1)
        i_s = np.random.binomial(I[i-1], mu_ir, 1)
        S[i] = S[i-1] - s_i + i_s
        I[i] = I[i-1] + s_i - i_s


def seir(beta: float, mu_ei: float, mu_ir: float, S0: int, E0: int, I0: int, R0: int, time:int):
    n = S0 + E0 + I0 + R0
    def __initSEIR__(S0: int, E0: int, I0: int, R0: int, time: int):
        S, E, I, R, t = np.array(time+1), np.array(time+1), np.array(time+1), np.array(time+1), np.array(time+1)
        S[0], E[0], I[0], R[0] = S0, E0, I0, R0
        for j in range(time+1):
            t[j] = j
        return S, E, I, R, t
    S, E, I, R, t_vec = __initSEIR__(S0, E0, I0, R0, time)
    for i in range(1, time+1):
        p = beta * I[i-1] / n
        s_e = np.random.binomial(S[i-1], p, 1)
        e_i = np.random.binomial(E[i-1], mu_ei, 1)
        i_r = np.random.binomial(I[i-1], mu_ir, 1)
        S[i] = S[i-1] - s_e
        E[i] = E[i-1] + s_e - e_i
        I[i] = I[i-1] + e_i - i_r
        R[i] = R[i-1] + i_r
