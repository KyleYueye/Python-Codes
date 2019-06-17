import matplotlib.pyplot as plt
import numpy as np
from math import e
from mpl_toolkits.mplot3d import Axes3D


def a(year):
    x = np.linspace(0.01,10)

    y1 = e ** (-year * x) / (2 ** 0.5 - e ** (-1 * x))
    y2 = 0.01 / (2 ** 0.5 - 1) + 0 * x

    # plt.figure()
    # plt.plot(x,y1)
    plt.figure(figsize=(8,5))
    plt.plot(x,y1)
    plt.plot(x,y2,color='red',linewidth=2.0,linestyle='--')
    plt.show()


def f(year,x):
    y1 = e ** (-year * x) / (2 ** 0.5 - e ** (-1 * x))
    y2 = 0.01 / (2 ** 0.5 - 1)
    return y1-y2


def findk(year,a,b,c):
    mid = (a+b)/2
    if abs(f(year,mid))<c:
        return mid
    if f(year,a)*f(year,mid)<=0:
        return findk(year,a,(a+b)/2,c)
    if f(year,mid+c)*f(year,b)<=0:
        return findk(year,(a+b)/2+c,b,c)


def B(k):
    m = (2**0.5-1)/(2**0.5-e**(-1*k))
    return m


def A(B):
    return 10/(1-B)**4


def pl():
    x = np.linspace(1,70)
    y = [A(B(findk(s,0.01,10,0.0001)))for s in x]
    plt.plot(x,y)
    plt.show()


def V(t,year):
    k = findk(year,0.01,10,0.0001)
    b = B(k)
    a = A(b)
    return a*(1-b*e**(-k*t))**4

def threeD():
    fig = plt.figure()
    ax = Axes3D(fig)
    T = np.arange(1,100,5)
    t = T.shape[0]
    Y = np.arange(1,70,2)
    y = Y.shape[0]
    T,Y = np.meshgrid(T,Y)
    Z = np.ndarray([y,t])
    for i in range(y):
        for j in range(t):
            Z[i,j] = V(T[i,j],Y[i,j])

    a = np.arange(1,100,5)
    b = np.ndarray([t])
    for i in range(t):
        b[i] = V(a[i],50)
    ax.plot(a,b,50,zdir='y',linewidth=3,color='black',zorder=1)

    ax.plot_surface(T,Y,Z,rstride=1,cstride=1,cmap=plt.get_cmap('cool'),alpha=0.7,zorder=2)
    # ax.contour(T,Y,Z,zdir='z',offset=-2,cmap='cool')
    ax.set_zlim(0,32000)

    plt.xlabel('growing time $t$')
    plt.ylabel(r'grown-up time $\tau$')
    ax.set_zlabel('weight')


    #bx = fig.gca(projection='3d')
    #bx.plot(T[25,:],50,Z[25,:])

    plt.show()

def twoD():
    x = np.linspace(0,100)
    y = [V(s,50) for s in x]
    plt.plot(x,y,color='mediumturquoise',linewidth = 3)
    plt.xlabel('growing time $t$')
    plt.ylabel('weight')
    plt.show()


if __name__ == '__main__':
    # k = findk(50,0.01,10,0.001)
    # b = B(k)
    # print(k)
    # print(b)
    # print(A(b))
    threeD()