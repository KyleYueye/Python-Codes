#############################
# 马尔科夫链
# MCM2018 Python 代码模板 SJTU
# By: Yue Ye
#############################

# -------------------------------------------------------_____
# 输入数据的说明及注意事项：
# 1. 由于马尔科夫链中状态数和长度不定，本程序采用vector进行存储
# 2. 简单来讲，vector就是一个可变长度的数组，其提供的方法可参阅具体文档
# 3. C++可视化异常麻烦，如需可视化可使用python或者matlab的代码
# ------------------------------------------------------------

import numpy as np
from random import random #


# Markov 函数以a和m作为输入参数，m表示过程总状态数
# a为任意长list，每项的数字代表状态
# 为效率起见函数无异常检查，请保证a中每一项取值为 [0,m-1]
# 返回一个m×m矩阵，就是转移矩阵
def Markov(a,m):
    res = np.ndarray([m, m])
    n = len(a)
    for i in range(n-1):
        res[a[i],a[i+1]] += 1
    for i in range(m):
        sum = 0
        for j in range(m):
            sum += res[i, j]
        if sum == 0:
            for j in range(m):
                res[i, j] = 1/m
        else:
            for j in range(m):
                res[i, j] /= sum

    return res


# Generate 函数以trans，n，start作为输入参数，
# n表示希望生成的马尔科夫过程长度
# start为初始状态
# trans为转移矩阵
# 为效率起见函数无异常检查，请保证转移矩阵行和为1，start是合法状态，n为正
# 返回生成的马尔科夫过程
def Generate(trans,n,start):
    ans = []
    m = len(trans)
    prev = start
    for i in range(n):
        next = m-1
        pos = random()
        for j in range(m-1):
            if pos < trans[prev, j]:
                next = j
                break
            else:
                pos -= trans[prev,j]
        ans.append(next)
        prev = next
    return ans


if __name__ == '__main__':
    a = [0,0,1,0,1,1,0,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,0,0]
    b = a
    t = Markov(b, 2)
    g = Generate(t, 1000000, 0)
    res = Markov(g, 2)
    for i in res:
        for j in i:
            print(j, " \n")
