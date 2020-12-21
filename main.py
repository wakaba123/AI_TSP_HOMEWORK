from Greedy import Greedy

INF = 1e10


def creat_graph(edges, num):
    a = [[int(INF) for i in range(num)] for j in range(num)]  # 创建一个二维数组
    for i in edges:
        i = i.strip().lstrip('(').rstrip(')\n').split(',')
        print(i[2])
        a[int(i[0])-1][int(i[1])-1] = float(i[2]) # 将二维数组根据边的长度初始化
        a[int(i[1])-1][int(i[0])-1] = float(i[2])
    return a


with open("graphs.txt", "r") as f:
    num = f.readline()
    num = int(num)
    lines = f.readlines()
    graph = creat_graph(lines, num)[:]  # 将得到的图保存在graph中

if __name__ == '__main__':
    ans = Greedy(graph, num)
    ans.output_graph()
    # ans.calculate()
    ans.print_outcome()


