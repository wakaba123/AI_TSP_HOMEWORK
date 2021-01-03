from Greedy import Greedy
from SA import Tuihuo
from PSO import Pso
from GA import GA
from ACO import ACO
import time


INF = 1e10


def creat_graph(edges, num):
    a = [[int(INF) for i in range(num)] for j in range(num)]  # 创建一个二维数组
    b = [0]*2*num
    c = 0
    for i in edges:
        i = i.strip().lstrip('(').rstrip(')\n').split(',')

       # print(i[2])
        if b[int(i[0])] == 0:
            b[int(i[0])] = 1
            c += 1
        if b[int(i[1])] == 0:
            b[int(i[1])] = 1
            c += 1

        a[int(i[0])-1][int(i[1])-1] = float(i[2])   # 将二维数组根据边的长度初始化
        a[int(i[1])-1][int(i[0])-1] = float(i[2])
    return a   #邻接矩阵,城市个数


with open("graphs.txt", "r") as f:
    num = f.readline()
    num = int(num)
    lines = f.readlines()
    graph = creat_graph(lines, num)[:]  # 将得到的图保存在graph中,城市数量


if __name__ == '__main__':
    t_start = time.time()
    ans0 = Greedy(graph, num)  # greedy
    ans0.print_outcome()
    t_end = time.time()
    print("\n贪心算法时间为:%f\n"% (t_end-t_start))

    t_start = time.time()
    ans1 = ACO(graph, num)
    ans1.startAnt(10)
    t_end = time.time()
    print("蚁群算法时间为:%f秒\n" % (t_end - t_start))   # zyf's ACO

    t_start = time.time()
    ans2 = GA(graph, 20, num)
    ans2.run(15000)
    print("遗传算法最短近似路程为：", 1 / ans2.group.getBest().fit)
    t_end = time.time()
    print("遗传算法时间为:%f秒\n" % (t_end - t_start))

    t_start = time.time()
    ans3 = Pso(graph, num, 10000, 20)  # yjq's PSO
    ans3.get_bestbird()
    ans3.visualization()              # 可视化操作
    t_end = time.time()
    print("粒子群算法时间为:%f秒\n" % (t_end - t_start))  # 记录时间

    t_start = time.time()
    ans4 = Tuihuo(graph, num)  # lwh's SA
    ans4.print_outcome()
    t_end = time.time()
    print("模拟退火算法时间为:%f秒\n" % (t_end - t_start))  # 记录时间



