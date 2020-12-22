from Greedy import Greedy
from yichuan1 import yichuan
import numpy as np

from yichuan1 import TSP

INF = 1e10


def creat_graph(edges, num):
    a = [[int(INF) for i in range(num)] for j in range(num)]  # 创建一个二维数组
    b = [0]*2*num
    c = 0
    for i in edges:
        i = i.strip().lstrip('(').rstrip(')\n').split(',')
       # print(i[2])
        if b[int(i[0])] == 0:
            b[int(i[0])] = 1
            c += 1
        if b[int(i[1])] == 0:
            b[int(i[1])] = 1
            c += 1
        a[int(i[0])-1][int(i[1])-1] = float(i[2]) # 将二维数组根据边的长度初始化
        a[int(i[1])-1][int(i[0])-1] = float(i[2])
    return a,c#邻接矩阵,城市个数


with open("graphs.txt", "r") as f:
    num = f.readline()
    num = int(num)
    lines = f.readlines()
    graph,number = creat_graph(lines, num)[:]  # 将得到的图保存在graph中,城市数量


if __name__ == '__main__':
    #ans = Greedy(graph, num)
    # ans.calculate()
   # ans.print_outcome()
    TSP(graph,400,number,20)


