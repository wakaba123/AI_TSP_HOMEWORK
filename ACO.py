import numpy as np
import math
import random
import matplotlib.pyplot as plt


def calcfit(addr, graph):  # 用于计算适应值
    sum1 = 0
    for i in range(-1, len(addr) - 1):
        now_city = addr[i]
        next_city = addr[i + 1]
        sum1 += graph[now_city][next_city]
    return 1 / sum1


# 计算两个城市的距离，用于启发信息计算
def calc2c(self, c1, c2):
    return self.graph[c1][c2]


# 信息素浓度表
#matrix = [[1 for i in range(10)] for i in range(10)]


# 蚂蚁的类，实现了根据信息素和启发信息完成一次遍历
class Ant:
    def __init__(self, graph, num):
        # tabu是已经走过的城市
        # 规定从第一个城市开始走
        self.tabu = [0]
        self.num = num
        self.allowed = [i for i in range(1, self.num)]
        self.nowCity = 0
        # a,b分别表示信息素和期望启发因子的相对重要程度
        self.a = 2
        self.b = 7
        # rho表示路径上信息素的挥发系数，1-rho表示信息素的持久性系数。
        self.rho = 0.1
        # 本条路线的适应度，距离分之一
        self.fit = 0
        self.graph = graph

    # 计算下一个城市去哪
    def next(self):
        sum = 0
        # 用一个数组储存下一个城市的概率
        p = [0 for i in range(self.num)]
        # 计算分母和分子
        for c in self.allowed:
            # 信息素浓度表
            matrix = [[1 for i in range(self.num)] for i in range(self.num)]
            tmp = math.pow(matrix[self.nowCity][c], self.a) * math.pow(1 / calc2c(self, self.nowCity, c), self.b)
            sum += tmp
            # 此处p是分子
            p[c] = tmp
        # 更新p为概率
        for c in self.allowed:
            p[c] = p[c] / sum
        # 更新p为区间
        for i in range(1, self.num):
            p[i] += p[i - 1]
        r = random.random()
        for i in range(self.num - 1):
            if (r < p[i + 1] and r > p[i]):
                # i+1即为下一个要去的城市
                self.tabu.append(i + 1)
                self.allowed.remove(i + 1)
                self.nowCity = i + 1
                return

    # 将所有城市遍历
    def tour(self):
        while (self.allowed):
            self.next()
        self.fit = calcfit(self.tabu, self.graph)

    # 更新信息素矩阵
    def updateMatrix(self):
        # line储存本次经历过的城市
        line = []
        for i in range(self.num - 2):
            # 因为矩阵是对阵的，2-1和1-2应该有相同的值，所以两个方向都要加
            line.append([self.tabu[i], self.tabu[i + 1]])
            line.append([self.tabu[i + 1], self.tabu[i]])
        # 信息素浓度表
        matrix = [[1 for i in range(self.num)] for i in range(self.num)]
        for i in range(1, self.num):
            for j in range(1, self.num):
                if ([i, j] in line):
                    matrix[i][j] = (1 - self.rho) * matrix[i][j] + self.fit
                else:
                    matrix[i][j] = (1 - self.rho) * matrix[i][j]

    # 一只蚂蚁复用，每次恢复初始状态
    def clear(self):
        self.tabu = [0]
        self.allowed = [i for i in range(1, self.num)]
        self.nowCity = 0
        self.fit = 0


# 蚁群算法的类，实现了算法运行过程
class ACO:
    def __init__(self, graph, num):
        # 初始先随机N只蚂蚁
        self.graph = graph
        self.num = num
        self.initN = 20
        self.bestTour = [i for i in range(1, self.num)]
        self.bestFit = calcfit(self.bestTour, graph)
        self.initAnt()

    def initAnt(self):
        i = 0
        tmpAnt = Ant(self.graph, self.num)
        print(self.initN, "只先锋蚂蚁正在探路")
        while (i < self.initN):
            i += 1
            tmpTour = [i for i in range(1, self.num)]
            random.shuffle(tmpTour)
            tmpAnt.tabu = tmpTour
            tmpAnt.allowed = []
            tmpAnt.updateMatrix()
            tmpFit = calcfit(tmpAnt.tabu, self.graph)
            if (tmpFit > self.bestFit):
                self.bestFit = tmpFit
                self.bestTour = tmpAnt.tabu
            tmpAnt.clear()

    # n为蚂蚁数量
    def startAnt(self, n):
        i = 0
        ant = Ant(self.graph, self.num)
        Gen = []  # 迭代次数
        distance = []  # 距离，这两个列表是为了画图
        while (i < n):
            i += 1
            ant.tour()
            if (ant.fit > self.bestFit):
                self.bestFit = ant.fit
                self.bestTour = ant.tabu
            print(i, ":", 1 / self.bestFit)
            ant.clear()
            Gen.append(i)
            distance.append(1 / self.bestFit)
            # 绘制求解过程曲线
        plt.plot(Gen, distance, '-r')
        plt.show()
        dist = 1 / self.bestFit

        print("蚁群算法最短近似路径是:", end='')
        for i in self.bestTour:
            print(i, end='')
            print('->', end='')
        print(0)
        print("蚁群算法最短近似路程是" + str(dist))
