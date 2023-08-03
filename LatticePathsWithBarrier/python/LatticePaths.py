import math
from itertools import combinations
import numpy as np


def IEP(m, n, barrier_input):
    '''容斥原理求解
    Args:
        m,n(int) : 格路终点坐标
        barriers_input(list) : 有障碍的路径列表,共k行(k为障碍数量),每行四个int(x1,y1,x2,x2)表示(x1,y1)与(x2,y2)间的路径不能通过

    Returns:
        result(int) : 有障碍的格路问题方案数
    '''
    barrier_input.sort(key=lambda x: (x[0], x[1]))  # 对障碍路径坐标进行排序
    barriers = []  # 有障碍的路径列表
    for barrier in barrier_input:
        x1, y1, x2, y2 = barrier
        barriers.append((int(min(x1, x2)), int(min(y1, y2)), int(
            max(x1, x2)), int(max(y1, y2))))  # 按路径起点坐标-终点坐标的方式存储一条路径
    full_paths = math.comb(m+n, n)
    result = full_paths  # 无约束条件下的路径方案数
    for i in range(1, len(barriers)+1):  # 求一定经过k条障碍的路径数
        for comb in combinations(barriers, i):  # 选择k条障碍可能的组合
            sub_result = math.comb(
                comb[0][0]+comb[0][1], comb[0][1])  # 起点到第一条障碍路径起点的方案数
            for k in range(1, len(comb)):
                if comb[k][0] >= comb[k-1][2] and comb[k][1] >= comb[k-1][3]:
                    # 上一条障碍终点到下一条障碍起点间的路径方案数
                    sub_result = sub_result * \
                        math.comb(comb[k][0]-comb[k-1][2]+comb[k]
                                  [1]-comb[k-1][3], comb[k][1]-comb[k-1][3])
                else:
                    sub_result = 0
            sub_result = sub_result * \
                math.comb(m-comb[-1][2]+n-comb[-1][3], n -
                          comb[-1][3])  # 最后一条障碍结束到终点间的方案数
            result = result+((-1)**i)*sub_result  # 根据容斥原理中的系数累加求得结果方案数
    return result


def DP(m, n, barrier_input):
    '''递推方式求解
    Args:
        m,n(int) : 格路终点坐标
        barriers_input(list) : 有障碍的路径列表,共k行(k为障碍数量),每行四个int(x1,y1,x2,x2)表示(x1,y1)与(x2,y2)间的路径不能通过
        plan_matrix : 递推矩阵

    Returns:
        result(int) : 有障碍的格路问题方案数
    '''

    barrier_map = {}
    for barrier in barrier_input:
        x1, y1, x2, y2 = barrier
        barrier_map[(int(max(x1, x2)), int(max(y1, y2)))] = (
            int(min(x1, x2)), int(min(y1, y2)))  # 以字典的方式存储障碍路径,key为障碍路径终点,val为起点
    plan_matrix = np.zeros((m+1, n+1), dtype=int)

    # 初始化递推矩阵
    for i in range(m+1):
        if (i, 0) in barrier_map.keys() and barrier_map[(i, 0)][1] == 0:
            break
        else:
            plan_matrix[i][0] = 1
    for j in range(n+1):
        if (0, j) in barrier_map.keys() and barrier_map[(0, j)][0] == 0:
            break
        else:
            plan_matrix[0][j] = 1

    for i in range(1, m+1):
        for j in range(1, n+1):
            if (i, j) not in barrier_map.keys():
                # 若点(i,j)不在障碍路径上,则可从两个方向移动至(i,j),递推关系为p[i][j]=p[i-1][j]+p[i][j-1]
                plan_matrix[i][j] = plan_matrix[i-1][j]+plan_matrix[i][j-1]
            elif barrier_map[(i, j)][0] == i:
                # 若(i,j)是一条垂直障碍路径的终点,则只能从左侧移动至点(i,j)
                plan_matrix[i][j] = plan_matrix[i-1][j]
            else:
                # 若(i,j)是一条水平障碍路径的终点,则只能从下方移动至点(i,j)
                plan_matrix[i][j] = plan_matrix[i][j-1]
    result = plan_matrix[m][n]
    return result


'''初始化格路问题

Inputs:
    m,n : 格路终点坐标
    num : 障碍路径条数
    (a,b),(c,d) : 每条障碍路径两个端点的坐标

可以直接调用IEP与DP两个函数接口进行计算,输入终点坐标及障碍表示矩阵即可

Example:
    10 5
    4
    2 2 3 2
    4 2 5 2
    6 2 6 3
    7 2 7 3
'''
m, n = input("格路终点坐标:").split()
m = int(m)
n = int(n)
num = int(input("障碍路径数:"))
barrier_input = []
for i in range(num):
    barrier_input.append(input("路径"+str(i)+"两端坐标:").split())

result = IEP(m, n, barrier_input)       # 容斥原理求解
result_dp = DP(m, n, barrier_input)  # 递推关系求解
print("容斥原理求解的方案数为: ", result)
print("递推方法求得的方案数为: ", result_dp)
