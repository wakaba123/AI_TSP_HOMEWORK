import random
import matplotlib.pyplot as plt
GRAPH = []


def calcfit(addr):  # 用于计算适应值, 1/总距离
    global GRAPH
    sum1 = 0
    now_city = 0
    for i in range(len(addr) - 1):
        now_city = addr[i]
        next_city = addr[i + 1]
        sum1 += GRAPH[now_city][next_city]
    sum1 += GRAPH[0][now_city]
    return 1 / sum1


def switchB2A(a, b):
    temp = b[:]
    q = []
    for i in range(len(a)):
        # print(i)
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
    generations = []
    route_lengths = []

    def __init__(self, graph, num, genenration, group_size):
        global GRAPH
        GRAPH = graph
        self.num = num
        self.generation = genenration
        self.group_size = group_size
        self.group = Group(self.num, self.generation, self.group_size)

    def get_bestbird(self):
        best_fit = 0
        best_bird = None
        for i in range(self.generation):
            temp_bird = self.group.best
            temp_fit = temp_bird.fit
            self.generations.append(i)
            self.route_lengths.append(1 / temp_fit)
            if temp_fit > best_fit:
                best_bird = temp_bird
                best_fit = temp_fit
            self.group.upDateBird()
        print("粒子群算法最短近似路径是:", end='')
        for i in best_bird.addr:
            print(i, end='')
            print('->',end='')
        print(0)
        print("粒子群算法最短近似路程是", end='')
        print(1 / best_fit)

    def visualization(self):
        plt.plot(self.generations, self.route_lengths, '-r')
        plt.show()


class Bird:
    def __init__(self, addr, city_num):
        self.v = []
        self.city_num = city_num
        self.addr = addr[:]
        self.bestAddr = addr[:]
        self.fit = calcfit(addr)
        self.bestFit = self.fit

    def switch(self, switchq):
        for pair in switchq:
            i, j = pair[0], pair[1]
            self.addr[i], self.addr[j] = self.addr[j], self.addr[i]
        # 交换后自动更行自己的成员变量
        self.upDate()

    def upDate(self):
        newfit = calcfit(self.addr)
        self.fit = newfit
        if newfit > self.bestFit:
            self.bestFit = newfit
            self.bestAddr = self.addr[:]

    def change(self):
        i, j = random.randrange(1, self.city_num - 1), random.randrange(1, self.city_num - 1)
        self.addr[i], self.addr[j] = self.addr[j], self.addr[i]
        self.upDate()

    def reverse(self):
        # 随机选择一个城市
        cityx = random.randrange(0, self.city_num - 1)
        noxcity = self.addr[:]
        noxcity.remove(cityx)
        maxFit = 0
        nearCity = noxcity[0]
        for c in noxcity:
            fit = calcfit([c, cityx])
            if fit > maxFit:
                maxFit = fit
                nearCity = c
        index1 = self.addr.index(cityx)
        index2 = self.addr.index(nearCity)
        tmp = self.addr[index1 + 1:index2 + 1]
        tmp.reverse()
        self.addr[index1 + 1:index2 + 1] = tmp
        self.upDate()


class Group:
    def __init__(self, num, generation, groupsize):
        self.group = []
        self.num = num
        self.generation = generation
        self.groupSize = groupsize  # 鸟的个数、粒子个数

        self.w = 0.25  # w为惯性系数，也就是保留上次速度的程度
        self.pChange = 0.3  # 变异系数pChange
        self.pReverse = 0.3  # 贪婪倒立变异概率

        self.initBirds()
        self.best = self.getBest()

    def initBirds(self):         # 创建鸟群的函数
        addr = [0]               # 因为从0开始 , 所以初始位置是0
        for i in range(self.groupSize):
            addr2 = [j+1 for j in range(self.num - 1)]   # 先得到有序的数组
            random.shuffle(addr2)   # 将其打乱作为初始的路线
            addr.extend(addr2)
            bird = Bird(addr, self.num)  # 以此路线生成一只鸟
            addr = [0]
            self.group.append(bird)     # 加进鸟群中

    def getBest(self):
        bestFit = 0
        bestBird = None
        # 遍历群体里的所有鸟，找到路径最短的
        for bird in self.group:
            nowfit = bird.fit
            if nowfit > bestFit:
                bestFit = nowfit
                bestBird = bird
        return bestBird

    # 更新每一只鸟的速度和位置
    def upDateBird(self):
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
            if random.random() < self.pReverse:
                bird.reverse()
            #更新最优的鸟
            if bird.fit > self.best.fit:
                self.best = bird
