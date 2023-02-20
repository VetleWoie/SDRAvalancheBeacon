import numpy as np
from matplotlib import pyplot as plt
def inductance(mu_r, N, A, l):
    mu_0 = (4 * np.pi) * 10**-7
    return (mu_r*mu_0*(N**2)*A)/l

def freq(L, C):
    return 1 / (2*np.pi * np.sqrt(L*C))

def capacitance(f, L):
    return 1 / (((2*np.pi*f)**2) * L)

if __name__ == "__main__":
    N = np.linspace(10,200)
    r = 0.4E-3
    A = 2*np.pi * (r**2)
    d = 0.224E-3
    l = N*d
    mu_r = 24


    L = inductance(mu_r, N, A, l)
    fig, ax = plt.subplots(1,1)
    ax.set_title('Inductance')
    ax.set_xlabel("Number of turns")
    ax.set_ylabel("Inductance/henry")
    ax.plot(N,L)
    ax.plot(N,np.full(N.shape, inductance(mu_r, 20, A, 20*d)), label = f"$L = {inductance(mu_r, 20, A, 20*d)}$")
    plt.legend()
    plt.show()

    C = 20E-12
    f = freq(L, C)
    ax[1].set_title('Frequency')
    ax[1].set_xlabel("Number of turns")
    ax[1].set_ylabel("Frequency/hz")
    ax[1].plot(N,f)

    f = 457E3
    C = capacitance(f, L)
    ax[2].set_title('Capacitance needed for 457khz')
    ax[2].set_xlabel("Number of turns")
    ax[2].set_ylabel("Capacitance/farad")
    ax[2].plot(N,C)
    plt.show()



