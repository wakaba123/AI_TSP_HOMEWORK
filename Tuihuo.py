import numpy as np
import matplotlib.pyplot as plt
import random


class Tuihuo:
    path = []

    def __init__(self, graph, num, value=0):  # 初始化类
        self.num = num
        self.graph = graph
        self.value = 0

    def output_graph(self):  # 输出初始图
        for i in self.graph:
            for j in i:
                print(j, end=',')
            print()

    def distance(self, tuihuocurrent):
        valuenow = 0
        for i in range(self.num - 1):
            valuenow += self.graph[tuihuocurrent[i]][tuihuocurrent[i + 1]]
        valuenow += self.graph[tuihuocurrent[self.num - 1]][0]
        return valuenow

    def threetuihuo(self, tuihuocurrent, x, y, w):
        if x > y:
            x, y = y, x
        if w > y:
            w, y = y, w
        if w > x:
            w, x = x, w
        temp1 = tuihuocurrent[x:y + 1] + tuihuocurrent[w + 1:x]
        tuihuocurrent[w + 1:y + 1] = temp1

        return tuihuocurrent

    def calculate(self):  # 计算近似最短路径并且将路径存储在path中
        result = []  # 用于生成可视化图表
        tuihuosolution = list(range(self.num))
        valuenow = 0
        valuenow = self.distance(tuihuosolution)
        valuebest = valuenow
        tuihuocurrent = tuihuosolution.copy()
        tuihuonow = tuihuosolution.copy()
        t = 100000  # 初始温度
        t1 = 1  # 最后底线温度
        r = 0.9999  # 降温参数

        while t > t1:
            # 使用两路扰乱和三路扰乱两种方式
            p1 = random.randrange(0, self.num - 1)
            if p1 > 0.5:  # 使用二路扰乱
                while 1:
                    x = random.randrange(0, self.num - 1)
                    y = random.randrange(0, self.num - 1) # 生成交换坐标点
                    if x != y:
                        break
                tuihuocurrent[x], tuihuocurrent[y] = tuihuocurrent[y], tuihuocurrent[x]
            else:  # 使用三路扰乱
                while 1:
                    x = random.randrange(0, self.num - 1)
                    y = random.randrange(0, self.num - 1)
                    w = random.randrange(0, self.num - 1)  # 生成交换坐标点
                    if x != y and x != w and y != w:
                        break
                tuihuocurrent = self.threetuihuo(tuihuocurrent, x, y, w)
            valuethen = self.distance(tuihuocurrent)

            # 判断是否接受该解
            if valuethen < valuenow:
                tuihuonow = tuihuocurrent.copy()
                valuenow = valuethen
                if valuethen < valuebest:
                    tuihuosolution = tuihuocurrent.copy()
                    valuebest = valuethen
            elif np.random.rand() < np.exp(-(valuethen - valuebest) / t):  # 一定概率在不是优解的情况下接受
                valuenow = valuethen
                tuihuonow = tuihuocurrent.copy()
            else:
                tuihuocurrent = tuihuonow.copy()

            t = t * r
            result.append(valuenow)

        plt.plot(np.array(result))
        plt.ylabel("valuenow")
        plt.xlabel("t")
        plt.show()
        self.value = valuebest
        return tuihuosolution

    def print_outcome(self):
        num = self.calculate()
        print("模拟退火算法近似最短路径为")
        print(0, end='')
        for i in range(len(num)):
            if i != 0:
                print("-> %d" % num[i], end='')
        print("-> 0")
        print("模拟退火算法近似最短路径长度为" + str(self.value))
