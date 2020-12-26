import numpy as np
import  copy
import matplotlib.pyplot as plt
np.random.seed(114514)


class yichuan():
    def __init__(self,pop,pop_size,DNA_size,graph,crossover_rate = 0.1555,mutation_rate=0.025):
        self.crossover_rate = crossover_rate#交叉概率
        self.mutation_rate = mutation_rate# 变异概率
        self.pop = pop#种群
        self.pop_size = pop_size#种群大小
        self.DNA_size = DNA_size#城市大小
        self.graph = graph#距离矩阵

    def compute_fitness(self, pop):
        # 初始化一个空表
        fitness = np.zeros(self.pop_size, dtype=np.float32)
        # 枚举每个个体
        for i, e in enumerate(pop):
            for j in range(self.DNA_size-1):
               # print(fitness)
                fitness[i] += self.graph[int(e[j])][int(e[j+1])]
        # 记录距离
        dis = copy.copy(fitness)
        # 适应度等于距离的倒数
        fitness = np.reciprocal(fitness)
        return fitness, dis

    # 轮盘赌，选择种群中的个体
    def select_population(self,fitness):
        #从种群中选择，pop_size个个体，每个个体被选择的概率为fitness / fitness.sum()
        indx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True,
                                    p=(fitness / fitness.sum()))

        #更新种群
        self.pop = self.pop[indx]

    def genetic_crossover(self):
        # 遍历种群每个个体
        for parent1 in self.pop:
            # 判断是否会基因交叉
            if np.random.rand() < self.crossover_rate:
                # 寻找父代
                n = np.random.randint(self.pop_size)
                parent2 = self.pop[n, :]
                # 随机产生基因交换片段
                pos = np.random.randint(self.DNA_size, size=2)
                # 区间左右端点
                l = min(pos)
                r = max(pos)
                # 记录区间
                seq = copy.copy(parent1[l:r])
                poss = []
                # 交换
                for i in range(self.DNA_size):
                    if parent2[i] in seq:
                        poss.append(i)
                a = 0
                for i in seq:
                    parent2[poss[a]] = i
                    a += 1
                b = 0
                for i in range(l, r):
                    parent1[i] = parent2[poss[b]]
                    b += 1

        # 种群中的所有个体基因突变
    def genetic_mutation(self):
        # 枚举个体
        for e in self.pop:
            # 变异的可能
            if np.random.rand() < self.mutation_rate:
                # 随机变异交换点
                position = np.random.randint(self.DNA_size, size=2)
                e[position[0]], e[position[1]] = e[position[1]], e[position[0]]



def init_pop(pop_size, DNA_size):
        # 初始化一个种群 大小为pop_size*DNA_size
        pop = np.zeros((pop_size, DNA_size))
        # DNA编码
        code = np.arange(DNA_size)
        for i in range(pop_size):
            pop[i] = copy.deepcopy(code)
            # 随机打乱
            np.random.shuffle(pop[i])
            b = np.where(pop[i] == 0)
            pop[i][b],pop[i][0] = pop[i][0],pop[i][b]
        # 返回种群
        return pop


def TSP(graph, pop_size, DNA_size, t):

        # 初始化一个种群
        pop = init_pop(pop_size, DNA_size)
        # 调用遗传算法类
        GA = yichuan(pop, pop_size, DNA_size, graph)
        # 保存最佳距离
        best_distance = 1e6
        d = []
        # 保存最佳路线
        route = None
        for i in range(t):
            # t-=1
            # 返回适应度，和距离函数
            fitness, dis = GA.compute_fitness(pop)

            d.append(min(dis))
            # 选择新的种群
            GA.select_population(fitness)
            # 基因交叉
            GA.genetic_crossover()
            # 基因突变
            GA.genetic_mutation()
            # 记录当前状态最优解
            # 返回最优解索引
            num = np.argmax(fitness)
            # 记录DNA
            DNA = GA.pop[num, :]
            # 保存最佳方案
            if best_distance > min(dis):
                best_distance = min(dis)
                route = DNA
        # 打印最终结果
        print("遗传算法最短近似路径为：")
        for each in route:
            print(int(each),"->",end= "")
        print("0")
        print("遗传算法最短近似路程为" ,{best_distance})
        print(d)
        plt.plot(range(t),np.array(d),'r')
        plt.show()

