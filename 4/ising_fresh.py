import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numba

k = 1
J = 1

T = 1

N = 16
NT = 10000
snap_every = NT // 100
N_snapshots = NT // snap_every

np.random.seed(1)
spins = np.random.randint(0, 2, size=(N, N)) * 2 - 1
magnetyzacja = spins.sum()
mag_array = np.zeros(NT)

def flip_spin(spins):
    """
    1. wybieramy losowy spin (dwa inty od 0 do N)
    2. liczymy energię jako sumę czterech składników
        * okresowe warunki brzegowe
    3. liczymy boltzmannowski czynnik
    4. losujemy uniform (0, 1)
    5. jeśli boltzmannowski czynnik < uniform: olewamy
        * inaczej: spin[losowy] *= -1
    6. w spins jeden ze spinów jest zamieniony: lub nie
    """
    global magnetyzacja

    x, y = np.random.randint(0, N, size=2)
    beta = 1/k/T
    energia = 2*J * spins[x,y] * (spins[(x+1)%N, y] + spins[(x-1)%N, y] +
                                spins[x, (y+1)%N] + spins[x, (y-1)%N])

    boltzmann = np.exp(-energia*beta)
    acceptance = np.random.random()
    if boltzmann > acceptance:
        magnetyzacja -= 2*spins[x, y]
        spins[x, y] *= -1

def plot_mag():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(mag_array/N**2)
    plt.show()

spins_history = np.empty(shape=(N_snapshots, N, N))

@numba.jit()
def petla_czasowa():
    for i in range(NT):
        if i % snap_every == 0:
            spins_history[i // snap_every] = spins
        mag_array[i] = magnetyzacja

        flip_spin(spins)

petla_czasowa()
plot_mag()

def animacja(spins):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    IM = ax.imshow(spins_history[0], origin='lower', cmap='Greys',
                  interpolation='none')
    title = ax.set_title("T= {}".format(T) + " i = 0 ")
    def animate(i):
        IM.set_array(spins_history[i])
        title.set_text("T= {}".format(T) + " i = {} ".format(i*snap_every))
        return [IM, title]

    animacja_niepotrzebna_zmienna = ani.FuncAnimation(fig, animate,
                                    frames = N_snapshots)
    plt.show()
animacja(spins)
