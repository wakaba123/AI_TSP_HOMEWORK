import random
import numpy as np

num = int(input())  # 这里输入用于生成数据集
graph = [ [ 0 for i in range(num)] for j in range(num)]
lengths = list(np.random.normal(30, 10, num * num))
f = open("graphs.txt","wt+")
f.write(str(num)+'\n')
for i in range(num):
    for j in range(i):
        length = lengths.pop()
        while length < 0:
            length = lengths.pop()
            pass
        graph[i][j] = length
        graph[j][i] = length
        f.write('('+str(i)+','+str(j)+','+str(length)+')'+'\n')
print("success")



