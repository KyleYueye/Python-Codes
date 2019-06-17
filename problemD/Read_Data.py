import matplotlib.pyplot as plt
import numpy as np
from math import e
from mpl_toolkits.mplot3d import Axes3D


def V(t):
    k = 0.48
    b = 1.2
    a = 40
    return a * (1 - b * e ** (-k * t)) ** 4


def twoD():
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    x = np.linspace(0,12)
    y = [V(s) for s in x]
    plt.plot(x,y,color='darkviolet',linewidth = 3)
    plt.xlabel('growing time $t$')
    plt.ylabel('weight')
    plt.show()


if __name__ == '__main__':
    twoD()