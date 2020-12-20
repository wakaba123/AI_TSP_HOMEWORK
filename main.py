from Greedy import Greedy

INF = 1e10


def creat_graph(edges, num):
    a = [[int(INF) for i in range(num + 1)] for j in range(num + 1)]  # 创建一个二维数组
    for i in edges:
        a[int(i[1])-1][int(i[3])-1] = int(i[5]) # 将二维数组根据边的长度初始化
    return a


with open("graph.txt", "r") as f:
    num = f.readline()
    num = int(num)
    lines = f.readlines()
    graph = creat_graph(lines, int(num))[:]  # 将得到的图保存在graph中

if __name__ == '__main__':
    ans = Greedy(graph, num)
    # ans.output_graph()
    # ans.calculate()
    ans.print_outcome()


