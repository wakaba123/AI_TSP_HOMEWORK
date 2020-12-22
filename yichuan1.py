import numpy as np
import  copy
np.seterr(divide='ignore',invalid='ignore')
np.random.seed(114514)
class yichuan():
    def __init__(self,pop,pop_size,DNA_size,graph,crossover_rate = 0.1555,mutation_rate=0.025):
        self.crossover_rate = crossover_rate#交叉概率
        self.mutation_rate = mutation_rate# 变异概率
        self.pop = pop#种群
        self.pop_size = pop_size#种群大小
        self.DNA_size = DNA_size#城市大小
        self.graph = graph#距离矩阵
        print(self.pop)




    def compute_fitness(self, pop,number):
        # 初始化一个空表
        fitness = np.zeros(self.pop_size, dtype=np.float32)
        # 枚举每个个体
        for i in range(number):
            for j in range(number):
                fitness[i] += self.pop[i][j]
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

        #花式索引，更新种群
        self.pop = self.pop[indx]

    def genetic_crossover(self):
        # 遍历种群每个个体
        for parent1 in self.pop:
            # 判断是否会基因交叉
            if np.random.rand() < self.crossover_rate:
                # 寻找父代2
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
            # 随机打乱函数
            np.random.shuffle(pop[i])
        # 返回种群
        return pop

def TSP(graph, pop_size, DNA_size, t):
        # 初始化一个种群
        pop = init_pop(pop_size, DNA_size)
        # 调用遗传算法类
        GA = yichuan(pop, pop_size, DNA_size, graph)
        # 保存最佳距离
        best_distance = 1e6
        # 保存最佳路线
        route = None
        # 保存最佳x坐标
        x = None
        # 保存适应度变化曲线
        fitness_process = []
        for i in range(t):
            # t-=1
            # 返回适应度，和距离函数
            fitness, dis = GA.compute_fitness(graph,DNA_size)
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
            # 打印当前状态
            print(f"The step is {i} ,the current best distance is {min(dis)} ,fitness is {max(fitness)}")
            lx = []

            # DNA转化为记录坐标
            fitness_process.append(max(fitness))
            for i in DNA:
                i = int(i)
                lx.append(i)

            # 保存最佳方案
            if best_distance > min(dis):
                best_distance = min(dis)
                route = DNA = GA.pop[num, :]
                x = copy.copy(lx)
        # 打印最终结果
        print(f"The best route is {route}")
        print(f"The route distance is {best_distance}")

