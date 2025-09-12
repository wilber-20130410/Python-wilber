#九九乘法表算法

for y in range(1, 10):
    for x in range(1,y + 1):
        print('%dX%d = %d'% (x, y, x * y), end=' ')
    print('')
