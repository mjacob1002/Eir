from matplotlib import pyplot as plt
import numpy as np


# tested
def dtmc_sir(beta: float, mu_ir: float, S0: int, I0: int, R0: int, time: int, xlabel: str):
    """
    Uses a Discrete Time Markov Chain method in order to plot a standard SIR model.
    :param beta: effective transmission rate
    :param mu_ir: the probability that an infected individual moves to the removed compartment
    :param S0: initial amount of susceptibles
    :param I0: initial amount of infecteds
    :param R0: initial amount of removeds
    :param time: duration of the markov chain; how many unit times
    :param xlabel: the unit of time for the "time" variable
    :return: nothing for now
    """
    n = S0 + I0 + R0
    S, I, R, t = __initSIR__(S0, I0, R0, time)

    for i in range(1, time + 1):
        p = beta * I[i - 1] / n
        print("P: ", p, " I: ", I[i - 1])
        s_i = np.random.binomial(n=int(S[i - 1]), p=p, size=1)
        i_r = np.random.binomial(n=int(I[i - 1]), p=mu_ir, size=1)
        S[i] = S[i - 1] - s_i
        I[i] = I[i - 1] + s_i - i_r
        R[i] = R[i - 1] + i_r
    plt.plot(t, I, label="Infected")
    plt.plot(t, S, label="Susceptible")
    plt.plot(t, R, label="Removed")
    plt.xlabel(xlabel=xlabel)
    plt.ylabel("Number of People")
    plt.legend()
    plt.title()
    plt.show()
    return S, I, R, t


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


# tested
def dtmc_sirv(t: int, beta: float, mu_ir: float, mu_sv: float, S0: int, I0: int, R0: int, V0 = 0.0, x_label = "Days"):
    """

    :param beta: effective transmission rate
    :param mu_ir: probability of transitioning from compartment Infected to Removed
    :param mu_sv: Probability of transitioning from Compartment Susceptible to Vaccinated
    :param S0: Starting amount of Susceptibles at the beginning of the simulation
    :param I0: Starting amount of Infected people at the beginning of the simulation
    :param R0: Starting amount of Removed people at the beginning of the simulation
    :param V0: Starting amount of Vaccinated people at the beginning of the simulation
    :param t: The amount of time the simulation should last
    :param x_label: The unit time used i.e hours, days, etc.
    :return: Susceptibles, Infected, Removed, Vaccinated arrays with values at each state change, as well as array of differnet time intervals

    """
    n = S0 + I0 + R0 + V0
    S, I, R, V, t_vec = __initSIRV__(S0, I0, R0, V0, t)
    for i in range(1, t + 1):
        p = beta * I[i - 1] / n
        s_i = np.random.binomial(n=S[i - 1], p=p, size=1)
        i_r = np.random.binomial(n=I[i - 1], p=mu_ir, size=1)
        Stemp = int(S[i - 1] - s_i)
        s_v = np.random.binomial(n=Stemp, p=mu_sv, size=1)
        S[i] = S[i - 1] - s_i - s_v
        I[i] = I[i - 1] + s_i - i_r
        R[i] = R[i - 1] + i_r
        V[i] = V[i - 1] + s_v
        print("STemp: ", Stemp, " S: ", S[i - 1], " I: ", I[i - 1], "R: ", R[i - 1], "V: ", V[i - 1])
    title = "SIRV Model; Beta = " + str(beta) + " Gamma= " + str(mu_ir) + "vaccine rate = " + str(mu_sv)
    plt.plot(t_vec, I, label="Infected")
    plt.plot(t_vec, S, label="Susceptible")
    plt.plot(t_vec, R, label="Removed")
    plt.plot(t_vec, V, label="Vaccine")
    plt.xlabel(xlabel=x_label)
    plt.ylabel("Number of People")
    plt.title(title)
    plt.legend()
    plt.show()
    return S, I, R, V, t_vec


# tested
def dtmc_sis(beta: float, mu_is: float, S0: int, I0: int, t: int, x_label: str):
    """
    
    :param beta:
    :param mu_is:
    :param S0:
    :param I0:
    :param t:
    :param x_label:
    :return:
    """
    def __initSI__(S0: int, I0: int, t: int):
        Susc = np.zeros(t + 1)
        Inf = np.zeros(t + 1)
        t_vector = np.zeros(t + 1)
        Susc[0], Inf[0] = S0, I0
        for i in range(t + 1):
            t_vector[i] = i
        return Susc, Inf, t_vector

    S, I, t_vec = __initSI__(S0=S0, I0=I0, t=t)
    n = S0 + I0
    for i in range(1, t + 1):
        p = beta * I[i - 1] / n
        s_i = np.random.binomial(S[i - 1], p, 1)
        i_s = np.random.binomial(I[i - 1], mu_is, 1)
        S[i] = S[i - 1] - s_i + i_s
        I[i] = I[i - 1] + s_i - i_s
        print("S; ", S[i - 1], " I: ", I[i - 1])
    plt.plot(t_vec, S, label="Susceptible")
    plt.plot(t_vec, I, label="Infected")
    plt.xlabel(x_label)
    plt.ylabel("Number of People")
    plt.legend()
    plt.show()
    return S, I, t_vec


# tested
def seir(beta: float, mu_ei: float, mu_ir: float, S0: int, E0: int, I0: int, R0: int, time: int, x_label: str):
    """
    Susceptible, Exposed, Infected, Removed compartmental model. Assumes that exposed individuals cannot transmit the
    disease.
    :param beta: effective transmission rate per unit time
    :param mu_ei: probability of transferring from exposed to infected
    :param mu_ir: probability of transferring from infected to removed
    :param S0: Initial Susceptible people at the start of the simulation
    :param E0: Initial Exposed people at the start of the simulation
    :param I0: Initial Infected people at the start of the simulation
    :param R0: Initial Removed people at the start of the simulation
    :param time: the amount of time for the simulation to run for
    :param x_label: the unit of time
    x_label:
    :return: return numpy array of number of susceptibles, exposed, infected, removed, and time vector with the
    time of each state change
    """
    n = S0 + E0 + I0 + R0

    def __initSEIR__(S0: int, E0: int, I0: int, R0: int, time: int):
        S, E, I, R, t = np.zeros(time + 1), np.zeros(time + 1), np.zeros(time + 1), np.zeros(time + 1), np.zeros(
            time + 1)
        S[0], E[0], I[0], R[0] = S0, E0, I0, R0
        for j in range(time + 1):
            t[j] = j
        return S, E, I, R, t

    S, E, I, R, t_vec = __initSEIR__(S0, E0, I0, R0, time)
    for i in range(1, time + 1):
        p = beta * I[i - 1] / n
        s_e = np.random.binomial(S[i - 1], p, 1)
        e_i = np.random.binomial(E[i - 1], mu_ei, 1)
        i_r = np.random.binomial(I[i - 1], mu_ir, 1)
        S[i] = S[i - 1] - s_e
        E[i] = E[i - 1] + s_e - e_i
        I[i] = I[i - 1] + e_i - i_r
        R[i] = R[i - 1] + i_r
    plt.plot(t_vec, S, label="Susceptible")
    plt.plot(t_vec, I, label="Infected")
    plt.plot(t_vec, E, label="Exposed")
    plt.plot(t_vec, R, label="Removed")
    plt.xlabel = x_label
    plt.ylabel = "Number of People"
    plt.legend()
    plt.show()
    return S, E, I, R, t_vec


# test:

beta1 = 2 / 24
ei = 1 / 24
ir = .8 / 24
S0 = 999
E0 = 0
I0 = 1
R0 = 0
time = 30 * 24
xlabel = "Hours"
#seir(beta=beta1, mu_ei=ei, mu_ir=ir, S0=S0, E0=E0, I0=I0, R0=R0, time=time, x_label=xlabel)
dtmc_sir(beta=beta1, mu_ir=ir, S0=S0, I0=I0, R0=R0, time=time, xlabel="Hours")
