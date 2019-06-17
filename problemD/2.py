import matplotlib.pyplot as plt
import numpy as np
from math import e
from mpl_toolkits.mplot3d import Axes3D


def tmp():
    a = 100
    b = 1
    k = 0.05
    x = np.linspace(1,100)
    y = a*(1 - b * e ** (-k * x))

    plt.plot(x,y)
    plt.show()


def V(t,m):
    k = 0.05
    b = 1
    a = 100
    return a * (1 - b * e ** (-k * t)) ** (1/(1-m))


def richards():
    fig = plt.figure()
    ax = Axes3D(fig)
    T = np.arange(0,100,2)
    t = T.shape[0]
    M = np.arange(0,0.99,0.05)
    m = M.shape[0]
    T,M = np.meshgrid(T,M)
    Z = np.ndarray([m,t])
    for i in range(m):
        for j in range(t):
            Z[i,j] = V(T[i,j],M[i,j])

    ax.plot_surface(T,M,Z,rstride=1,cstride=1,cmap=plt.get_cmap('rainbow'))
    # ax.contour(T,M,Z,zdir='z',offset=-2,cmap='rainbow')
    ax.set_zlim(0,100)
    plt.xlabel('growing time $t$')
    plt.ylabel('parameter $m$')
    ax.set_zlabel(r'$V_t$')
    plt.show()


if __name__ == '__main__':
    # tmp()
    richards()