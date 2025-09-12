#累加器算法
import time

def Add_N(n1):
    total=0
    for a in range(1, n1 + 1):
        total = total + a
    return total

N = 10000
t1 = time.perf_counter()
print("1到%d 自然数累加结果为%d" % (N, Add_N(N)))
t2 = time.perf_counter()
print("循环累加算法用时： %.8f 秒" % (t2 - t1))

t3 = time.perf_counter()
print("采用累加公式计算1到%d 累加和为%d" % (N, N * (N + 1) / 2))
t4 = time.perf_counter()
print("循环累加算法用时： %.8f 秒" % (t4 - t3))