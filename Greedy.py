class Greedy:
    path = []

    def __init__(self, graph, num):  # 初始化类
        self.num = num
        self.graph = graph

    def output_graph(self):   # 输出初始图
        for i in self.graph:
            for j in i:
                print(j, end=',')
            print()

    def calculate(self):  # 计算近似最短路径并且将路径存储在path中
        temp_line = self.graph[0]
        min_var = 1e10
        min_num = 0
        sum_num = 0
        while len(self.path) < self.num:
            # print(self.path)
            for i, var in enumerate(temp_line):      # 寻找每个点以后的最邻近节点
                if len(self.path) != self.num - 1 and i  == 0:
                    continue
                if var < min_var and i not in self.path:
                    min_num = i
                    min_var = var
            self.path.append(min_num)   # 将其添加进路径
            sum_num += min_var
            min_var = 1e10
            temp_line = self.graph[min_num]  # 跳到下一个节点
        return sum_num

    def print_outcome(self):
        num = self.calculate()
        print("贪心算法近似最短路径长度为 " + str(num))

        print("贪心算法近似最短路径为:0",end='')
        for i in self.path:
            print("->", end='')
            print(i, end='')
