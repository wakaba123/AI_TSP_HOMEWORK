import random
import math
import matplotlib.pyplot as plt
import time
import numpy as np
# 读取数据
INF = 1e10
GRAPH = []
# 计算适应度，也就是距离分之一，这里用伪欧氏距离

def calcfit(gene):
    sum = 0
    # 从第0个到最后一个城市的距离
    for i in range(len(gene) - 2):
        nowcity = gene[i]
        nextcity = gene[i + 1]
        sum += GRAPH[nowcity][nextcity]

    # 最后一个城市回到原点的距离
    sum += GRAPH[nextcity][0]
    fitness = np.reciprocal(sum)
    return fitness


# 每个个体的类，方便根据基因计算适应度
class Person:
    def __init__(self, gene):
        self.gene = gene
        self.fit = calcfit(gene)


class Group:
    def __init__(self, GroupSize, GeneSize):
        self.GroupSize = GroupSize  # 种群规模
        self.GeneSize = GeneSize  # 基因数量，也就是城市数量
        self.initGroup()
        self.upDate()

    # 初始化种群，随机生成若干个体
    def initGroup(self):
        self.group = []
        i = 0
        while (i < self.GroupSize):
            i += 1
            gene = [0]
            gene1 = [i + 1 for i in range(self.GeneSize - 1)]
            random.shuffle(gene1)
            gene.extend(gene1)
            # print(gene)
            tmpPerson = Person(gene)
            self.group.append(tmpPerson)

    # 获取种群中适应度最高的个体
    def getBest(self):
        bestFit = self.group[0].fit
        best = self.group[0]
        for person in self.group:
            if (person.fit > bestFit):
                bestFit = person.fit
                best = person
        return best

    # 根据适应度，使用轮盘赌返回一个个体，用于遗传交叉
    def getOne(self):
        # section的简称，区间
        sec = [0]
        sumsec = 0
        for person in self.group:
            sumsec += person.fit
            sec.append(sumsec)
        p = random.random() * sumsec
        for i in range(len(sec)):
            if (p > sec[i] and p < sec[i + 1]):
                # 这里注意区间是比个体多一个0的
                return self.group[i]

    # 更新种群相关信息
    def upDate(self):
        self.best = self.getBest()


# 遗传算法的类，定义了遗传、交叉、变异等操作
class GA:
    def __init__(self, graph, GroupSize, GeneSize):
        global GRAPH
        GRAPH = graph
        self.group = Group(GroupSize, GeneSize)
        self.pCross = 0.35  # 交叉率
        self.pChange = 0.1  # 变异率
        self.Gen = 1  # 代数

    # 变异操作
    def change(self, gene):
        # 把列表随机的一段取出然后再随机插入某个位置
        # length是取出基因的长度，postake是取出的位置，posins是插入的位置
        geneLenght = len(gene)
        index1 = random.randint(1, geneLenght - 1)
        index2 = random.randint(1, geneLenght - 1)
        newGene = gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        return newGene

    # 交叉操作
    def cross(self, p1, p2):
        geneLenght = len(p1.gene)
        index1 = random.randint(1, geneLenght - 1)
        index2 = random.randint(index1, geneLenght - 1)
        tempGene = p2.gene[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in p1.gene:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        return newGene

    # 获取下一代
    def next_child(self):
        self.Gen += 1
        # next_child代表下一代的所有基因
        next_child = []
        # 将最优秀的基因直接传递给下一代
        next_child.append(self.group.getBest().gene[:])
        while (len(next_child) < self.group.GroupSize):
            pChange = random.random()
            pCross = random.random()
            p1 = self.group.getOne()
            if (pCross < self.pCross):
                p2 = self.group.getOne()
                newGene = self.cross(p1, p2)
            else:
                newGene = p1.gene[:]
            if (pChange < self.pChange):
                newGene = self.change(newGene)
            next_child.append(newGene)
        self.group.group = []
        for gene in next_child:
            self.group.group.append(Person(gene))
            self.group.upDate()
    # n代表代数，遗传算法的入口

    def run(self, n):
        Gen = []  # 代数
        dist = []  # 每一代的最优距离
        # 上面三个列表是为了画图
        i = 1
        while (i < n):
            self.next_child()
            i += 1
            Gen.append(i)
            temp = self.group.getBest()
            dist.append(1 / temp.fit)
        # 绘制进化曲线
        print("遗传算法最短近似路径是:", end='')
        for i in temp.gene:
            print(i, end='')
            print('->', end='')
        print(0)
        plt.plot(Gen, dist, '-r')
        plt.show()





