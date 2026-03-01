# -*- coding: utf-8 -*-
# 求两个整数的最大公约数
# © 2025~2026 wilber-20130410

def Divisor(x, y):
    reduce = 0
    if x < y:
        reduce = x
    elif x > y:
        reduce = y
    else:
        return x
    while reduce >= 1:
        if x % reduce == 0 and y % reduce == 0:
            return reduce
        else:
            reduce -= 1

try:
    n1 = int(input('请输入第一个整数： '))
    n2 = int(input('请输入第二个整数： '))
    if n1 <= 0 or n2 <= 0:
        print('输入的整数应大于0')
    else:
        print('%d 和 %d 的最大公约数是 %d' % (n1, n2, Divisor(n1, n2)))
except:
    print('输入数字出错！')
