import random
import matplotlib.pyplot as plt

GRAPH = []


def calcfit(addr):  # 用于计算适应值, 1/总距离
    global GRAPH
    sum1 = 0
    now_city = 0
    for i in range(len(addr) - 1):  # 遍历
        now_city = addr[i]
        next_city = addr[i + 1]
        sum1 += GRAPH[now_city][next_city]
    sum1 += GRAPH[0][now_city]
    return 1 / sum1


def switchB2A(a, b):
    temp = b[:]  # 复制一份b防止b被修改
    q = []  # 用来存储最终的变换序列组
    for i in range(len(a)):
        # print(i)
        if a[i] != temp[i]:
            j = b.index(a[i])
            q.append([i, j])
            temp[j], temp[i] = temp[i], temp[j]  # 交换值
    return q


def multiply(w, v):
    l = int(w * len(v))  # 计算需要保留的路径
    res = v[0:l]
    return res


class Pso:
    generations = []  # 用于进行画图
    route_lengths = []  # 用于进行画图

    def __init__(self, graph, num, genenration, group_size):  # 对类进行初始化
        global GRAPH
        GRAPH = graph
        self.num = num
        self.generation = genenration
        self.group_size = group_size
        self.group = Group(self.num, self.generation, self.group_size)

    def get_bestbird(self):  # 用于找到最好的鸟,并且打印出相关的数据
        best_fit = 0
        best_bird = None
        for i in range(self.generation):  # 进行generation代的循环
            temp_bird = self.group.best
            temp_fit = temp_bird.fit
            self.generations.append(i)
            self.route_lengths.append(1 / temp_fit)
            if temp_fit > best_fit:  # 判断和寻找最好的鸟
                best_bird = temp_bird
                best_fit = temp_fit
            self.group.upDateBird()
        print("粒子群算法最短近似路径是:", end='')
        for i in best_bird.addr:
            print(i, end='')
            print('->', end='')
        print(0)
        print("粒子群算法最短近似路程是", end='')
        print(1 / best_fit)
        return 1 / best_fit

    def visualization(self):  # 用于结果的可视化操作
        plt.plot(self.generations, self.route_lengths, '-r')
        plt.show()


class Bird:
    def __init__(self, addr, city_num):
        self.v = []  # 鸟的速度
        self.city_num = city_num  # 城市的数量
        self.addr = addr[:]  # 鸟的此时路径
        self.bestAddr = addr[:]  # 鸟经过的最好路径
        self.fit = calcfit(addr)  # 鸟此时路径的适应值
        self.bestFit = self.fit  # 鸟最好路径的适应值

    def switch(self, switchq):
        for pair in switchq:
            i, j = pair[0], pair[1]
            self.addr[i], self.addr[j] = self.addr[j], self.addr[i]
        # 交换后自动更行自己的成员变量
        self.upDate()

    def upDate(self):  # 更新自己经过的最好路径
        newfit = calcfit(self.addr)
        self.fit = newfit
        if newfit > self.bestFit:
            self.bestFit = newfit
            self.bestAddr = self.addr[:]

    def change(self):  # 进行路径的转换,随机变换
        i, j = random.randrange(1, self.city_num - 1), random.randrange(1, self.city_num - 1)
        self.addr[i], self.addr[j] = self.addr[j], self.addr[i]
        self.upDate()

    def reverse(self):  # 类似于染色体变异的函数
        # 随机选择一个城市
        cityx = random.randrange(0, self.city_num - 1)  # 随机选取一个点作为起点
        noxcity = self.addr[:]  # 复制一份addr
        noxcity.remove(cityx)  # 删除刚刚选取的点
        maxFit = 0
        nearCity = noxcity[0]  # 选取第一个点为最近城市
        for c in noxcity:  # 循环寻找离的最近的城市
            fit = calcfit([c, cityx])
            if fit > maxFit:
                maxFit = fit
                nearCity = c
        index1 = self.addr.index(cityx)
        index2 = self.addr.index(nearCity)
        tmp = self.addr[index1 + 1:index2 + 1]
        tmp.reverse()
        self.addr[index1 + 1:index2 + 1] = tmp  # 对其进行翻转
        self.upDate()  # 更新鸟的参数


class Group:
    def __init__(self, num, generation, groupsize):
        self.group = []
        self.num = num
        self.generation = generation
        self.groupSize = groupsize  # 鸟的个数、粒子个数

        self.w = 0.11  # w为惯性系数，也就是保留上次速度的程度
        self.pChange = 0.42  # 变异系数pChange
        self.pReverse = 0.003  # 贪婪倒立变异概率

        self.initBirds()
        self.best = self.getBest()

    def initBirds(self):  # 创建鸟群的函数
        addr = [0]  # 因为从0开始 , 所以初始位置是0
        for i in range(self.groupSize):
            addr2 = [j + 1 for j in range(self.num - 1)]  # 先得到有序的数组
            random.shuffle(addr2)  # 将其打乱作为初始的路线
            addr.extend(addr2)
            bird = Bird(addr, self.num)  # 以此路线生成一只鸟
            addr = [0]
            self.group.append(bird)  # 加进鸟群中

    def getBest(self):  # 找到最好的鸟
        bestFit = 0
        bestBird = None
        # 遍历群体里的所有鸟，找到路径最短的
        for bird in self.group:  # 进行比较判断
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
            # 更新最优的鸟
            if bird.fit > self.best.fit:
                self.best = bird
