import numpy as np
from matplotlib import pyplot as plt


def determ_sir(beta: float, gamma: float, S0: int, I0: int, R0: int, time: int, dt: float, x_label: str):
    def f(beta: float, gamma: float, S: float, I: float, R: float, n: int. title):
        x = beta * I * S / n
        y = gamma * I
        return -x, x - y

    k = int(time / dt)
    n = S0 + I0 + R0
    S, I, R, t = np.zeros(k + 1), np.zeros(k + 1), np.zeros(k + 1), np.zeros(k + 1)
    S[0], I[0], R[0], t[0] = S0, I0, R0, 0
    for i in range(1, k + 1):
        change = f(beta=beta, gamma=gamma, S=S[i - 1], I=I[i - 1], R=R[i-1], n=n)
        S[i] = S[i - 1] + dt * change[0]
        I[i] = I[i - 1] + dt * change[1]
        R[i] = R[i - 1] + dt * change[2]
        t[i] = i
    plt.plot(t, S, label="Susceptible")
    plt.plot(t, I, label="Infected")
    plt.plot(t, R, label="Removed")
    plt.xlabel(x_label)
    plt.ylabel("Number of People")
    plt.legend()
    plt.show()


def determ_SIRV(beta: float, gamma: float, vrate: float, S0: int, I0: int, R0: int, V0: int, time: int, dt: float,
                x_label: str, title="SIR Model", fname="SIRDeterministicModel.png"):
    k = int(time / dt)
    S, I, R, V, t = np.zeros(k + 1), np.zeros(k + 1), np.zeros(k + 1), np.zeros(k + 1), np.zeros(k + 1)
    S[0], I[0], R[0], V[0], t[0] = S0, I0, R0, V0, 0
    n = S0 + I0 + R0

    def f(beta: float, gamma: float, vrate: float, S: float, I: float, n: int):
        x = beta * S * I / n
        y = gamma * I
        z = vrate * S / n
        print(z)
        return -x - z, x - y, y, z

    for i in range(1, k + 1):
        rate = f(beta=beta, gamma=gamma, vrate=vrate, S=S[i - 1], I=I[i - 1], n=n) 
        S[i] = S[i-1] + dt * rate[0]
        I[i] = I[i-1] + dt * rate[1]
        R[i] = R[i-1] + dt * rate[2]
        V[i] = V[i-1] + dt * rate[3]
        t[i] = i
    plt.plot(t, S,label="Susceptible")
    plt.plot(t, I, label="Infected")
    plt.plot(t, R, label="Removed")
    plt.plot(t, V, label="Vaccinated")
    plt.xlabel(x_label)
    plt.ylabel("Number of People")
    plt.title(title)
    plt.legend()
    plt.show()
    plt.savefig(fname)

def determ_sis(beta: float, gamma: float, S0: float, I0: float, time: int, dt: float, x_label="Days", title="SIS model",
               fname="SISModelPng"):
    """
    Describes how to model SIS. 
    """
    n = S0 + I0
    S, I, t = np.zeros(int(time / dt) + 1), np.zeros(int(time / dt + 1)), np.zeros(int(time / dt) + 1)
    S[0], I[0] = S0, I0

    def f(beta, gamma, S, I, n):
        x = beta * S * I / n
        y = gamma * I
        return y - x, x - y

    for i in range(1, int(time / dt + 1)):
        t[i] = i
        r = f(beta, gamma, S[i-1], I[i-1], n)
        S[i] = S[i - 1] + dt * r[0]
        I[i] = I[i - 1] + dt * r[1]
    plt.plot(t, S, label="Susceptibles")
    plt.plot(t, I, label="Infected")
    plt.xlabel(x_label)
    plt.ylabel("Number of People")
    plt.title(title)
    plt.legend()
    plt.savefig(fname)
    plt.show()
    return S, I

beta1 = 1/50
gamma1 = 1/100
vrate1 = 1/100
S0 = 980
I0 = 2
R0 = 0
V0 = 0
time = 6000
dt = .1
xlabel = "Days"

