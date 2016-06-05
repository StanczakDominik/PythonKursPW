import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

k = 1
J = 1
np.random.seed(1)

def ising(N, T, NT, snap_every):
    beta = 1/k/T
    N_snapshots = NT//snap_every
    spins = np.random.randint(0,2, size=(N,N))*2-1
    snapshots = np.empty((N_snapshots, N, N))
    def flip_spin(spins):
        x, y = np.random.randint(0,N,2)    #1.
        test = spins[x,y]
        neighbor_spins = spins[(x+1)%N,(y)%N] + spins[(x-1)%N,y%N] +
                            spins[x%N,(y-1)%N] + spins[x%N,(y+1)%N] #2.
        deltaE=J*2*test*neighbor_spins #3.
        probability_cutoff = np.exp(-beta*deltaE) #4.
        uniform_random = np.random.random() #5.

        if(uniform_random < probability_cutoff): #6.
            spins[x,y] *= -1

    def plot(spins):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(spins, origin='lower', cmap='Greys')
        plt.show()

    for i in range(NT):
        flip_spin(spins)
        if i % snap_every == 0:
            snapshots[i // snap_every] = spins

    def animation():
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(T)
        IM = ax.imshow(snapshots[0], origin='lower', cmap='Greys')

        def animate(i):
            IM.set_array(snapshots[i])
            return [IM]
        animacja = anim.FuncAnimation(fig, animate, frames=N_snapshots)
        plt.show()

    animation()
if __name__=="__main__":
    ising(16, 1, 10000, 100)
    # ising(64, 1, 100000, 1000)
    # ising(64, 2.269185, 100000, 1000)
    # ising(64, 3.5, 100000, 1000)
