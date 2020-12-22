import random
import math
import matplotlib.pyplot as plt


def calcfit(addr, graph):  # 用于计算适应值
    sum1 = 0
    for i in range(-1, len(addr) - 1):
        now_city = addr[i]
        next_city = addr[i + 1]
        sum1 += graph[now_city][next_city]
    return 1 / sum1


def switchB2A(a, b):
    temp = b[:]
    q = []
    for i in range(len(a)):
        if a[i] != temp[i]:
            j = b.index(a[i])
            q.append([i, j])
            temp[j], temp[i] = temp[i], temp[j]  # 交换值
    return q


def multiply(w, v):
    l = int(w * len(v))
    res = v[0:l]
    return res


class Pso:
    def __init__(self, num, graph):
        self.graph = graph
        self.num = num
        self.cities = {}
        group = Group(self.graph,self.num)



class Bird:
    def __init__(self, addr):
        self.addr = addr[:]
        self.bestAddr = addr[:]
        self.v = []
        self.fit = calcfit(addr, self.graph)
        self.bestFit = calcfit(addr, self.graph)

    def switch(self, switchq):
        for pair in switchq:
            i, j = pair[0], pair[1]
            self.addr[i], self.addr[j] = self.addr[j], self.addr[i]
        # 交换后自动更行自己的成员变量
        self.upDate()

    def upDate(self):
        newfit = calcfit(self.addr)
        self.fit = newfit
        if (newfit > self.bestFit):
            self.bestFit = newfit
            self.bestAddr = self.addr[:]

    def change(self):
        i, j = random.randrange(0, 48), random.randrange(0, 48)
        self.addr[i], self.addr[j] = self.addr[j], self.addr[i]
        self.upDate()
'''
    def reverse(self):
        # 随机选择一个城市
        cityx = random.randrange(1, 49)
        noxcity = self.addr[:]
        noxcity.remove(cityx)
        maxFit = 0
        nearCity = noxcity[0]
        for c in noxcity:
            fit = calcfit([c, cityx])
            if (fit > maxFit):
                maxFit = fit
                nearCity = c
        index1 = self.addr.index(cityx)
        index2 = self.addr.index(nearCity)
        tmp = self.addr[index1 + 1:index2 + 1]
        tmp.reverse()
        self.addr[index1 + 1:index2 + 1] = tmp
        self.upDate()
'''

class Group:
    def __init__(self, graph, num):
        self.graph = graph
        self.num = num
        self.groupSize = 500  # 鸟的个数、粒子个数
        self.addrSize = 48  # 位置的维度，也就是TSP城市数量
        self.w = 0.25  # w为惯性系数，也就是保留上次速度的程度
        self.pChange = 0.1  # 变异系数pChange
        # self.pReverse = 0.1  # 贪婪倒立变异概率
        self.initBirds()
        self.best = self.getBest()
        self.Gen = 0

    def initBirds(self):
        self.group = []
        for i in range(self.groupSize):
            addr = [i + 1 for i in range(self.addrSize)]
            random.shuffle(addr)
            bird = Bird(addr)
            self.group.append(bird)

    def getBest(self):
        bestFit = 0
        bestBird = None
        # 遍历群体里的所有鸟，找到路径最短的
        for bird in self.group:
            nowfit = calcfit(bird.add, self.graph)
            if nowfit > bestFit:
                bestFit = nowfit
                bestBird = bird
        return bestBird

    def getAvg(self):
        sum = 0
        for p in self.group:
            sum += 1 / p.fit
        return sum / len(self.group)

    def showBest(self):
        print(self.Gen, ":", 1 / self.best.fit)

    # 更新每一只鸟的速度和位置
    def upDateBird(self):
        self.Gen += 1
        for bird in self.group:
            # g代表group，m代表me，分别代表自己和群组最优、自己最优的差
            deltag = switchB2A(self.best.addr, bird.addr)
            deltam = switchB2A(bird.bestAddr, bird.addr)
            newv = multiply(self.w, bird.v)[:] + multiply(random.random(), deltag)[:] + multiply(random.random(),
                                                                                                 deltam)
            bird.switch(newv)
            bird.v = newv
            if random.random() < self.pChange:
                bird.change()
            # if random.random() < self.pReverse:
            #  bird.reverse()
            # 顺便在循环里把最优的鸟更新了，防止二次遍历
            if bird.fit > self.best.fit:
                self.best = bird